import aiohttp
import json

async def fetch_status():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.jailbreaks.app/status') as resp:
            if resp.status == 200:
                return json.loads(await resp.text())
            else:
                return None