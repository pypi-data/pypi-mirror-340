import os
from uuid import UUID
from typing import Optional, Union, List, Dict, Any

from aidolon_browser_client import AuthenticatedClient
from aidolon_browser_client.api.session_management import (
    create_browser_session,
    close_browser_session,
    get_session_status,
    get_browser_context
)
from aidolon_browser_client.api.browser_actions import (
    click_element,
    type_text,
    navigate_browser,
    press_key,
    drag_and_drop
)
from aidolon_browser_client.api.content_extraction import (
    take_screenshot,
    scrape_information,
    scrape_page,
    generate_pdf
)
from aidolon_browser_client.models import (
    CreateBrowserSessionBody,
    ClickElementBody,
    ClickElementBodyWait,
    TypeTextBody,
    NavigateBrowserBody,
    PressKeyBody,
    PressKeyBodyWait,
    DragAndDropBody,
    TakeScreenshotBody,
    ScrapeInformationBody,
    ScrapeInformationBodyLevelOfDetail,
    ScrapePageBody,
    ScrapePageBodyFormatItem,
    GeneratePdfBody,
    BrowserContext
)
from aidolon_browser_client.models.error import Error

class BrowserSession:

    """
    A browser session for interacting with the Aidolon API.

    Attributes:
        client (AuthenticatedClient): The API client used for requests.
        session_id (Optional[str]): The unique identifier for the session.
        live_viewer_url (Optional[str]): URL for the live session viewer.
        dimensions (Optional[tuple]): Dimensions of the session display.
        user_agent (Optional[str]): The browser user agent used.
        timeout (int): Timeout for the session in seconds.
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = None, context: Optional[Dict[str, Any]] = None, timeout: int = 300):
        """Initialize an aidolon browser session.
        
        Args:
            api_key: API key for Aidolons. If None, will try to get from environment variable.
            base_url: Base URL for Aidolons API.
            context: Optional browser context dictionary (cookies, localStorage, sessionStorage, userAgent).
            timeout: Session timeout in seconds. Default is 300 seconds (5 minutes).
        """
        if not base_url:
            if os.getenv("AIDOLONS_API_BASE_URL"):
                base_url = os.getenv("AIDOLONS_API_BASE_URL")
            else:
                base_url = "https://api.aidolon.com/api/v1"
        self.client = AuthenticatedClient(base_url=base_url, token=api_key) if api_key else AuthenticatedClient(base_url=base_url)
        self.session_id = None
        self.live_viewer_url = None
        self.dimensions = None
        self.user_agent = None
        self.timeout = None
        
        # Create a browser session with context if provided
        if context is not None:
            browser_context = BrowserContext.from_dict(context)
            session_body = CreateBrowserSessionBody(
                visible=True,
                timeout=timeout,
                context=browser_context
            )
        else:
            session_body = CreateBrowserSessionBody(
                visible=True,
                timeout=timeout
            )
        
        response = create_browser_session.sync(
            client=self.client,
            body=session_body
        )
        
        if hasattr(response, 'session_id'):
            self.session_id = response.session_id
            self.live_viewer_url = response.embed_url if hasattr(response, 'embed_url') else None
            
            if hasattr(response, 'live_session'):
                live_session = response.live_session
                self.dimensions = live_session.dimensions if hasattr(live_session, 'dimensions') else None
                self.user_agent = live_session.user_agent if hasattr(live_session, 'user_agent') else None
                self.timeout = live_session.timeout if hasattr(live_session, 'timeout') else None
            
            print("Browser session started.")
        else:
            raise Exception("Failed to create browser session.")
    
    def click(self, selector: str, wait: str = "auto"):
        """Click on an element in the browser.
        
        Args:
            selector: CSS selector, XPath, or natural language description.
            wait: Wait strategy ("auto", "navigation", "load", "domcontentloaded", "networkidle").
        """
        if not self.session_id:
            raise Exception("No active browser session.")
            
        wait_enum = getattr(ClickElementBodyWait, wait.upper(), ClickElementBodyWait.AUTO)
        
        click_body = ClickElementBody(
            selector=selector,
            wait=wait_enum
        )
        
        response = click_element.sync(
            client=self.client,
            session_id=self.session_id,
            body=click_body
        )
        
        print("Browser clicked.")
        return response
    
    def navigate(self, url: str):
        """Navigate to a specific URL.
        
        Args:
            url: URL to navigate to.
        """
        if not self.session_id:
            raise Exception("No active browser session.")
            
        navigate_body = NavigateBrowserBody(url=url)
        
        response = navigate_browser.sync(
            client=self.client,
            session_id=self.session_id,
            body=navigate_body
        )
        
        print(f"Navigated to {url}")
        return response
    
    def type(self, selector: str, text: str):
        """Type text into an element.
        
        Args:
            selector: CSS selector, XPath, or natural language description.
            text: Text to type.
        """
        if not self.session_id:
            raise Exception("No active browser session.")
            
        type_body = TypeTextBody(
            selector=selector,
            text=text
        )
        
        response = type_text.sync(
            client=self.client,
            session_id=self.session_id,
            body=type_body
        )
        
        print(f"Typed text: {text}")
        return response
    
    def press(self, selector: str, key: str, wait: str = "auto"):
        """Press a key on an element.
        
        Args:
            selector: CSS selector, XPath, or natural language description.
            key: Key to press (e.g., "Enter", "Tab").
            wait: Wait strategy ("auto", "navigation", "network", "none").
        """
        if not self.session_id:
            raise Exception("No active browser session.")
            
        wait_enum = getattr(PressKeyBodyWait, wait.upper(), PressKeyBodyWait.AUTO)
        
        press_body = PressKeyBody(
            selector=selector,
            key=key,
            wait=wait_enum
        )
        
        response = press_key.sync(
            client=self.client,
            session_id=self.session_id,
            body=press_body
        )
        
        print(f"Pressed key: {key}")
        return response
    
    def drag_and_drop(self, source_selector: str, target_selector: str):
        """Drag and drop an element to a target location.
        
        Args:
            source_selector: CSS selector, XPath, or natural language description of the element to drag.
            target_selector: CSS selector, XPath, or natural language description of the drop target.
        """
        if not self.session_id:
            raise Exception("No active browser session.")
            
        drag_body = DragAndDropBody(
            source_selector=source_selector,
            target_selector=target_selector
        )
        
        response = drag_and_drop.sync(
            client=self.client,
            session_id=self.session_id,
            body=drag_body
        )
        
        print(f"Dragged from {source_selector} to {target_selector}")
        return response
    
    def take_screenshot(self, full_page: bool = True):
        """Take a screenshot of the current page.
        
        Args:
            full_page: Whether to capture the full page or just the viewport.
            
        Returns:
            Response containing url of captured image.
        """
        if not self.session_id:
            raise Exception("No active browser session.")
            
        screenshot_body = TakeScreenshotBody(
            full_page=full_page
        )
        
        response = take_screenshot.sync(
            client=self.client,
            session_id=self.session_id,
            body=screenshot_body
        )
        
        print("Screenshot taken.")
        return response
    
    def scrape_information(self, description: str, level_of_detail: str = "full"):
        """Scrape specific information from the page based on a description. This function
        allows natural language queries to the webpage content.
        
        Args:
            description: Description of what information to extract.
            level_of_detail: Level of detail to include ("basic", "standard", "full").
            
        Returns:
            Response containing structured data from the page.
        """
        if not self.session_id:
            raise Exception("No active browser session.")
        
        detail_enum = getattr(ScrapeInformationBodyLevelOfDetail, level_of_detail.upper(), 
                             ScrapeInformationBodyLevelOfDetail.FULL)
            
        scrape_body = ScrapeInformationBody(
            description=description,
            level_of_detail=detail_enum
        )
        
        response = scrape_information.sync(
            client=self.client,
            session_id=self.session_id,
            body=scrape_body
        )
        
        print(f"Information scraped: {description}")
        return response.data
    
    def scrape_page(self, format: List[str] = None, delay: float = 0,
                    screenshot: bool = False, pdf: bool = False):
        """Scrape the entire page content in various formats.
        
        Args:
            format: List of formats to return (e.g., ["html", "text", "json", "markdown"]).
            delay: Delay in seconds before scraping.
            screenshot: Whether to include a screenshot.
            pdf: Whether to include a PDF version.
            
        Returns:
            Response containing the page content in the requested formats.
        """
        if not self.session_id:
            raise Exception("No active browser session.")
            
        if format is None:
            format = ["html", "text"]
            
        format_enums = []
        for fmt in format:
            format_enum = getattr(ScrapePageBodyFormatItem, fmt.upper(), None)
            if format_enum:
                format_enums.append(format_enum)
            
        scrape_body = ScrapePageBody(
            format_=format_enums,
            delay=delay,
            screenshot=screenshot,
            pdf=pdf
        )
        
        response = scrape_page.sync(
            client=self.client,
            session_id=self.session_id,
            body=scrape_body
        )
        
        print("Page scraped.")
        return response
    
    def generate_pdf(self, delay: float = 0):
        """Generate a PDF of the current page.
        
        Args:
            delay: Delay in seconds before generating the PDF.
            
        Returns:
            Response containing url of PDF.
        """
        if not self.session_id:
            raise Exception("No active browser session.")
            
        pdf_body = GeneratePdfBody(
            delay=delay
        )
        
        response = generate_pdf.sync(
            client=self.client,
            session_id=self.session_id,
            body=pdf_body
        )
        
        print("PDF generated.")
        return response
    
    def get_details(self) -> Dict[str, Any]:
        """Retrieve the latest session details from the remote API.
        
        Returns:
            Complete session details as a dictionary.
        """
        if not self.session_id:
            raise Exception("No active browser session.")
        
        response = get_session_status.sync(
            client=self.client,
            session_id=self.session_id
        )
        
        return response
    
    def get_status(self) -> str:
        """Get the current status of the browser session.
        
        Returns:
            Status string.
        """
        details = self.get_details()
        
        return details.status if hasattr(details, 'status') else 'unknown'
    
    def get_context(self) -> Dict[str, Any]:
        """Retrieve the browser context data from the remote API.
        
        Returns:
            Context data as a dictionary.
        """
        if not self.session_id:
            raise Exception("No active browser session.")
        
        response = get_browser_context.sync(
            client=self.client,
            session_id=self.session_id
        )
        
        return response.context if hasattr(response, 'context') else response
    
    def close_session(self):
        """Close the browser session and release resources."""
        if not self.session_id:
            print("No active browser session to close.")
            return
            
        response = close_browser_session.sync(
            client=self.client,
            session_id=self.session_id
        )
        
        self.session_id = None
        print("Browser session closed.")
        return response
    
    def __enter__(self):
        """Return self to allow access to instance methods inside the with block."""
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """Ensure that the session is closed when exiting the with block."""
        self.close_session()


def create_session(api_key: Optional[str] = None, base_url: str = "https://api.aidolon.com", context: Optional[Dict[str, Any]] = None, timeout: int = 300):
    """Create a new browser session.
    
    Args:
        api_key: API key for Aidolon. If None, will try to get from environment variable.
        base_url: Base URL for Aidolon API.
        context: Optional browser context dictionary (cookies, localStorage, sessionStorage, userAgent).
        timeout: Session timeout in seconds. Default is 300 seconds (5 minutes).
    
    Returns:
        BrowserSession object.
    """
    return BrowserSession(api_key=api_key, base_url=base_url, context=context, timeout=timeout)
