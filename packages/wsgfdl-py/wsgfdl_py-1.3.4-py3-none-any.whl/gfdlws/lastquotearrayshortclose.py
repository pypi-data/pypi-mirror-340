import asyncio
import websockets
import json

exg = None
sym = None
msg = None
isi = None


def get(ws, exchange, symbols,isShortIdentifiers):
    exg = exchange
    sym = symbols
    isi = isShortIdentifiers
    rmsg = asyncio.get_event_loop().run_until_complete(mass_subscribe_n_stream(ws, exg, sym, isi))
    return rmsg


async def mass_subscribe_n_stream(ws, exg, sym, isi):
    try:
        instrument_identifiers = [{"Value": s} for s in sym.split(',')]

        req_msg = {
            "MessageType": "GetLastQuoteArrayShortWithClose",
            "Exchange": exg,
            "isShortIdentifiers": isi,
            "InstrumentIdentifiers": instrument_identifiers
        }
        req_msg_str = json.dumps(req_msg)
        print("Request : " + req_msg_str)
        await ws.send(req_msg_str)
        rmsg = await get_msg(ws)
        return rmsg
    except Exception as e:
        print(f"An error occurred: {e}")
        return msg


async def get_msg(ws):
    while True:
        try:
            message = await ws.recv()
            rslt = json.loads(message)
            if rslt["MessageType"] == 'LastQuoteArrayShortWithCloseResult':
                return message
        except websockets.ConnectionClosedOK:
            break