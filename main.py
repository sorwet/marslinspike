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
async def simpleRelay(ctx: ChatContext) -> None:
    print(ctx.message.data_message)
    if ctx.message.data_message.group:
        urbitClient.post_message(urbitHost, urbitBridgeChat, {"text": f"{ctx.message.username} in group {ctx.message.data_message.group.name}: {ctx.message.get_body()}"})
    else:
        urbitClient.post_message(urbitHost, urbitBridgeChat, {"text": f"{ctx.message.username}: {ctx.message.get_body()}"})

async def main():
    urbitClient.connect()
    async with signalClient:
        await signalClient.set_profile("marslinspike")
        await signalClient.start()

anyio.run(main)
