# import asyncio
# import websockets
# import json
#
# url = None
# key = None
# exg = None
# sym = None
# msg = None
# prc = None
# prd = None
# frm = None
# to = None
# iss = None
# rno = None
# utg = None
#
#
# def getbyperiod(ws, exchange, InstrumentIdentifier, periodicity, period, fromtime, totime, usertag, isShortIdentifiers):
#     if exchange is None:
#         return "Exchange is mandatory."
#     else:
#         exg = exchange
#
#     if InstrumentIdentifier is None:
#         return "InstrumentIdentifier / Symbol is mandatory."
#     else:
#         sym = InstrumentIdentifier
#
#     if periodicity is None:
#         prc = 'MINUTE'
#     else:
#         prc = periodicity
#
#     if period is None:
#         prd = '1'
#     else:
#         prd = period
#
#     rmsg = asyncio.get_event_loop().run_until_complete(
#         mass_subscribe_n_streamft(ws, exg, sym, prc, prd, fromtime, totime, isShortIdentifiers, usertag))
#     return rmsg
#
#
# def getcaldle(ws, exchange, InstrumentIdentifier, periodicity, period, max, usertag, isShortIdentifiers):
#     if exchange is None:
#         return "Exchange is mandatory."
#     else:
#         exg = exchange
#
#     if InstrumentIdentifier is None:
#         return "Symbol is mandatory."
#     else:
#         sym = InstrumentIdentifier
#
#     if periodicity is None:
#         prc = 'MINUTE'
#     else:
#         prc = periodicity
#
#     if period is None:
#         prd = '1'
#     else:
#         prd = period
#
#     if max is None:
#         rno = max
#     else:
#         rno = 10
#
#     if isShortIdentifiers == "":
#         iss = 'false'
#     else:
#         iss = isShortIdentifiers
#
#     if usertag is None:
#         utg = ''
#     else:
#         utg = usertag
#
#     rmsg = asyncio.get_event_loop().run_until_complete(
#         mass_subscribe_n_stream(ws, exg, sym, prc, prd, iss, rno, utg))
#     return rmsg
#
#
# async def mass_subscribe_n_streamft(ws, exg, sym, prc, prd, frm, to, iss, utg):
#     try:
#         if iss != "" and utg != "":
#             req_msg = '{"MessageType":"GetHistory","Exchange":"' + exg + '","InstrumentIdentifier":"' + sym + '","Periodicity":"' + prc + '","Period":' + str(
#                 prd) + ',"From":"' + str(frm) + '","To":"' + str(to) + '","isShortIdentifier":"' + iss + '","UserTag":"' + utg + '"}'
#         elif iss == "" and utg != "":
#             req_msg = '{"MessageType":"GetHistory","Exchange":"' + exg + '","InstrumentIdentifier":"' + sym + '","Periodicity":"' + prc + '","Period":' + str(
#                 prd) + ',"From":"' + str(frm) + '","To":"' + str(to) + '","isShortIdentifier":"false","UserTag":"' + utg + '"}'
#         elif iss == "" and utg == "":
#             req_msg = '{"MessageType":"GetHistory","Exchange":"' + exg + '","InstrumentIdentifier":"' + sym + '","Periodicity":"' + prc + '","Period":' + str(
#                 prd) + ',"From":"' + str(frm) + '","To":"' + str(to) + '","isShortIdentifier":"false"}'
#         elif iss != "" and utg == "":
#             req_msg = '{"MessageType":"GetHistory","Exchange":"' + exg + '","InstrumentIdentifier":"' + sym + '","Periodicity":"' + prc + '","Period":' + str(
#                 prd) + ',"From":"' + str(frm) + '","To":"' + str(to) + '","isShortIdentifier":"' + iss + '"}'
#         await ws.send(req_msg)
#         print("Request : " + req_msg)
#         rmsg = await get_msg(ws)
#         return rmsg
#     except:
#         return msg
#
#
# async def mass_subscribe_n_stream(ws, exg, sym, prc, prd, iss, rno, utg):
#     req_msg = None
#     try:
#         if iss != "" and utg != "":
#             req_msg = '{"MessageType":"GetHistory","Exchange":"' + exg + '","InstrumentIdentifier":"' + sym + '","Periodicity":"' + prc + '","Period":' + str(
#                 prd) + ',"Max":' + str(rno) + ',"isShortIdentifier":"' + iss + '","UserTag":"' + utg + '"} '
#         elif iss != "" and utg == "":
#             req_msg = '{"MessageType":"GetHistory","Exchange":"' + exg + '","InstrumentIdentifier":"' + sym + '","Periodicity":"' + prc + '","Period":' + str(
#                 prd) + ',"Max":' + str(rno) + ',"isShortIdentifier":"' + iss + '"}'
#         elif iss == "" and utg == "":
#             req_msg = '{"MessageType":"GetHistory","Exchange":"' + exg + '","InstrumentIdentifier":"' + sym + '","Periodicity":"' + prc + '","Period":' + str(
#                 prd) + ',"Max":' + str(rno) + ',"isShortIdentifier":"false"' + '"}'
#         elif iss == "" and utg != "":
#             req_msg = '{"MessageType":"GetHistory","Exchange":"' + exg + '","InstrumentIdentifier":"' + sym + '","Periodicity":"' + prc + '","Period":' + str(
#                 prd) + ',"Max":' + str(rno) + ',"isShortIdentifier":"false"' + '","UserTag":"' + utg + '"}'
#         await ws.send(str(req_msg))
#         print("Request : " + req_msg)
#         rmsg = await get_msg(ws)
#         return rmsg
#     except:
#         return "Exception : " + str(msg)
#
#
# async def get_msg(ws):
#     while True:
#         try:
#             message = await ws.recv()
#             rslt = json.loads(message)
#             if rslt["MessageType"] == 'HistoryOHLCResult' or rslt["MessageType"] == 'HistoryTickResult':
#                 return message
#         except websockets.ConnectionClosedOK:
#             break
#         # print(message)

