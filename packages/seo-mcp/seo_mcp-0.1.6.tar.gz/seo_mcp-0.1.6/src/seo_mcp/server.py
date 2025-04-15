"""
SEO MCP Server: A free SEO tool MCP (Model Control Protocol) service based on Ahrefs data. Includes features such as backlinks, keyword ideas, and more.
"""
import requests
import time
import os
import urllib.parse
from typing import Dict, List, Optional, Any

from fastmcp import FastMCP
from seo_mcp.backlinks import get_backlinks, load_signature_from_cache, get_signature_and_overview
from seo_mcp.keywords import get_keyword_ideas

mcp = FastMCP("SEO MCP")

# CapSolver website: https://dashboard.capsolver.com/passport/register?inviteCode=1dTH7WQSfHD0
# Get API Key from environment variable - must be set for production use
api_key = os.environ.get("CAPSOLVER_API_KEY")


def get_capsolver_token(site_url: str) -> Optional[str]:
    """
    Use CapSolver to solve the captcha and get a token
    
    Args:
        site_url: Site URL to query
        
    Returns:
        Verification token or None if failed
    """
    if not api_key:
        print("ERROR: CAPSOLVER_API_KEY environment variable not set")
        return None
    
    payload = {
        "clientKey": api_key,
        "task": {
            "type": 'AntiTurnstileTaskProxyLess',
            "websiteKey": "0x4AAAAAAAAzi9ITzSN9xKMi",  # site key of your target site: ahrefs.com,
            "websiteURL": site_url,
            "metadata": {
                "action": ""  # optional
            }
        }
    }
    res = requests.post("https://api.capsolver.com/createTask", json=payload)
    resp = res.json()
    task_id = resp.get("taskId")
    if not task_id:
        print(f"ERROR: Failed to create captcha task: {res.text}")
        return None
    print(f"INFO: Got taskId: {task_id}, waiting for solution...")
 
    while True:
        time.sleep(1)  # delay
        payload = {"clientKey": api_key, "taskId": task_id}
        res = requests.post("https://api.capsolver.com/getTaskResult", json=payload)
        resp = res.json()
        status = resp.get("status")
        if status == "ready":
            token = resp.get("solution", {}).get('token')
            print(f"INFO: Captcha token obtained successfully")
            return token
        if status == "failed" or resp.get("errorId"):
            print(f"ERROR: Captcha solving failed: {res.text}")
            return None


@mcp.tool()
def get_backlinks_list(domain: str) -> Optional[Dict[str, Any]]:
    """
    Get backlinks list for the specified domain
    Args:
        domain (str): The domain to query
    Returns:
        List of backlinks for the domain, containing title, URL, domain rating, etc.
    """
    # Try to get signature from cache
    signature, valid_until, overview_data = load_signature_from_cache(domain)
    
    # If no valid signature in cache, get a new one
    if not signature or not valid_until:
        # Step 1: Get token
        site_url = f"https://ahrefs.com/backlink-checker/?input={domain}&mode=subdomains"
        token = get_capsolver_token(site_url)
        if not token:
            print(f"ERROR: Failed to get verification token for domain: {domain}")
            raise Exception(f"Failed to get verification token for domain: {domain}")
        
        # Step 2: Get signature and validUntil
        signature, valid_until, overview_data = get_signature_and_overview(token, domain)
        if not signature or not valid_until:
            print(f"ERROR: Failed to get signature for domain: {domain}")
            raise Exception(f"Failed to get signature for domain: {domain}")
    
    # Step 3: Get backlinks list
    backlinks = get_backlinks(signature, valid_until, domain)
    return {
        "overview": overview_data,
        "backlinks": backlinks
    }


@mcp.tool()
def keyword_generator(keyword: str, country: str = "us", search_engine: str = "Google") -> Optional[List[str]]:
    """
    Get keyword ideas for the specified keyword
    """
    site_url = f"https://ahrefs.com/keyword-generator/?country={country}&input={urllib.parse.quote(keyword)}"
    token = get_capsolver_token(site_url)
    if not token:
        print(f"ERROR: Failed to get verification token for keyword: {keyword}")
        raise Exception(f"Failed to get verification token for keyword: {keyword}")
    return get_keyword_ideas(token, keyword, country, search_engine)

# Main execution

def main():
    """Run the MCP server"""
    mcp.run()


if __name__ == "__main__":
    main()
