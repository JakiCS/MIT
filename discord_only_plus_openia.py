from dotenv import load_dotenv
from openai import OpenAI  # Open IA Library
import discord
import os

# set openai api key
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Si no hay key, igual dejamos correr el bot (para que no explote al iniciar)
oa_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

# ask OpenAI - respond like a pirate
def call_openai(question):
    if oa_client is None:
        return "No tengo configurada la OPENAI_API_KEY, así que no puedo responder con IA por ahora."

    try:
        # Call the OpenAI API
        completion = oa_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": f"Respond like a pirate to the following question: {question}"
                },
            ]
        )
        # Print response (CORREGIDO)
        response = completion.choices[0].message.content
        print(response)
        return response

    except Exception as e:
        print(f"OpenAI error: {e}")
        return "Arrr! Tuve un problema consultando la IA. Probá de nuevo más tarde ☠️"

# Set up intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$question'):
        print(f"Message: {message.content}")
        message_content = message.content.split("$question")[1]
        print(f"Question: {message_content}")
        response = call_openai(message_content)
        print(f"Assistant: {response}")
        print("---")
        await message.channel.send(response)

client.run(os.getenv('TOKEN'))