import asyncio
import websockets
import json

# Function to get messages from WebSocket
async def get_msg(ws):
    while True:
        try:
            message = await ws.recv()
            rslt = json.loads(message)
            if rslt["MessageType"] == 'HistoryOHLCResult' or rslt["MessageType"] == 'HistoryTickResult':
                return message
        except websockets.ConnectionClosedOK:
            break


# Function to request historical data with from-time and to-time
async def mass_subscribe_n_streamft(ws, exg, sym, prc, prd, frm, to,max, iss, utg):
    req_msg = {
        "MessageType": "GetHistory",
        "Exchange": exg,
        "InstrumentIdentifier": sym,
        "Periodicity": prc,
        "Period": prd,
        "From": frm ,
        "To": to ,
        "Max":max if max else 0,
        "isShortIdentifier": iss if iss else "false",
        "UserTag": utg if utg else ""

    }
    await ws.send(json.dumps(req_msg))
    print(req_msg)
    return await get_msg(ws)


# Function to request historical data with a limit on maximum records
async def mass_subscribe_n_stream(ws, exg, sym, prc, prd, iss, rno, utg):
    req_msg = {
        "MessageType": "GetHistory",
        "Exchange": exg,
        "InstrumentIdentifier": sym,
        "Periodicity": prc,
        "Period": prd,
        "Max": rno,
        "isShortIdentifier": iss if iss else "false",
        "UserTag": utg if utg else ""
    }
    await ws.send(json.dumps(req_msg))
    print(req_msg)
    return await get_msg(ws)

async def mass_subscribe_n_streamad(ws, exg, sym, prc, prd,frm,to,adj, iss, rno, utg):
    req_msg = {
        "MessageType": "GetHistory",
        "Exchange": exg,
        "InstrumentIdentifier": sym,
        "Periodicity": prc,
        "Period": prd,
        "From": frm,
        "To": to,
        "AdjustSplits":adj,
        "Max": rno,
        "isShortIdentifier": iss if iss else "false",
        "UserTag": utg if utg else ""
    }
    await ws.send(json.dumps(req_msg))
    print(req_msg)
    return await get_msg(ws)


# Wrapper function to call mass_subscribe_n_streamft based on period range
def getbyperiod(ws, exchange, InstrumentIdentifier, periodicity, period, fromtime, totime, usertag, isShortIdentifiers):
    exg = exchange
    sym = InstrumentIdentifier
    prc = periodicity or 'MINUTE'
    prd = period or 1
    iss = isShortIdentifiers or 'false'
    utg = usertag or ''

    return asyncio.get_event_loop().run_until_complete(
        mass_subscribe_n_streamft(ws, exg, sym, prc, prd, fromtime, totime, iss, utg))


# Wrapper function to call mass_subscribe_n_stream for maximum records
def getcaldle(ws, exchange, InstrumentIdentifier, periodicity, period, max, usertag, isShortIdentifiers):
    exg = exchange
    sym = InstrumentIdentifier
    prc = periodicity or 'MINUTE'
    prd = period or 1
    rno = max or 10
    iss = isShortIdentifiers or 'false'
    utg = usertag or ''

    return asyncio.get_event_loop().run_until_complete(
        mass_subscribe_n_stream(ws, exg, sym, prc, prd, iss, rno, utg))

# Wrapper function to call mass_subscribe_n_stream for maximum records
def getadjusted(ws, exchange, InstrumentIdentifier, periodicity, period,fromtime, totime, max, AdjustSplits, usertag, isShortIdentifiers):
    exg = exchange
    sym = InstrumentIdentifier
    prc = periodicity or 'MINUTE'
    prd = period or 1
    rno = max or 10
    iss = isShortIdentifiers or 'false'
    utg = usertag or ''

    return asyncio.get_event_loop().run_until_complete(
        mass_subscribe_n_streamad(ws, exg, sym, prc, prd,fromtime, totime,AdjustSplits, iss, rno, utg))
