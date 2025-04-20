import aiohttp
import asyncio


async def get_shortened_url(url_to_shorten: str, base_url: str) -> tuple[int, dict[str, str | int]]:
    async with aiohttp.ClientSession() as session:
        response = await session.post(base_url, json={"url": url_to_shorten})
        if response.status not in {200, 201}:
            raise Exception(f"Error: {response.status}")
        result = await response.json()
        return response.status, {"id": result["id"], "short_url": result["short_url"]}


async def get_original_url(base_url: str, url_id: int) -> tuple[int, dict[str, str | int]]:
    async with aiohttp.ClientSession() as session:
        response = await session.get(f"{base_url}/{url_id}")
        if response.status not in {200, 201, 307}:
            raise Exception(f"Error: {response.status}")
        return response.status, {"original_url": str(response.url)}


if __name__ == "__main__":
    print(asyncio.run(get_shortened_url("https://google.com", "http://localhost:8080")))
    print(asyncio.run(get_original_url("http://localhost:8080", 3)))