"""
Check the estimated search traffic for any website. Try Ahrefs' free traffic checker.
"""

from typing import Optional, Dict, Any, Literal, List
import requests


def check_traffic(token: str, domain_or_url: str, mode: Literal["subdomains", "exact"] = "subdomains", country: str = "", protocol: str = "None") -> Optional[Dict[str, Any]]:
    """
    检查指定网站的预估搜索流量
    
    Args:
        domain_or_url (str): 要查询的域名或URL
        token (str): 验证令牌
        mode (str): 查询模式，默认为 "subdomains"
        country (str): 国家/地区，默认为 "None"
        protocol (str): 协议，默认为 "None"
    
    Returns:
        Optional[Dict[str, Any]]: 包含流量数据的字典，如果请求失败则返回 None
    """
    print(f"正在获取网站流量数据，域名: {domain_or_url}...")
    
    if not token:
        print("验证令牌获取失败")
        return None
    
    url = "https://ahrefs.com/v4/stGetFreeTrafficOverview"
    
    params = {
        "input": {
            "captcha": token,
            "country": country,
            "protocol": protocol,
            "mode": mode,
            "url": domain_or_url
        }
    }
    
    headers = {
        "accept": "*/*",
        "content-type": "application/json",
        "referer": f"https://ahrefs.com/traffic-checker/?input={domain}&mode={mode}"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code != 200:
            print(f"请求失败，状态码: {response.status_code}")
            print(response.text)
            return None
        
        data: Optional[List[Any]] = response.json()

        # 检查响应数据格式
        if not isinstance(data, list) or len(data) < 2 or data[0] != "Ok":
            print(f"响应数据格式不正确: {data}")
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
        
        print(f"成功获取 {domain_or_url} 的流量数据")
        return result
    except Exception as e:
        print(f"获取流量数据时出错: {str(e)}")
        return None