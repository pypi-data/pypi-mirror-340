import trafilatura
import requests
import base64
from playwright.sync_api import sync_playwright

def get_base64_from_url(url: str) -> str:
    # Làm sạch URL khỏi ký tự xuống dòng, khoảng trắng thừa và %0A
    clean_url = url.strip().replace('\n', '').replace('\r', '').replace('%0A', '')

    response = requests.get(clean_url)
    response.raise_for_status()  # Báo lỗi nếu tải không thành công

    return base64.b64encode(response.content).decode('utf-8')

def draw_web_content_playwright(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        
        print("== Page Title ==")
        print(page.title())
        
        print("\n== Body Preview ==")
        print(page.content())
        
        browser.close()
    
def draw_web_content_trafilatura(url: str) -> str:

    """
    This function retrieves and extracts the main content from a given URL.

    Parameters:
    - url: The URL to fetch and extract content from.

    Functionality:
    1. Fetches the content of the URL using the `trafilatura` library.
    2. Extracts the main content while excluding comments and tables.
    3. Limits the extracted content to 8000 characters for brevity.

    Returns:
    - The extracted content as a string or an error message if the process fails.
    """
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            extracted = trafilatura.extract(downloaded, include_comments=False, include_tables=False)
            print(extracted)
            return extracted[:8000] if extracted else "Unable to extract useful content."
        else:
            return "Unable to retrieve content from the URL."
    except Exception as e:
        return f"Error accessing {url}: {str(e)}"
    
def searxng_search(query: str) -> str:
    """
    This function performs a search using the SearxNG search engine.

    Parameters:
    - query: The search query string.

    Functionality:
    1. Sends a GET request to the SearxNG API with the query and specified parameters.
    2. Extracts the top 10 search results from the API response.
    3. Formats the results into a readable string containing the title, URL, and content of each result.

    Returns:
    - A formatted string of search results or an error message if the search fails.
    """
    base_url = "https://searxng.vbi-server.com"  # Base URL for the SearxNG instance
    params = {
        "q": query,  # Query string
        "format": "json",  # Response format
        "language": "en",  # Language for the search results
        "categories": "general"  # Search categories
    }

    try:
        # Send a GET request to the SearxNG API
        response = requests.get(f"{base_url}/search", params=params, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()  # Parse the JSON response

        # Extract the top 5 results
        results = data.get("results", [])[:10]
        if not results:
            return "No relevant results found."  # Return a message if no results are found

        # Format the results into a readable string
        return "\n\n".join([f"{r['title']}\n{r['url']}\n{r['content']}" for r in results])

    except Exception as e:
        # Handle exceptions and return an error message
        return f"Error during search: {str(e)}"

if __name__ == "__main__":
    print(get_base64_from_url("https://statics.gemxresearch.com/images/2025/04/09/155134/image.png"))