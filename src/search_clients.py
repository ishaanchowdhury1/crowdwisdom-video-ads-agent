import requests
from datetime import datetime, timedelta, timezone
from .config import settings


def tavily_search(query: str, days: int = 30, max_results: int = 8):
    if not settings.tavily_api_key:
        raise RuntimeError("TAVILY_API_KEY is missing")
    start = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    payload = {"api_key": settings.tavily_api_key, "query": query, "search_depth": "advanced", "max_results": max_results, "topic": "news", "time_range": "month"}
    r = requests.post("https://api.tavily.com/search", json=payload, timeout=45)
    r.raise_for_status()
    return {"from_date": start, "query": query, "results": r.json().get("results", [])}


def exa_search(query: str, days: int = 30, max_results: int = 8):
    if not settings.exa_api_key:
        raise RuntimeError("EXA_API_KEY is missing")
    start = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    payload = {"query": query, "type": "auto", "numResults": max_results, "startPublishedDate": start, "contents": {"highlights": {"maxCharacters": 1200}}}
    r = requests.post("https://api.exa.ai/search", headers={"x-api-key": settings.exa_api_key, "Content-Type": "application/json"}, json=payload, timeout=45)
    r.raise_for_status()
    return {"from_date": start, "query": query, "results": r.json().get("results", [])}
