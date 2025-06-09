"""
HTML fetching endpoint using Playwright
"""
from typing import Optional, Dict, List, Any
from fastapi import APIRouter, HTTPException, BackgroundTasks
import asyncio
import time
from app.config.settings import logger, IGNORE_HTTPS_ERRORS, PRESERVE_IMG_TAGS
from app.models.schemas import HtmlRequest, HtmlResponse

router = APIRouter()

# Browser pool management
browser_pool = []
MAX_POOL_SIZE = 3
browser_pool_lock = asyncio.Lock()

# Initialize Playwright
async def init_playwright():
    """Initialize Playwright and return a browser instance"""
    try:
        from playwright.async_api import async_playwright
        playwright = await async_playwright().start()
        return playwright
    except Exception as e:
        logger.error(f"Failed to initialize Playwright: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to initialize Playwright: {str(e)}")

# Browser management functions
async def get_browser():
    """Get a browser from the pool or create a new one"""
    async with browser_pool_lock:
        if browser_pool:
            logger.info("Reusing browser from pool")
            return browser_pool.pop()
        
        logger.info("Creating new browser instance")
        try:
            playwright = await init_playwright()
            browser = await playwright.webkit.launch(
                headless=True,
            )
            return {"playwright": playwright, "browser": browser}
        except Exception as e:
            logger.error(f"Error creating browser: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error creating browser: {str(e)}")

async def return_browser(browser_data):
    """Return a browser to the pool"""
    async with browser_pool_lock:
        if len(browser_pool) < MAX_POOL_SIZE:
            browser_pool.append(browser_data)
            logger.info(f"Returned browser to pool. Pool size: {len(browser_pool)}")
        else:
            logger.info("Browser pool full, closing browser")
            try:
                await browser_data["browser"].close()
                await browser_data["playwright"].stop()
            except Exception as e:
                logger.error(f"Error closing browser: {str(e)}")

