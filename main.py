import asyncio, quinnat, configparser
from mausignald import SignaldClient
from mausignald.types import Message

config = configparser.ConfigParser()
config.read('default.ini')

signalUsername = config['signalUsername']
urbitUrl = config['urbitUrl']
urbitId = config['urbitId']
urbitCode = config['urbitCode']

urbitClient = quinnat.Quinnat(urbitUrl, urbitId, urbitCode)
signalClient = SignaldClient()

async def qr_callback(uri: str) -> None:
    import os
    os.system(f"qrencode -t ansiutf8 '{uri}'")

async def handle_message(message: Message) -> None:

    urbitClient.post_message(urbitHost, urbitBridgeChat, {"text": "Got message: {message}"})

async def main():

    signalClient.add_event_handler(Message, handle_message)
    await signalClient.connect()
    await urbitClient.connect()

    await signalClient.link(qr_callback)
        await signalClient.subscribe(signal_username)

    loop = asynchio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_forever()
