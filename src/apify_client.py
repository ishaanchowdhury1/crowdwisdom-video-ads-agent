"""Small deterministic Apify REST adapter.

Hermes is still the orchestrator. This adapter is only responsible for executing an
Actor when a Hermes profile decides which Actor/input to use.
"""
import requests
from .config import settings

APIFY_API = "https://api.apify.com/v2"


def start_actor(actor_id: str, run_input: dict, timeout_s: int = 180):
    if not settings.apify_api_token:
        raise RuntimeError("APIFY_API_TOKEN is missing")
    url = f"{APIFY_API}/acts/{actor_id.replace('/', '~')}/runs"
    r = requests.post(url, params={"token": settings.apify_api_token}, json=run_input, timeout=30)
    r.raise_for_status()
    run = r.json()["data"]
    run_id = run["id"]
    dataset_id = run["defaultDatasetId"]
    # Poll the run.
    import time
    for _ in range(max(1, timeout_s // 3)):
        s = requests.get(f"{APIFY_API}/actor-runs/{run_id}", params={"token": settings.apify_api_token}, timeout=30)
        s.raise_for_status()
        status = s.json()["data"]["status"]
        if status in {"SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"}:
            break
        time.sleep(3)
    if status != "SUCCEEDED":
        raise RuntimeError(f"Apify run ended with status={status}")
    items = requests.get(f"{APIFY_API}/datasets/{dataset_id}/items", params={"token": settings.apify_api_token, "format": "json", "clean": "true"}, timeout=60)
    items.raise_for_status()
    return items.json()
