import discord
import requests
import os

TOKEN = ""
WEBHOOK_URL = "https://skarphedinns.app.n8n.cloud/webhook/discord-agent"
ALLOWED_CHANNEL_ID = 1338861605336907879
# Enable all required intents
intents = discord.Intents.default()
intents.message_content = True  # This is required to read messages!
big = 266760086859415576

# Initialize bot with intents
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Ignore messages from itself

    if message.channel.id != ALLOWED_CHANNEL_ID:
        return  # Ignore messages from other channels

    if message.author.id == big:
        return
    
    print(f"📨 Received message: {message.content}")  # Debugging line

    # Send the message to n8n
    response = requests.post(WEBHOOK_URL, json={
        "message": message.content,
        "user": message.author.name
    })


    # Get the response from n8n and send it to Discord
    if response.status_code == 200:
        reply = response.json().get("response", "I didn't understand that.")
        print(f"📤 Sent message: {reply}")
        await message.channel.send(reply)
    else:
        print("⚠️ Error in n8n request:", response.text)

client.run(TOKEN)
