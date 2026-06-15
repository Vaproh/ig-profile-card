import logging
import random
from typing import Any, Dict, Optional

from curl_cffi import requests as cffi_requests

logger = logging.getLogger(__name__)

API_URL = "https://i.instagram.com/api/v1/users/web_profile_info/?username={}"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]


def build_headers(user_agent: str = None) -> Dict[str, str]:
    if user_agent is None:
        user_agent = random.choice(USER_AGENTS)
    return {
        "User-Agent": user_agent,
        "x-ig-app-id": "936619743392459",
        "Accept": "*/*",
        "Accept-Language": "en-US",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }


def fetch_profile(username: str, proxy_url: str = None) -> Dict[str, Any]:
    url = API_URL.format(username)
    headers = build_headers()

    try:
        resp = cffi_requests.get(
            url,
            headers=headers,
            timeout=15,
            proxies={"https": proxy_url, "http": proxy_url} if proxy_url else None,
            impersonate="chrome",
        )

        if resp.status_code == 404:
            return {"status": "missing", "error": "Profile not found"}

        if resp.status_code == 429:
            return {"status": "rate_limited", "error": "Rate limited by Instagram"}

        if resp.status_code != 200:
            return {"status": "error", "error": f"HTTP {resp.status_code}"}

        data = resp.json()

        user = data.get("data", {}).get("user")
        if not user:
            return {"status": "missing", "error": "User data not found in response"}

        return {
            "status": "ok",
            "username": user.get("username", username),
            "full_name": user.get("full_name", ""),
            "bio": user.get("biography", ""),
            "followers": user.get("edge_followed_by", {}).get("count", 0),
            "following": user.get("edge_follow", {}).get("count", 0),
            "posts": user.get("edge_owner_to_timeline_media", {}).get("count", 0),
            "is_private": user.get("is_private", False),
            "is_verified": user.get("is_verified", False),
            "profile_pic_url": user.get("profile_pic_url_hd", user.get("profile_pic_url", "")),
            "external_url": user.get("external_url", ""),
        }

    except Exception as e:
        logger.error(f"Error fetching profile {username}: {e}")
        return {"status": "error", "error": str(e)}