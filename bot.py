import os
import discord
import random
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all(), help_command=None)
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


@bot.command(name="class", help="Get info on the different classes you can choose to play as by entering its name.")
async def classInfo(ctx, className=""):
    print("COMMAND: class")
    classes = ["artificer", "barbarian", "bard", "cleric", "druid", "fighter", "monk", "paladin", "ranger", "rogue", "sorcerer", "warlock", "wizard"]
    if className == "" or className.lower() not in classes:
            await ctx.send("**Choose from the following classes**:\n> Artificer\n> Barbarian\n> Bard\n> Cleric\n> Druid\n> Fighter\n> Monk\n> Paladin\n> Ranger\n> Rogue\n> Sorcerer\n> Warlock\n> Wizard")

    else:
        className = className.lower()
        url = f"http://dnd5e.wikidot.com/{className}"
        try:
            response = requests.get(url)
            html_data = response.text
            soup = BeautifulSoup(html_data, "html.parser")
            info = soup.find_all(name='em')
            result = f'**Class: {className.title()}**:\n> {info[0].text.strip("<em>/")}\n> *Learn more: {url} *'
            await ctx.send(result)
        except Exception as e:
            print(f"Error: {e}")


@bot.command(name="ability", help="Get info about what each abilitiy score means.")
async def asInfo(ctx, ability='info'):
    print("COMMAND: ability")
    abilityConversion = {'cha':'charisma', 'con':'constitution', 'dex':'dexterity', 'int':'intelligence', 'str':'strength', 'wis':'wisdom'}

    if ability.lower() == 'info' or ability.lower() not in abilityConversion:
        await ctx.send(f'**Understanding Ability Scores**\n'
        f'\n> **Strength** (str): How hard you can throw a tomato at someone'
        f'\n> **Dexterity** (dex): How many tomatoes you can dodge'
        f'\n> **Constitution** (con): How many rotton tomatoes you can eat'
        f'\n> **Intelligence** (int): Knowing a tomato is a fruit'
        f'\n> **Wisdom** (wis): Knowing not to put a tomato in a fruit salad'
        f'\n> **Charisma** (cha): Being able to sell that tomato fruit salad to someone'
        f'\n\n*Use the command **!ability [ability abbreviation]** to learn more about a specific one.*'
        f'\n*Example: **!ability wis***')
    else:
        try:
            ability = ability.lower()
            response = requests.get(f'https://www.dnd5eapi.co/api/ability-scores/{ability}')
            associatedSkills = [str(s['name']) for s in response.json()["skills"]]
            if associatedSkills == []:
                result = f'**Ability: {response.json()["full_name"]}**\n\n> {response.json()["desc"][0]}\n*Associated skills:* None'
            else:
                associatedSkills_str = ", ".join([str(s['name']) for s in response.json()["skills"]])
                result = f'**Ability: {response.json()["full_name"]}**\n\n> {response.json()["desc"][0]}\n*Associated skills:* {associatedSkills_str}'
            await ctx.send(result)
        except Exception as e:
            print(f'Error: {e}')

@bot.command(name="race", help="Get info about the different races your character can be.")
async def raceInfo(ctx, raceName="info"):
    print("COMMAND: raceInfo")
    diffRaces = ['dragonborn', 'dwarf', 'elf', 'gnome', 'half-elf', 'half-orc', 'halfling', 'human', 'tiefling']

    if raceName.lower() == "info" or raceName.lower() not in diffRaces:
        await ctx.send(f'**Choose from the following races:**'
        f'\n> Dragonborn\n> Dwarf\n> Elf\n> Gnome\n> Half-Elf\n> Half-Orc\n> Halfling\n> Human\n> Tiefling')
    else:
        raceName = raceName.lower()
        url = f"http://dnd5e.wikidot.com/lineage:{raceName}"
        try:
            response = requests.get(url)
            html_data = response.text
            soup = BeautifulSoup(html_data, "html.parser")
            info = soup.find_all(name="em")
            result = f'**Race: {raceName.title()}**\n> {info[0].text.strip("<em>/")}\n> *Learn more: {url} *'
            await ctx.send(result)
        except Exception as e:
            print(f'Error: {e}')

@bot.command(name="help", help="Get information on all of Rollie Pollie's available commands.")
async def helpInfo(ctx, cmdRequested="help"):
    print('COMMAND: help')
    commandDict = {c.name: {"helpinfo":c.help, "params":[p for p in c.clean_params]} for c in bot.commands}

    if cmdRequested == "help" or cmdRequested not in commandDict:
        result = "**Need some help? Here's a list of all the available commands:**\n"
        for k,v in commandDict.items():
            info = f'> __*!{k}*__ --> {v["helpinfo"]} Write it like this: `!{k} {", ".join(v["params"])}`\n'
            result += info
        await ctx.send(result)

    else:
        cmd = cmdRequested.lower()
        result = f'> __*!{cmd}*__ --> {commandDict[cmd]["helpinfo"]} Write it like this: `!{cmd} {", ".join(commandDict[cmd]["params"])}`\n'
        await ctx.send(result)

@bot.command(name="role", help="Assign yourself a role from this server.")
async def assignRole(ctx, roleName="HELP"):
    listOfRoles = ctx.guild.roles
    dictOfRoles = dict()
    listOfRoleNames = list()

    for r in listOfRoles:
        dictOfRoles[r.name.title()] = [r, r.name, r.id]
        listOfRoleNames.append(r.name)

    RPB_indx = listOfRoleNames.index("Rollie Pollie Bot")
    listOfRoleNames = listOfRoleNames[1:RPB_indx]  # keeps only roles that Rollie Pollie Bot can assign
    listofRoleNames_str = ", ".join([n for n in listOfRoleNames])

    if roleName.title() == "Help" or roleName.title() not in listOfRoleNames:
        await ctx.send(f'Use `!role [roleName]` to assign yourself a role! The following roles are available to you: {listofRoleNames_str}')

    else:
        userWants = dictOfRoles[roleName.title()]  # returns list --> [r object, r name, r id]
        if userWants[0] in ctx.author.roles:  # if the user already has this role
            await ctx.author.remove_roles(userWants[0])
            await ctx.send(f"The role {userWants[1]} has been removed because it was already assigned to you. To add it again, repeat the command.")
        else:
            await ctx.author.add_roles(userWants[0])
            await ctx.send(f"The role {userWants[1]} has been assigned to you!")

bot.run(TOKEN)
