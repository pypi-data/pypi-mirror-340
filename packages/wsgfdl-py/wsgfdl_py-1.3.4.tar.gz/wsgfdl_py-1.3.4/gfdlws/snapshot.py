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


def get(ws, exchange, symbol, periodicity, period,isShortIdentifiers):
    exg = exchange
    sym = symbol
    prc = periodicity
    prd = period
    iss = isShortIdentifiers
    rmsg = asyncio.get_event_loop().run_until_complete(mass_subscribe_n_stream(ws, exg, sym, prc, prd, iss))
    return rmsg


async def mass_subscribe_n_stream(ws, exg, sym, prc, prd, iss):
    try:
        # Format symbols as [{"Value": "symbol"}]
        instrument_identifiers = [{"Value": s} for s in sym.split(',')]

        # Prepare the request message as a dictionary
        req_msg = {
            "MessageType": "GetSnapshot",
            "Exchange": exg,
            "Periodicity": prc,
            "Period": prd,
            "isShortIdentifiers": iss,
            "InstrumentIdentifiers": instrument_identifiers
        }

        # Convert to JSON string for sending
        req_msg_str = json.dumps(req_msg)
        print("Request : " + req_msg_str)

        # Send the request message over the WebSocket
        await ws.send(req_msg_str)

        # Listen for the response message
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
            if rslt["MessageType"] == 'SnapshotResult':
                return message
        except websockets.ConnectionClosedOK:
            break
