# Imports
# Please Don't Ruin This Bot

import os
import discord
from discord.ext import commands
import random
from keep_alive import keep_alive
from replit import db
from googleapiclient.discovery import build
from roastlist import roastlistpy
from discord.ext.commands import (
    CommandNotFound, MissingRequiredArgument, CommandOnCooldown)
import database
import asyncio
from discord.ext import tasks
import requests
import json

rank = {
    "Duck God - Owner": "FusioSid",
}

# Api key for image search
isapi_key = "AIzaSyCj52wnSciil-4JPd6faOXXHfEb1pzrCuY"

# Prefix
prefix = '.'
client = commands.Bot(prefix, help_command=None)
intents = discord.Intents.all()

fusionsidid = 624076054969188363
fusionsid = client.fetch_user(624076054969188363)

# -----------------------------------------------------------------------------------------------------------------------------------
# Events and loops

# When bot is online change status and print
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("Hunting Frogs"))
    print("A wild duck god has spawned")
    channel = client.get_channel(889716400392921119)
    await channel.send("Online")

# New Member Join
@client.event
async def on_member_join(member):
  channel = member.channel
  embeddm = discord.Embed(title="__Welcome Message!__",description=f"Hey there {member.name}, Welcome to the discord server. My name is duck god. You shall worship me or else.\nIf you want to live - Join the duck cult. Command is .jc \n.help = Help and Command List")
  await channel.send(embed=embeddm)

@client.event
async def on_message(message):
  channel = message.channel
  msg = message.content
  
  if message.author == client.user:
        return

  bad_word = database.check_word(msg)
  if bad_word == True:
    await message.channel.purge(limit=1)
    await message.channel.send("Thats a bad word", delete_after=1.5)

  if channel.id == 892597297626628127:
    await message.channel.send("sup")

  await client.process_commands(message)

  

@tasks.loop(minutes=60.0)
async def genintrest():
  with open('mainbank.json', 'r') as f:
      users = json.load(f)

  for user in users:
      bank = users[user]["bank"]
      before = bank
      bank += bank*0.069
      money_made = bank - before
      sendto = await client.fetch_user(user)
      msg_dm = f"You made {money_made} in intrest while you were away by keeping your coins in duck bank!"
      await sendto.send(embed=discord.Embed(title="Intrest", description=msg_dm))
      users[user]["bank"] = bank
      with open('mainbank.json', 'w') as f:
        json.dump(users, f)

  print("Generated Intrest")

genintrest.start()

# -----------------------------------------------------------------------------------------------------------------------------------

# Client Commands:

# Cult Commands:

# Join Cult


def update_cult_members(member):
    if "members" in db.keys():
        members = db["members"]
        members.append(member)
        db["members"] = members
    else:
        db["members"] = [member]


@client.command(aliases=['jc'])
async def joincult(ctx, dcname: str):
    update_cult_members(dcname)
    em = discord.Embed(title=f'{dcname} has joined the cult')
    await ctx.send(embed=em)

# List Cult Members


@client.command(aliases=['lcm'])
async def list_cult_members(ctx,):
    dcm = db["members"]
    dcmlen = len(dcm)
    frikinranvar = 0
    await ctx.send("The Duck Cult Members Are:\n")
    for i in range(dcmlen):
        await ctx.send(dcm[frikinranvar])
        frikinranvar = frikinranvar + 1

# -----------------------------------------------------------------------------------------------------------------------------------
# Fun/Question commands:

# Counting


@client.command()
async def c(ctx, num: int):
    channel = ctx.channel.id
    if channel == 865787555378757672:
        numrn = db["numrn"]
        if num == numrn + 1:
            db["numrn"] = num
        else:
            await ctx.send(embed=discord.Embed(title="The little ducker ruined it", description=f"Duck you {ctx.author.name}"))
            await ctx.send("Count reset to zero, don't ruin it this time")
            db["numrn"] = 0
    else:
        await ctx.send("Youre in the wrong channel go to the counting channel")
# 8ball


@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    _8ballans = [
        "As I see it, yes",
        "It is certain",
        "It is decidedly so",
        "Most likely",
        "Outlook good",
        "Signs point to yes",
        "Without a doubt",
        "Yes",
        "Yes - definitely",
        "You may rely on it",
        "Reply hazy, try again",
        "Ask again later",
        "Better not tell you now",
        "Cannot predict now",
        "Concentrate and ask again",
        "Don't count on it",
        "My reply is no",
        "My sources say no",
        "Outlook not so good",
        "Very doubtful"
    ]
    em = discord.Embed(title="__Duck 8 Ball__",
                       description=f"{question}\nAnswer: {random.choice(_8ballans)}")
    await ctx.send(embed=em)

