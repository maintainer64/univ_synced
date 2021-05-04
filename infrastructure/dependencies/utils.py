from aiohttp import ClientSession, TCPConnector


async def session_maker() -> ClientSession:
    return ClientSession(connector=TCPConnector(ssl=True), headers={"Content-Type": "application/json"},)
