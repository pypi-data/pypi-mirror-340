# import asyncio
# import websockets
# import json
#
# exg = None
# sym = None
# msg = None
# isi = None
#
#
# def get(ws, exchange, symbols,isShortIdentifiers):
#     exg = exchange
#     sym = symbols
#     isi = isShortIdentifiers
#     rmsg = asyncio.get_event_loop().run_until_complete(mass_subscribe_n_stream(ws, exg, sym, isi))
#     return rmsg
#
#
# async def mass_subscribe_n_stream(ws, exg, sym, isi):
#     try:
#         req_msg = str('{"MessageType":"GetLastQuoteArray","Exchange":"' + exg + '","isShortIdentifiers":"' + isi + '","InstrumentIdentifiers":' + str(sym) + '}')
#         print("Request : " + req_msg)
#         await ws.send(req_msg)
#         rmsg = await get_msg(ws)
#         return rmsg
#     except:
#         return msg
#
#
# async def get_msg(ws):
#     while True:
#         try:
#             message = await ws.recv()
#             rslt = json.loads(message)
#             if rslt["MessageType"] == 'LastQuoteArrayResult':
#                 return message
#         except websockets.ConnectionClosedOK:
#             break
#         print(message)
import asyncio
import websockets
import json

exg = None
sym = None
msg = None
isi = None


def get(ws, exchange, symbols, isShortIdentifiers):
    exg = exchange
    sym = symbols
    isi = isShortIdentifiers
    rmsg = asyncio.get_event_loop().run_until_complete(mass_subscribe_n_stream(ws, exg, sym, isi))
    return rmsg


async def mass_subscribe_n_stream(ws, exg, sym, isi):
    try:
        # Prepare the symbol list as [{"Value": "SYMBOL"}]
        instrument_identifiers = [{"Value": s} for s in sym.split(',')]

        # Construct the request message
        req_msg = {
            "MessageType": "GetLastQuoteArray",
            "Exchange": exg,
            "isShortIdentifiers": isi,
            "InstrumentIdentifiers": instrument_identifiers
        }

        # Convert to JSON string for sending
        req_msg_str = json.dumps(req_msg)
        print("Request : " + req_msg_str)

        # Send the request message over the WebSocket
        await ws.send(req_msg_str)

        # Receive and return the response message
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
            if rslt["MessageType"] == 'LastQuoteArrayResult':
                return message
        except websockets.ConnectionClosedOK:
            break
        print(message)