# Duck search


@client.command(aliases=["ds"])
async def ducksearch(ctx, *, search):
    ran = random.randint(0, 9)
    resource = build("customsearch", "v1", developerKey=isapi_key).cse()
    result = resource.list(
        q=f"{search}", cx="54c1117c3e104029b", searchType="image"
    ).execute()
    url = result["items"][ran]["link"]
    embed1 = discord.Embed(title=f"Duck Search:({search.title()})")
    embed1.set_image(url=url)
    await ctx.send(embed=embed1)

# Calculator


def calculator(num1, operator, num2):
    if operator == "+":
        return num1 + num2
    elif operator == "-":
        return num1 - num2
    elif operator == "/":
        return num1 / num2
    elif operator == "x":
        return num1 * num2


@client.command()
async def calc(ctx, n1: int, op, n2: int):
    ans = calculator(n1, op, n2)
    await ctx.send(embed=discord.Embed(title='Calculator Duck:', description=ans))

# Duck Roast


@client.command(aliases=["rm"])
async def duckroast(ctx):
    roast = random.choice(roastlistpy)
    em = discord.Embed(title=roast)
    await ctx.send(embed=em)

# Message Commands:

# Message User


@client.command(aliases=["dm"])
async def duckdm(ctx, member: discord.Member, *, message):
    embeddm = discord.Embed(title=message)
    await member.send(embed=embeddm)
    await ctx.channel.purge(limit=1)

# Send Roast


@client.command(aliases=["sr"])
async def sendroast(ctx, member: discord.Member):
    message = random.choice(roastlistpy)
    author = ctx.author.name
    embeddm = discord.Embed(
        title=message, description="Imagine being roasted by a ducking bot")
    await member.send(embed=embeddm)
    await ctx.channel.purge(limit=1)

# Feedback


@client.command(aliases=["fb", "suggestion", "suggest"])
async def feedback(ctx, member="FusionSid", *, message):
    embeddm = discord.Embed(title=message)
    await member.send(embed=embeddm)
    await ctx.channel.purge(limit=1)
    await ctx.send("Feedback Sent")

@client.command(aliases=["rm"])
async def duckroast(ctx):
    roast = random.choice(roastlistpy)
    em = discord.Embed(title=roast)
    await ctx.send(embed=em)

@client.command(aliases=["sr"])
async def sendroast(ctx, member: discord.Member):
    message = random.choice(roastlistpy)
    author = ctx.author.name
    embeddm = discord.Embed(
        title=message, description="Imagine being roasted by a ducking bot")
    await member.send(embed=embeddm)
    await ctx.channel.purge(limit=1)
    
# DUCK BATTLE


@client.command(aliases=["fight"])
async def battle(ctx, amount: int):
    user = ctx.author

    users = await get_bank_data()

    wallet = users[str(user.id)]["wallet"]
    bank = users[str(user.id)]["bank"]

    try:
        amount = int(amount)

    except:
        if amount.lower() == "max":
            amount = bank

        elif amount.lower() == "all":
            amount = bank

        else:
            amount = conv2num(amount)

    def wfcheck(m):
        return m.channel == ctx.channel and m.author == ctx.author
    await ctx.send(embed=discord.Embed(title="Duck War", description=f"Are you sure you want to send {amount} into battle? \n(1 duck costs 69 duckcoins)\ny/n"))
    msg = await client.wait_for("message", check=wfcheck)
    msg = msg.content
    print(msg)
    if msg.lower() == "y":
        lived = random.randint(0, amount)
        dead = amount - lived
        await ctx.send(embed=discord.Embed(title = "DUCK WAR", description=f"Ducks Lived = {lived}, \nDucks Lost = {dead}"))
        if lived > dead:
            win = True
            await open_account(ctx.author)
            user = ctx.author

            users = await get_bank_data()

            earnings = lived*69

            await ctx.send('{} Got {:,} duckcoins for winning the war!!'.format(ctx.author.mention, earnings))

            users[str(user.id)]["wallet"] += earnings

            with open("mainbank.json", 'w') as f:
                json.dump(users, f)
        else:
            win = False
            await ctx.send("Duck You, Inocent ducks have lost their lives\nYou lose the war")
            await open_account(ctx.author)
            user = ctx.author

            users = await get_bank_data()

            earnings = dead*69

            await ctx.send(embed=discord.Embed(title = f'{ctx.author.mention}', description = 'Lost {:,} duckcoins!!'.format(earnings)))

            users[str(user.id)]["wallet"] -= earnings

            with open("mainbank.json", 'w') as f:
                json.dump(users, f)
    else:
        await ctx.send("Ok")


