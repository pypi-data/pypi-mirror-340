import asyncio
import websockets
import json

url = None
key = None
exg = None
sym = None
msg = None
prc = None
prd = None
iss = None
printed_once = False

def get(ws, exchange, symbol, periodicity, period, unsubscribe =None):
    exg = exchange
    sym = symbol
    prc = periodicity
    prd = period
    uns =unsubscribe or "false"
    rmsg = asyncio.get_event_loop().run_until_complete(mass_subscribe_n_stream(ws, exg, sym, prc, prd ,uns))
    return rmsg


async def mass_subscribe_n_stream(ws, exg, sym, prc, prd,uns):
    global printed_once
    try:
        req_msg = str(
            '{"MessageType":"SubscribeSnapshot","Exchange":"' + exg + '","Periodicity":"' + prc + '","Period":' + f'{prd}' + ',"InstrumentIdentifier": "' + sym + '","unsubscribe": "' + uns + '"}')
        if not printed_once:
            print("Request : " + req_msg)
            printed_once = True
        await ws.send(req_msg)
        rmsg = await get_msg(ws)  # Listens for the tick data until market close
        return rmsg
    except:
        return msg


async def get_msg(ws):
    while True:
        try:
            message = await ws.recv()
            rslt = json.loads(message)
            if rslt["MessageType"] == 'RealtimeSnapshotResult':
                return message
        except websockets.ConnectionClosedOK:
            break