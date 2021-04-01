import configparser, quinnat, anyio, boto3
from semaphore import Bot, ChatContext

config = configparser.ConfigParser()
config.read('default.ini')

s3Url = config['S3']['s3Url']
s3AccessKey = config['S3']['s3AccessKey']
s3SecretKey = config['S3']['s3SecretKey']
s3Bucket = config['S3']['s3Bucket']
s3BucketUrl = s3Url + '/' + s3Bucket
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

def parseContentType(contentType):
    return contentType.split('/')[1]

def uploadAttachment(fileToUpload):
    s3Key = fileToUpload.id + '.' + parseContentType(fileToUpload.content_type)
    s3Client.Bucket(s3Bucket).upload_file(
        Filename = fileToUpload.stored_filename,
        Key = s3Key
    )
    s3AttachmentUrl = s3BucketUrl + '/' + s3Key
    return s3AttachmentUrl

@signalClient.handler('')
async def simpleRelay(ctx: ChatContext) -> None:

    if ctx.message.data_message.group and not ctx.message.data_message.attachments:
        urbitClient.post_message(urbitHost, urbitBridgeChat, {"text": f"{ctx.message.username} in group {ctx.message.data_message.group.name}: {ctx.message.get_body()}"})

    if ctx.message.data_message.group and ctx.message.data_message.attachments:
        if ctx.message.get_body():
            urbitClient.post_message(urbitHost, urbitBridgeChat, {"text": f"{ctx.message.username} in group {ctx.message.data_message.group.name}: {ctx.message.get_body()}"})
        for i in ctx.message.data_message.attachments:
            s3AttachmentUrl = uploadAttachment(i)
            urbitClient.post_message(urbitHost, urbitBridgeChat, {"text": f"{ctx.message.username} in group {ctx.message.data_message.group.name}:"})
            urbitClient.post_message(urbitHost, urbitBridgeChat, {"url": f"{s3AttachmentUrl}"})

    if not ctx.message.data_message.group and not ctx.message.data_message.attachments:
        urbitClient.post_message(urbitHost, urbitBridgeChat, {"text": f"{ctx.message.username}: {ctx.message.get_body()}"})

    if not ctx.message.data_message.group and ctx.message.data_message.attachments:
        if ctx.message.get_body():
            urbitClient.post_message(urbitHost, urbitBridgeChat, {"text": f"{ctx.message.username}: {ctx.message.get_body()}"})
        for i in ctx.message.data_message.attachments:
            s3AttachmentUrl = uploadAttachment(i)
            urbitClient.post_message(urbitHost, urbitBridgeChat, {"text": f"{ctx.message.username}:"})
            urbitClient.post_message(urbitHost, urbitBridgeChat, {"url": f"{s3AttachmentUrl}"})

async def main():
    urbitClient.connect()
    async with signalClient:
        await signalClient.set_profile("marslinspike")
        await signalClient.start()

anyio.run(main)
