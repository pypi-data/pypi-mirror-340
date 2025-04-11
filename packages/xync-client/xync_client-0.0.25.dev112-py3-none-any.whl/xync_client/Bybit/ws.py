import json

import websockets


async def prv(did: str, tok: str, ts: int, cb: callable):
    u = f"wss://ws2.bybit.com/private?appid=bybit&os=web&deviceid={did}&timestamp={ts}"
    async with websockets.connect(u) as websocket:
        auth_msg = json.dumps({"req_id": did, "op": "login", "args": [tok]})
        await websocket.send(auth_msg)

        sub_msg = json.dumps({"op": "subscribe", "args": ["FIAT_OTC_TOPIC", "FIAT_OTC_ONLINE_TOPIC"]})
        await websocket.send(sub_msg)
        sub_msg = json.dumps({"op": "input", "args": ["FIAT_OTC_TOPIC", '{"topic":"SUPER_DEAL"}']})
        await websocket.send(sub_msg)
        sub_msg = json.dumps({"op": "input", "args": ["FIAT_OTC_TOPIC", '{"topic":"OTC_ORDER_STATUS"}']})
        await websocket.send(sub_msg)
        sub_msg = json.dumps({"op": "input", "args": ["FIAT_OTC_TOPIC", '{"topic":"WEB_THREE_SELL"}']})
        await websocket.send(sub_msg)
        sub_msg = json.dumps({"op": "input", "args": ["FIAT_OTC_TOPIC", '{"topic":"APPEALED_CHANGE"}']})
        await websocket.send(sub_msg)

        sub_msg = json.dumps({"op": "subscribe", "args": ["fiat.cashier.order"]})
        await websocket.send(sub_msg)
        sub_msg = json.dumps({"op": "subscribe", "args": ["fiat.cashier.order-eftd-complete-privilege-event"]})
        await websocket.send(sub_msg)
        sub_msg = json.dumps({"op": "subscribe", "args": ["fiat.cashier.order-savings-product-event"]})
        await websocket.send(sub_msg)
        sub_msg = json.dumps({"op": "subscribe", "args": ["fiat.deal-core.order-savings-complete-event"]})
        await websocket.send(sub_msg)

        sub_msg = json.dumps({"op": "subscribe", "args": ["FIAT_OTC_TOPIC", "FIAT_OTC_ONLINE_TOPIC"]})
        await websocket.send(sub_msg)

        while resp := await websocket.recv():
            if data := json.loads(resp).get("data"):
                cb(data)
