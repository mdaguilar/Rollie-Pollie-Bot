import os
import discord
import random
import requests
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
print("running")


@bot.command(name="roll", help="Simuates a die roll depending on the number of sides you enter. You can also enter how many of that die you'd like to roll.")
async def roll(ctx, numSides, numToRoll=1):
    print("COMMAND: roll")
    try:
        numSidesInt = int(numSides.strip('d'))
        dice = [random.choice(range(1, numSidesInt+1)) for _ in range(numToRoll)]
        dice_str = ", ".join([str(d) for d in dice])
        result = f"**Rolling a {numSides} die {numToRoll} times...**\n> Results: {dice_str}\n> Total: {sum(dice)}"
        await ctx.send(result)
    except Exception as e:
        print(f"Error: {e}")

@bot.command(name="alignment", help="Get info on the different alignments by entering its abreviation.")
async def roll(ctx, alignmentAbbreviation=""):
    print("COMMAND: alignment")
    if alignmentAbbreviation == "":
        await ctx.send("**Choose from the following abreviations**: LG, NG, CG, LN, N, CN, LE, NE, CE")

    alignmentAbbreviation = alignmentAbbreviation.upper()
    indexConversion = {
        "LG":"lawful-good", "NG":"neutral-good", "CG":"chaotic-good",
        "LN":"lawful-neutral", "N":"neutral", "CN":"chaotic-neutral",
        "LE":"lawful-evil", "NE":"neutral-evil", "CE":"chaotic-evil",
        }
        
    try:
        response = requests.get(f"https://www.dnd5eapi.co/api/alignments/{indexConversion[alignmentAbbreviation]}")
        result = f'**Alignment: {response.json()["name"]}**\n> {response.json()["desc"]}'
        await ctx.send(result)
    except Exception as e:
        print(f"Error: {e}")

bot.run(TOKEN)
