import asyncio
import websockets
import json

exg = None
tkn = None
msg = None
isi = None


def get(ws, exchange, token):
    exg = exchange
    tkn = token
    rmsg = asyncio.get_event_loop().run_until_complete(mass_subscribe_n_stream(ws, exg, tkn))
    return rmsg


async def mass_subscribe_n_stream(ws, exg, tkn):
    try:
        token = [{"Value": s} for s in tkn.split(',')]

        req_msg = {
            "MessageType": "GetLastQuoteArrayOptionGreeks",
            "Exchange": exg,
            "Tokens": token
        }
        req_msg_str = json.dumps(req_msg)
        print("Request : " + req_msg_str)
        await ws.send(req_msg_str)
        rmsg = await get_msg(ws)
        return rmsg
    except:
        return msg


async def get_msg(ws):
    while True:
        try:
            message = await ws.recv()
            rslt = json.loads(message)
            if rslt["MessageType"] == 'LastQuoteArrayOptionGreeksResult':
                return message
        except websockets.ConnectionClosedOK:
            break
        print(message)
