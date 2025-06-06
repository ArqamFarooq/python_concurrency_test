import asyncio
import json
import time
import httpx
from statistics import mean
from typing import List, Dict

async def fetch_url(client: httpx.AsyncClient, url: str, retries: int = 2) -> Dict:
    for attempt in range(retries + 1):
        start_time = time.time()
        try:
            response = await client.get(url, timeout=10)
            response.raise_for_status()
            return {"url": url, "status": response.status_code, "time": time.time() - start_time}
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            if attempt == retries:
                return {"url": url, "status": "failed", "time": time.time() - start_time, "error": str(e)}
            await asyncio.sleep(0.5)

async def main():
    # Read URLs from JSON file
    try:
        with open("urls.json", "r") as f:
            urls = json.load(f)["urls"]
    except FileNotFoundError:
        print("urls.json not found")
        return

    start_time = time.time()
    async with httpx.AsyncClient() as client:
        tasks = [fetch_url(client, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    total_time = time.time() - start_time
    successful = [r for r in results if r["status"] != "failed"]
    response_times = [r["time"] for r in successful]

    print("Summary Statistics:")
    print(f"Total URLs: {len(urls)}")
    print(f"Successful responses: {len(successful)}")
    print(f"Total time taken: {total_time:.2f} seconds")
    print(f"Fastest response: {min(response_times):.2f} seconds" if response_times else "N/A")
    print(f"Slowest response: {max(response_times):.2f} seconds" if response_times else "N/A")
    print(f"Average response time: {mean(response_times):.2f} seconds" if response_times else "N/A")
    for result in results:
        if result["status"] == "failed":
            print(f"Failed: {result['url']} - {result['error']}")

if __name__ == "__main__":
    asyncio.run(main())