import asyncio, configparser, quinnat

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
print("Quinnat initialised. Connecting to ship {} @ {} ...".format(urbitId, urbitUrl))

urbitClient.connect()
print("Connected to ship {}.".format(urbitId))
print("Posting message in {}...".format(urbitBridgeChat))
urbitClient.post_message(urbitHost, urbitBridgeChat, {"text": "Sending test message."})
