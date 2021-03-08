import asyncio, configparser, quinnat
from pysignald_async.api import JsonAddressv1, JsonMessageEnvelopev1

config = configparser.ConfigParser()
config.read('default.ini')

signalUsername = config['Signal']['signalUsername']
signaldSocketPath = config['Signal']['signaldSocketPath']
urbitUrl = config['Urbit']['urbitUrl']
urbitId = config['Urbit']['urbitId']
urbitCode = config['Urbit']['urbitCode']
urbitBridgeChat = config['Urbit']['urbitBridgeChat']

urbitClient = Quinnat(urbitUrl, urbitId, urbitCode)


class RelayBot(SignaldAPI):

    def handle_envelope(self, payload):

        message = envelope.dataMessage
        source = envelope.source.number

        if message is not None and source is not None:
            username = envelope.username
            asyncio.create_task(
                    urbitClient.post_message(
                        urbitHost, 
                        urbitBridgeChat, 
                        {
                            "text": "Got message from {source}: {message.body}"
                        }
                    )
            )

async def main():
    urbitClient.connect()

    loop = asyncio.get_running_loop()
    _, signald = await loop.create_unix_connection(SignaldAPI, path=signaldSocketPath)
    await signald.subscribe(username=signalUsername)

asyncio.run(main())