# Duck economy stuff:

mainshop = [{"name": "Duck Statue", "price": 100000, "description": "A massive statue of the all mighty Duck God", "buy": True},
            {"name": "Laptop", "price": 1000,
                "description": "For them memes and for watching videos on duckhub", "buy": True},
            {"name": "PC", "price": 5000,
                "description": "a really powerful gaming pc powered by the blood of you enemies", "buy": True},
            {"name": "Duck Car", "price": 99999,
                "description": "Duck Car go brrr", "buy": True},
            # Collectables
            {"name": "Frog foot", "price": 1000,
                "description": "Frog foot to show off at your next duck meeting\nCollectable - Not Available to buy", "buy": False},
            {"name": "Frog head", "price": 10000,
                "description": "The head of a frog. An amazing flex.\nCollectable - Not Available to buy", "buy": False},
            {"name": "Frog Corpse", "price": 1000000,
                "description": "The ULTIMATE flex. You murdered an entire frog\nCollectable - Not Available to buy", "buy": False},
            {"name": "Duck slave", "price": 69,
                "description": "A duck minon who isnt paid anything. If he works the minimum time(50h a day) then maybe you can let him eat\nCollectable - Not Available to buy", "buy": False}
            ]

# {"name": "", "price": , "description":"", "buy": }


def conv2num(amount):
    lenght = 0
    for i in amount:
        lenght += 1
    lenght -= 1

    last_letter = amount[lenght]

    rest = amount[:-1]

    try:
        rest = int(rest)
        if last_letter.lower() == "k":
            amount = rest*1000

        elif last_letter.lower() == "m":
            amount = rest*1000000

    except:
        print("Not a number")

    return amount


@client.command(aliases=['bal'])
async def balance(ctx, person: discord.Member = None):
    print(person)
    if person == None:
        print(ctx.author)
        await open_account(ctx.author)
        user = ctx.author

        users = await get_bank_data()

        wallet_amt = users[str(user.id)]["wallet"]
        bank_amt = users[str(user.id)]["bank"]
        
        # round
        wallet_amt = round(wallet_amt, 2)
        bank_amt = round(bank_amt, 2)
        
        wallet_amt = "{:,}".format(wallet_amt)
        bank_amt = "{:,}".format(bank_amt)

        em = discord.Embed(
            title=f'{ctx.author.name} Balance', color=discord.Color.red())
        em.add_field(name="Wallet Balance", value=wallet_amt)
        em.add_field(name='Bank Balance', value=bank_amt)
        await ctx.send(embed=em)
    else:
        await open_account(person)
        user = person

        users = await get_bank_data()

        wallet_amt = users[str(user.id)]["wallet"]
        bank_amt = users[str(user.id)]["bank"]
        
        # round
        wallet_amt = round(wallet_amt, 2)
        bank_amt = round(bank_amt, 2)

        em = discord.Embed(title=f'{person.name} Balance', color=discord.Color.red())
        em.add_field(name="Wallet Balance", value=wallet_amt)
        em.add_field(name='Bank Balance', value=bank_amt)
        await ctx.send(embed=em)

@client.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def beg(ctx):
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()

    earnings = random.randrange(101)

    await ctx.send(embed=discord.Embed(title = f'{ctx.author.mention} Here you filty peasant', description = f'Got {earnings} duckcoins!!'))

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json", 'w') as f:
        json.dump(users, f)


@client.command()
@commands.cooldown(1, 60*1440, commands.BucketType.user)
async def daily(ctx):
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()

    earnings = 10000

    await ctx.send(embed=discord.Embed(title = f'{ctx.author.mention}', description = 'Got {:,} duckcoins!!'.format(earnings)))

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json", 'w') as f:
        json.dump(users, f)


@client.command(aliases=['with'])
async def withdraw(ctx, amount=None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    user = ctx.author

    users = await get_bank_data()

    wallet = users[str(user.id)]["wallet"]
    bank = users[str(user.id)]["bank"]

    try:
        amount = int(amount)

    except:
        if amount.lower() == "max":
            amount = bank

        elif amount.lower() == "all":
            amount = bank

        else:
            amount = conv2num(amount)

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[1]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author, amount)
    await update_bank(ctx.author, -1*amount, 'bank')
    await ctx.send('{} You withdrew {:,} coins'.format(ctx.author.mention, amount))


