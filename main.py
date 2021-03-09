import configparser, quinnat

config = configparser.ConfigParser()
config.read('default.ini')

signalUsername = config['SIGNAL']['signalUsername']
signaldSocketPath = config['SIGNAL']['signaldSocketPath']
urbitUrl = config['URBIT']['urbitUrl']
urbitId = config['URBIT']['urbitId']
urbitCode = config['URBIT']['urbitCode']
urbitBridgeChat = config['URBIT']['urbitBridgeChat']
urbitHost = config['URBIT']['urbitHost']

urbitClient = quinnat.Quinnat(urbitUrl, urbitId, urbitCode)
print(f"connecting to ship {urbitId} @ {urbitUrl}")
urbitClient.connect()
print(f"connected to ship {urbitId}.")

urbitClient.post_message(urbitHost, urbitBridgeChat, {"text": ctx.message.get_body()})
