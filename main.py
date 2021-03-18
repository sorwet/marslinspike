import configparser, quinnat, anyio
from semaphore import Bot, ChatContext

config = configparser.ConfigParser()
config.read('default.ini')

signalUsername = config['SIGNAL']['signalUsername']
signaldSocketPath = config['SIGNAL']['signaldSocketPath']
urbitUrl = config['URBIT']['urbitUrl']
urbitId = config['URBIT']['urbitId']
urbitCode = config['URBIT']['urbitCode']
urbitBridgeChat = config['URBIT']['urbitBridgeChat']
urbitHost = config['URBIT']['urbitHost']

signalClient = Bot(signalUsername)
urbitClient = quinnat.Quinnat(urbitUrl, urbitId, urbitCode)

@signalClient.handler('')
async def echo(ctx: ChatContext) -> None:
    urbitClient.post_message(urbitHost, urbitBridgeChat, {"text": f"Got message: {ctx.message.get_body()}"})

async def main():
    urbitClient.connect()
    async with signalClient:
        await signalClient.set_profile("marslinspike ex bot")
        await signalClient.start()

anyio.run(main)
