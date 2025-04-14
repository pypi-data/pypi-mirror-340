
import requests
import websockets
import asyncio
import json

class SpreadClient:
    def __init__(self, ws_url="ws://localhost:8765", rest_url="http://localhost:5099"):
        self.ws_url = ws_url
        self.rest_url = rest_url

    async def subscribe(self, symbols, on_message):
        async with websockets.connect(self.ws_url) as ws:
            await ws.send(json.dumps({
                "method": "SUBSCRIBE",
                "params": [f"{s}@bpspread" for s in symbols],
                "id": 1
            }))
            async for msg in ws:
                data = json.loads(msg)
                await on_message(data)

    def get_spread_rest(self, symbols=[], market_type="um"):
        params = {}
        if symbols:
            params["symbols"] = ",".join(symbols)
        if market_type:
            params["type"] = market_type
        resp = requests.get(f"{self.rest_url}/api/spread", params=params)
        return resp.json()

    def download_spread_file(self, symbol, date, market_type="um"):
        params = {
            "symbol": symbol,
            "date": date,
            "type": market_type
        }
        resp = requests.get(f"{self.rest_url}/api/spread/download", params=params)
        return resp.json()