@client.command(aliases=['dep'])
async def deposit(ctx, amount=None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    user = ctx.author

    users = await get_bank_data()

    wallet = users[str(user.id)]["wallet"]
    bank = users[str(user.id)]["bank"]

    try:
        amount = int(amount)

    except:
        if amount.lower() == "max":
            amount = wallet

        elif amount.lower() == "all":
            amount = wallet

        else:
            amount = conv2num(amount)

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author, -1*amount)
    await update_bank(ctx.author, amount, 'bank')
    await ctx.send('{} You deposited {:,} coins'.format(ctx.author.mention, amount))


@client.command(aliases=['sm'])
async def send(ctx, member: discord.Member, amount=None):
    await open_account(ctx.author)
    await open_account(member)
    if amount == None:
        await ctx.send("Please enter the amount i havent got all day")
        return

    bal = await update_bank(ctx.author)
    if amount == 'all':
        amount = bal[0]

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send('Get some more duckcoins you poor duck\nYou do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author, -1*amount, 'bank')
    await update_bank(member, amount, 'bank')
    await ctx.send(f'{ctx.author.mention} You gave {member} {amount} coins')


@client.command(aliases=['rb'])
async def rob(ctx, member: discord.Member):
    await open_account(ctx.author)
    await open_account(member)
    bal = await update_bank(member)

    if bal[0] < 100:
        await ctx.send('It is useless to rob him/her :(')
        return

    earning = random.randrange(0, bal[0])

    await update_bank(ctx.author, earning)
    await update_bank(member, -1*earning)
    await ctx.send(f'{ctx.author.mention} You robbed {member} and got {earning} coins')


@client.command()
async def gamble(ctx, amount=None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return
    bal = await update_bank(ctx.author)

    user = ctx.author

    users = await get_bank_data()

    wallet = users[str(user.id)]["wallet"]
    bank = users[str(user.id)]["bank"]

    try:
        amount = int(amount)

    except:
        if amount.lower() == "max":
            amount = bank

        elif amount.lower() == "all":
            amount = bank

        else:
            amount = conv2num(amount)

    if amount > bal[0]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return
    final = []
    for i in range(3):
        a = random.choice(['X', 'O', 'Q'])

        final.append(a)

    await ctx.send(str(final))

    if final[0] == final[1] or final[1] == final[2] or final[0] == final[2]:
        await update_bank(ctx.author, 2*amount)
        await ctx.send(f'You won :) {ctx.author.mention}')
    else:
        await update_bank(ctx.author, -1*amount)
        await ctx.send(f'You lose :( {ctx.author.mention}')


@client.command()
async def shop(ctx, *, item_=None):
    if item_ == None:
        em = discord.Embed(title="Shop")

        for item in mainshop:
            name = item["name"]
            price = item["price"]
            desc = item["description"]
            buy = item['buy']
            if buy == True:
                em.add_field(name=name, value=f"${price} | {desc}")
    else:
        em = discord.Embed(title="Shop")
        for item in mainshop:
            if item["name"].lower() == item_.lower():
                name = item["name"]
                price = item["price"]
                desc = item["description"]
                buy = item['buy']
                em.add_field(name=name, value=f"${price} | {desc}")
            else:
              em.add_field(name=item_, value="Item not in shop")
              break
    await ctx.send(embed=em)


@client.command()
async def buy(ctx, amount=1, *, item):
    await open_account(ctx.author)

    res = await buy_this(ctx.author, amount, item)

    if not res[0]:
        if res[1] == 1:
            await ctx.send("That Object isn't there!")
            return
        if res[1] == 2:
            await ctx.send(f"You don't have enough duckcoins in your wallet to buy {amount} {item}")
            return

    await ctx.send(f"You just bought {amount} {item}")


async def buy_this(user, amount, item_name):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False, 1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0] < cost:
        return [False, 2]

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t == None:
            obj = {"item": item_name, "amount": amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item": item_name, "amount": amount}
        users[str(user.id)]["bag"] = [obj]

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

    await update_bank(user, cost*-1, "wallet")

    return [True, "Worked"]


@client.command()
async def bag(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []

    em = discord.Embed(title="Bag")
    for item in bag:
        name = item["item"]
        amount = item["amount"]

        em.add_field(name=name, value=amount)

    await ctx.send(embed=em)


@client.command()
async def sell(ctx, amount=1, *, item):
    await open_account(ctx.author)

    res = await sell_this(ctx.author, item, amount)

    if not res[0]:
        if res[1] == 1:
            await ctx.send("You dont have that item!")
            return
        if res[1] == 2:
            await ctx.send(f"You don't have {amount} {item} in your bag.")
            return
        if res[1] == 3:
            await ctx.send(f"You don't have {item} in your bag.")
            return

    await ctx.send(f"You just sold {amount} {item}.")


async def sell_this(user, item_name, amount, price=None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price == None:
                price = 0.7 * item["price"]
            break

    if name_ == None:
        return [False, 1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False, 2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t == None:
            return [False, 3]
    except:
        return [False, 3]

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

    await update_bank(user, cost, "wallet")

    return [True, "Worked"]


async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open('mainbank.json', 'w') as f:
        json.dump(users, f)

    return True


async def get_bank_data():
    with open('mainbank.json', 'r') as f:
        users = json.load(f)

    return users


async def update_bank(user, change=0, mode='wallet'):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open('mainbank.json', 'w') as f:
        json.dump(users, f)
    bal = users[str(user.id)]['wallet'], users[str(user.id)]['bank']
    return bal


# Admin Commands


def is_it_me(ctx):
    return ctx.author.id == 624076054969188363

# Say stuff


@client.command(aliases=["s"])
@commands.check(is_it_me)
async def say(ctx, em: str, *, message):
    await ctx.channel.purge(limit=1)
    if em == "yt":
        await ctx.send(embed=discord.Embed(title=message))
    if em == "yd":
        await ctx.send(embed=discord.Embed(description=message))
    if em == "n":
        await ctx.send(message)

# Eat Messages


@client.command(aliases=['eatm', 'clear', 'del'])
@commands.check(is_it_me)
async def eatmessage(ctx, ammount: int):
    await ctx.channel.purge(limit=ammount+1)

# Leave Cult


def leave_cult(index):
    members = db["members"]
    if len(members) >= index:
        del members[index]
        db["members"] = members


@client.command(aliases=['rcm'])
@commands.check(is_it_me)
async def removecm(ctx, lcname: int):
    members = db["members"]
    leavingmember = members[lcname]
    leave_cult(lcname)
    em = discord.Embed(title=f'{leavingmember} has been removed from the cult')
    await ctx.send(embed=em)


@client.command(aliases=["dms"])
@commands.check(is_it_me)
async def spamdm(ctx, amount: int, member: discord.Member, *, message):
    em = discord.Embed(title=message)
    for i in range(amount):
        await member.send(embed=em)
    await ctx.channel.purge(limit=1)


# Custom SQL Command
@client.command()
@commands.check(is_it_me)
async def sql(ctx, *, cmd):
  database.execute(cmd)
  await ctx.send("Done", delete_after=1)


@client.command()
@commands.check(is_it_me)
async def sqlsearch(ctx, *, cmd):
  search = database.search(cmd)
  await ctx.send(search)


@client.command()
@commands.check(is_it_me)
async def sqlundo(ctx):
  database.undo()

@client.command()
@commands.check(is_it_me)
async def admincmds(ctx):
    embed = discord.Embed(title='Admin Commands:',
                          description='removecm <lcname:int>\ndms <amount> <member>\neatm <amount>\nsay <yt/yd/n> <text>\n.keyhelp for key/database commands')

    await ctx.send(embed=embed, delete_after=5)


@client.command(aliases=['code'])
async def sourcecode(ctx):
    await ctx.send("https://github.com/FusionSid/Duck-God-Discord-Bot")

# Errors

@client.event
async def on_command_error(ctx, error):
    er = error
    channel = client.get_channel(889716400392921119)
    await channel.send(embed=discord.Embed(title="ERROR", description=er))
    if isinstance(error, CommandOnCooldown):
        em = discord.Embed(title="Wow buddy, Slow it down\nThis command is on cooldown",
                           description=f'Try again in {error.retry_after:,.2f}seconds.')
        await ctx.send(embed=em)

    elif isinstance(error, CommandNotFound):
        em = discord.Embed(title="Command not found",
                           description="This command either doesn't exist, or you typed it wrong.\n.commands to see list of commands")
        await ctx.send(embed=em)

    elif isinstance(error, MissingRequiredArgument):
        em = discord.Embed(title="Missing a requred value/arg",
                           description="You haven't passed in all value/arg")
        await ctx.send(embed=em)

    else:
        print("An error has occured:")
        await ctx.send("ERROR", delete_after=1)

# Run

extensions = ['cogs.Music', 'cogs.Help', 'cogs.Fun']

if __name__ == 'main':
    for ext in extensions:
        client.load_extension(ext)

keep_alive()
client.run(os.environ['Token'])