# HTML fetching function
async def fetch_html_with_playwright(request: HtmlRequest) -> HtmlResponse:
    """Fetch HTML content using Playwright"""
    start_time = time.time()
    browser_data = None
    
    try:
        browser_data = await get_browser()
        browser = browser_data["browser"]
        
        # Create context with headers if provided
        context_options = {
            "ignore_https_errors": IGNORE_HTTPS_ERRORS  # Use the config setting
        }
        if request.headers:
            context_options["extra_http_headers"] = request.headers
        if not request.images_enabled:
            context_options["java_script_enabled"] = True
            context_options["bypass_csp"] = True
            context_options["viewport"] = {"width": 1280, "height": 720}
            
        context = await browser.new_context(**context_options)
        page = await context.new_page()
        
        # Handle image loading based on settings and request parameters
        # Use request.preserve_img_tags if provided, otherwise use global setting
        preserve_img_tags = request.preserve_img_tags if request.preserve_img_tags is not None else PRESERVE_IMG_TAGS
        
        # Setup request interception - this happens before page navigation
        if not request.images_enabled:
            # Block all image loading requests regardless of preserve_img_tags setting
            # This prevents actual image downloading but keeps the img tags in the DOM
            await page.route("**/*.{png,jpg,jpeg,gif,webp,svg,avif,webp}", lambda route: route.abort())
            
            # If preserving img tags, we don't need additional CSS since we're not removing the tags
            if preserve_img_tags:
                # Add script to prevent image loading attempts but keep tags in DOM
                await page.add_script_tag(content="""
                    // Prevent further image loading without removing elements
                    const observer = new MutationObserver((mutations) => {
                        mutations.forEach(mutation => {
                            if (mutation.addedNodes) {
                                mutation.addedNodes.forEach(node => {
                                    if (node.tagName === 'IMG') {
                                        node.setAttribute('loading', 'lazy');
                                        node.setAttribute('src', 'about:blank');
                                    }
                                });
                            }
                        });
                    });
                    observer.observe(document.documentElement, { childList: true, subtree: true });
                    
                    // Handle existing images
                    document.querySelectorAll('img').forEach(img => {
                        img.setAttribute('loading', 'lazy');
                        img.setAttribute('src', 'about:blank');
                    });
                """)
        
        # Navigate to the URL - use domcontentloaded by default to avoid waiting for images
        # if not explicitly requested
        navigation_options = {"timeout": request.timeout}
        if request.wait_until == "selector":
            navigation_options["wait_until"] = "domcontentloaded"
        elif request.wait_until == "load" and not request.images_enabled:
            # If images are disabled but wait_until is "load", use "domcontentloaded" instead
            # to prevent timeouts waiting for images that will never load
            navigation_options["wait_until"] = "domcontentloaded"
            logger.info("Changed wait_until from 'load' to 'domcontentloaded' because images are disabled")
        else:
            navigation_options["wait_until"] = request.wait_until
            
        await page.goto(str(request.url), **navigation_options)
        
        # Wait for selector if specified
        if request.wait_until == "selector" and request.selector:
            await page.wait_for_selector(request.selector, state="visible", timeout=request.timeout)
            
        # Additional wait if specified
        if request.wait_for > 0:
            await asyncio.sleep(request.wait_for / 1000)  # Convert ms to seconds
        
        # Get HTML content and metadata
        html = await page.content()
        title = await page.title()
        
        # Extract meta tags
        meta_tags = await page.evaluate("""() => {
            const metaTags = {};
            document.querySelectorAll('meta').forEach(meta => {
                if (meta.name && meta.content) {
                    metaTags[meta.name] = meta.content;
                } else if (meta.getAttribute('property') && meta.content) {
                    metaTags[meta.getAttribute('property')] = meta.content;
                }
            });
            return metaTags;
        }""")
        
        # Clean up
        await context.close()
        
        fetch_time = time.time() - start_time
        logger.info(f"HTML fetched in {fetch_time:.2f} seconds")
        
        return HtmlResponse(
            html=html,
            url=str(request.url),
            status="success",
            fetch_time=fetch_time,
            title=title,
            meta=meta_tags
        )
    
    except Exception as e:
        logger.error(f"Error fetching HTML: {str(e)}")
        fetch_time = time.time() - start_time
        return HtmlResponse(
            html="",
            url=str(request.url),
            status=f"error: {str(e)}",
            fetch_time=fetch_time
        )
    finally:
        # Return browser to pool
        if browser_data:
            await return_browser(browser_data)

# Initialize browser pool
async def initialize_browser_pool(background_tasks: BackgroundTasks):
    """Initialize the browser pool in the background"""
    async def _init_pool():
        async with browser_pool_lock:
            logger.info(f"Initializing browser pool with {MAX_POOL_SIZE} browsers")
            global browser_pool
            
            # Close any existing browsers
            for browser_data in browser_pool:
                try:
                    await browser_data["browser"].close()
                    await browser_data["playwright"].stop()
                except Exception as e:
                    logger.error(f"Error closing browser: {str(e)}")
            
            browser_pool = []
            
            # Create new browser instances
            for _ in range(MAX_POOL_SIZE):
                try:
                    browser_data = await get_browser()
                    browser_pool.append(browser_data)
                except Exception as e:
                    logger.error(f"Error initializing browser: {str(e)}")
            
            logger.info(f"Browser pool initialized with {len(browser_pool)} browsers")
    
    background_tasks.add_task(_init_pool)
    return {"status": "Browser pool initialization started"}

# Endpoints
@router.post("/get_html", response_model=HtmlResponse)
async def get_html(request: HtmlRequest):
    """
    Fetch HTML content from a URL using Playwright
    """
    try:
        return await fetch_html_with_playwright(request)
    except Exception as e:
        logger.error(f"Error in get_html endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/init_browser_pool")
async def init_pool(background_tasks: BackgroundTasks):
    """
    Initialize or refresh the browser pool
    """
    return await initialize_browser_pool(background_tasks)

@router.get("/browser_pool_status")
async def pool_status():
    """
    Get the current status of the browser pool
    """
    return {
        "pool_size": len(browser_pool),
        "max_pool_size": MAX_POOL_SIZE
    } 