import configparser, quinnat, anyio, boto3
from semaphore import Bot, ChatContext

config = configparser.ConfigParser()
config.read('default.ini')

s3Url = config['S3']['s3Url']
s3AccessKey = config['S3']['s3AccessKey']
s3SecretKey = config['S3']['s3SecretKey']
s3Bucket = config['S3']['s3Bucket']
signalUsername = config['SIGNAL']['signalUsername']
signaldSocketPath = config['SIGNAL']['signaldSocketPath']
urbitUrl = config['URBIT']['urbitUrl']
urbitId = config['URBIT']['urbitId']
urbitCode = config['URBIT']['urbitCode']
urbitBridgeChat = config['URBIT']['urbitBridgeChat']
urbitHost = config['URBIT']['urbitHost']

s3Client = boto3.resource(
        service_name='s3',
        aws_access_key_id=s3AccessKey,
        aws_secret_access_key=s3SecretKey,
        endpoint_url=s3Url
)
signalClient = Bot(signalUsername)
urbitClient = quinnat.Quinnat(urbitUrl, urbitId, urbitCode)

@signalClient.handler('')
async def simpleRelay(ctx: ChatContext) -> None:
    if ctx.message.data_message.group and not ctx.message.data_message.attachments:
        urbitClient.post_message(urbitHost, urbitBridgeChat, {"text": f"{ctx.message.username} in group {ctx.message.data_message.group.name}: {ctx.message.get_body()}"})
    if ctx.message.data_message.group and ctx.message.data_message.attachments:
        s3Client.Bucket(s3Bucket).upload_file(Filename=ctx.message.data_message.attachments[0].stored_filename, Key=ctx.message.data_message.attachments[0].id)
        urbitClient.post_message(urbitHost, urbitBridgeChat, {"text": f"*{ctx.message.username} in group {ctx.message.data_message.group.name} sent an attachment.*"})
    if not ctx.message.data_message.group and not ctx.message.data_message.attachments:
        urbitClient.post_message(urbitHost, urbitBridgeChat, {"text": f"{ctx.message.username}: {ctx.message.get_body()}"})
    if not ctx.message.data_message.group and ctx.message.data_message.attachments:
        s3Client.Bucket(s3Bucket).upload_file(Filename=ctx.message.data_message.attachments[0].stored_filename, Key=ctx.message.data_message.attachments[0].id)
        urbitClient.post_message(urbitHost, urbitBridgeChat, {"text": f"*{ctx.message.username} sent an attachment.*"})

async def main():
    urbitClient.connect()
    async with signalClient:
        await signalClient.set_profile("marslinspike")
        await signalClient.start()

anyio.run(main)
