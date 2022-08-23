import discord 
import responses

common_prefix = "/"
private_prefix = "?"
prefixes = [common_prefix, private_prefix]

async def send_message(message, user_message, is_private):
    #try:
    response = responses.handle_response(user_message)
    if response == None or response == "":
        return
    await message.author.send(response) if is_private else await message.channel.send(response)
    #except Exception as e:
    #    print(e)

def run_discord_bot():
    token = open("token").read()
    intents = discord.Intents.default()
    #intents.members = True
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        user_message = str(message.content)
        if user_message[0] not in prefixes:
            return
        if user_message[0] == private_prefix:
            await send_message(message, user_message[1:], is_private=True)
        else:
            await send_message(message, user_message[1:], is_private=False)
    client.run(token)

