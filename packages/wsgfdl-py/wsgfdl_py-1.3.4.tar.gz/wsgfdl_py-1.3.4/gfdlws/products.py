# import asyncio
# import websockets
# import json
# url = None
# key = None
# exg = None
# ist = None
#
#
# def get(ws,Exchange, InstrumentType=None):
#     exg = Exchange
#     ist = InstrumentType
#     rmsg = asyncio.get_event_loop().run_until_complete(mass_subscribe_n_stream(ws, exg, ist))
#     return rmsg
#
#
# async def mass_subscribe_n_stream(ws, exg, ist):
#     try:
#         req_msg = '{"MessageType":"GetProducts","Exchange":"' + exg
#         if ist is not None:
#             req_msg = req_msg + '",InstrumentType":"' + ist
#
#         req_msg = str(req_msg + '"}')
#         print("Request : " + req_msg)
#         await ws.send(req_msg)
#         rmsg = await get_msg(ws)
#         return rmsg
#     except:
#         return "Error"
#
#
# async def get_msg(ws):
#     while True:
#         try:
#             message = await ws.recv()
#             rslt = json.loads(message)
#             if rslt.get["MessageType"] == 'ProductsResult':
#                 return message
#         except websockets.ConnectionClosedOK:
#             break


import asyncio
import websockets
import json

# Define variables
url = None
key = None
exg = None
ist = None

# Function to get the message from the WebSocket
def get(ws, Exchange, InstrumentType=None):
    exg = Exchange
    ist = InstrumentType
    # Use asyncio to run the async mass_subscribe_n_stream function synchronously
    rmsg = asyncio.get_event_loop().run_until_complete(mass_subscribe_n_stream(ws, exg, ist))
    return rmsg

# Async function to send request and handle response
async def mass_subscribe_n_stream(ws, exg, ist):
    try:
        # Create request message as a dictionary
        req_msg = {
            "MessageType": "GetProducts",
            "Exchange": exg
        }

        # Add InstrumentType if it's provided
        if ist is not None:
            req_msg["InstrumentType"] = ist

        # Convert dictionary to JSON string
        req_msg_str = json.dumps(req_msg)
        print(f"Request: {req_msg_str}")

        # Send the request message to the WebSocket
        await ws.send(req_msg_str)

        # Await the response message from the WebSocket
        rmsg = await get_msg(ws)
        return rmsg

    except Exception as e:
        # Print and return an error message if an exception occurs
        print(f"Error occurred: {e}")
        return "Error"

# Async function to receive and process WebSocket messages
async def get_msg(ws):
    while True:
        try:
            # Wait for message from the WebSocket
            message = await ws.recv()

            # Parse the message as JSON
            rslt = json.loads(message)

            # Check for the 'ProductsResult' message type and return it
            if rslt.get("MessageType") == 'ProductsResult':
                return message

        # Break the loop when the connection is closed
        except websockets.ConnectionClosedOK:
            break
