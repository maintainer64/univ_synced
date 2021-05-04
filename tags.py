import aiohttp
import asyncio
import os


async def load_latest_version(transport):
    u = os.getenv("CIRCLE_PROJECT_USERNAME")
    r = os.getenv("CIRCLE_PROJECT_REPONAME")
    print("URL:", f"https://api.github.com/repos/{u}/{r}/releases/latest")
    async with transport.get(f"https://api.github.com/repos/{u}/{r}/releases/latest") as resp:
        data = await resp.json()
        print("data:", data)
        return data["tag_name"]


async def upper_version(version: str) -> str:
    digits = list(map(int, version.strip("v").split(".")))
    assert len(digits) == 3
    digits[-1] += 1
    return f"v{digits[0]}.{digits[1]}.{digits[2]}"


async def publish_new_version(
    transport, version,
):
    u = os.getenv("CIRCLE_PROJECT_USERNAME")
    r = os.getenv("CIRCLE_PROJECT_REPONAME")
    async with transport.post(
        f"https://api.github.com/repos/{u}/{r}/releases",
        headers={"Accept": "application/vnd.github.v3+json"},
        json={"tag_name": version},
    ) as resp:
        assert resp.status == 201


async def create_tag_new_version():
    u = os.getenv("CIRCLE_PROJECT_USERNAME")
    token = os.getenv("GH_TOKEN")
    async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(login=u, password=token)) as session:
        last_version = await load_latest_version(transport=session)
        new_version = await upper_version(version=last_version)
        await publish_new_version(transport=session, version=new_version)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_tag_new_version())
    loop.close()
