"""
Check the estimated search traffic for any website. Try Ahrefs' free traffic checker.
"""

from typing import Optional, Dict, Any, Literal, List
import requests


def check_traffic(token: str, domain_or_url: str, mode: Literal["subdomains", "exact"] = "subdomains", country: str = "") -> Optional[Dict[str, Any]]:
    """
    Check the estimated search traffic for any website.
    
    Args:
        domain_or_url (str): The domain or URL to query
        token (str): Verification token
        mode (str): Query mode, default is "subdomains"
        country (str): Country, default is "None"
    
    Returns:
        Optional[Dict[str, Any]]: Dictionary containing traffic data, returns None if request fails
    """
    print(f"Getting website traffic data, domain: {domain_or_url}...")
    
    if not token:
        print("Failed to get verification token")
        return None
    
    url = "https://ahrefs.com/v4/stGetFreeTrafficOverview"
    
    params = {
        "input": {
            "captcha": token,
            "country": country,
            "protocol": "",
            "mode": mode,
            "url": domain_or_url
        }
    }
    
    headers = {
        "accept": "*/*",
        "content-type": "application/json",
        "referer": f"https://ahrefs.com/traffic-checker/?input={domain_or_url}&mode={mode}"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code != 200:
            print(f"Request failed, status code: {response.status_code}")
            print(response.text)
            return None
        
        data: Optional[List[Any]] = response.json()

        # 检查响应数据格式
        if not isinstance(data, list) or len(data) < 2 or data[0] != "Ok":
            print(f"Incorrect response data format: {data}")
            return None
        
        # 提取有效数据
        traffic_data = data[1]
        
        # 格式化返回结果
        result = {
            "traffic_history": traffic_data.get("traffic_history", []),
            "traffic": {
                "trafficMonthlyAvg": traffic_data.get("traffic", {}).get("trafficMonthlyAvg", 0),
                "costMontlyAvg": traffic_data.get("traffic", {}).get("costMontlyAvg", 0)
            },
            "top_pages": traffic_data.get("top_pages", []),
            "top_countries": traffic_data.get("top_countries", []),
            "top_keywords": traffic_data.get("top_keywords", [])
        }
        
        print(f"Successfully got traffic data for {domain_or_url}")
        return result
    except Exception as e:
        print(f"Error getting traffic data: {str(e)}")
        return None