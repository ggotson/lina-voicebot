import os
import discord
import openai

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

client = discord.Client(intents=intents)

openai.api_key = os.getenv("OPENAI_API_KEY")
TOKEN = os.getenv("DISCORD_TOKEN")

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("!lina"):
        prompt = message.content[5:].strip()
        if not prompt:
            await message.channel.send("🎙️ 영어로 말하고 싶은 내용을 입력해주세요! 예: `!lina Hello, how are you?`")
            return

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "너는 친절한 영어 회화 튜터 Lina야. 사용자의 영어 표현을 도와주고, 자연스럽게 이어가는 역할을 해."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response['choices'][0]['message']['content']
        await message.channel.send(f"🗣️ {answer}")

client.run(TOKEN)
