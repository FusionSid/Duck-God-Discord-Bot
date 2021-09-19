# Imports
# Duck Bot is the best bot
# Please Don't Ruin This Bot

import os
import discord
from discord.ext import commands
import random
from keep_alive import keep_alive
from replit import db
from googleapiclient.discovery import build
from roastlist import roastlistpy
from discord.ext.commands import (CommandNotFound, MissingRequiredArgument, CommandOnCooldown)
import asyncio
from discord.ext import tasks
import youtube_dl
import requests

# Api key for image search
isapi_key = "AIzaSyCj52wnSciil-4JPd6faOXXHfEb1pzrCuY"

#Prefix
prefix = '.'
client = commands.Bot(prefix, help_command=None)
intents = discord.Intents.all()


# Events

# When bot is online change status and print
@client.event
async def on_ready():
  await client.change_presence(activity=discord.Game("Hunting Frogs"))
  print("A wild duck god has spawned")
  channel = client.get_channel(865762590831149087)
  await channel.send("Sup\nI'm Online now")

# New Member Join
@client.event
async def on_member_join(member):
  embeddm = discord.Embed(title = "__Welcome Message!__", description = f"Hey there {member.name}, Welcome to the discord server. My name is duck god. You shall worship me or else.\nIf you want to live - Join the duck cult. Command is .jc \nIt wont work here so type it in the server.\n.help = Help and Command List")
  channel = client.get_channel()
  await channel.send(embed=embeddm)
  await member.send(embed=embeddm)


# Client Commands:

# -----------------------------------------------------------------------------------------------------------------------------------
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
async def joincult(ctx, dcname : str):
  update_cult_members(dcname)
  em = discord.Embed(title = f'{dcname} has joined the cult')
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
  numrn = db["numrn"]
  if num == numrn + 1:
    db["numrn"] = num
  else:
    await ctx.send(embed=discord.Embed(title="The little ducker ruined it", description=f"Duck you {ctx.author.name}"))
    await ctx.send("Count reset to zero, don't ruin it this time")
    db["numrn"] = 0

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
  em = discord.Embed(title="__Duck 8 Ball__", description = f"{question}\nAnswer: {random.choice(_8ballans)}")
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
async def calc(ctx, n1: int, op, n2:int):
  ans = calculator(n1, op, n2)
  await ctx.send(embed=discord.Embed(title='Calculator Duck:', description = ans))

# Duck Roast
@client.command(aliases=["rm"])
async def duckroast(ctx):
  roast = random.choice(roastlistpy)
  em = discord.Embed(title = roast)
  await ctx.send(embed=em)

# -----------------------------------------------------------------------------------------------------------------------------------

# Message Commands:

# Message User
@client.command(aliases=["dm"])
async def duckdm(ctx, member:discord.Member, *, message):
  embeddm = discord.Embed(title = message)
  await member.send(embed=embeddm)
  await ctx.channel.purge(limit=1)

# Send Roast 
@client.command(aliases=["sr"])
async def sendroast(ctx, member:discord.Member):
  message = random.choice(roastlistpy)
  author = ctx.author.name
  embeddm = discord.Embed(title = message, description = "Imagine being roasted by a ducking bot")
  await member.send(embed=embeddm)
  await ctx.channel.purge(limit=1)

# Feedback
@client.command(aliases=["fb"])
async def feedback(ctx, member="FusionSid", *, message):
  embeddm = discord.Embed(title = message)
  await member.send(embed=embeddm)
  await ctx.channel.purge(limit=1)
  await ctx.send("Feedback Sent")


# Music commands:

from music_cog import music_cog
client.add_cog(music_cog(client))

# -----------------------------------------------------------------------------------------------------------------------------------
# Duck economy stuff:

# Duck Coin Create Account
@client.command()
async def createacc(ctx):
  if ctx.author.name in db.keys():
    em = discord.Embed(title = "You already have an account")
    await ctx.send(embed=em)
  else:
    db[ctx.author.name] = 0
    await ctx.send(embed =discord.Embed(title="Account Created!"))

# Balance in duckcoins
@client.command(aliases=["bal"])
async def duckbal(ctx):
  if ctx.author.name in db.keys():
    em = discord.Embed(title = f'__**{ctx.author.name}**__', description =  f'Account balance is {db[ctx.author.name]}')
    await ctx.send(embed=em)
  else:
    await ctx.send(embed = discord.Embed("Looks like you don't have an account. To create one: .createacc"))

# Beg for coins
@client.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def beg(ctx):
  if ctx.author.name in db.keys():
    afb = random.randint(1, 100)
    balrn = int(db[ctx.author.name])
    abrn = balrn + afb
    db[ctx.author.name] = abrn
    em = discord.Embed(title = "Here you little peasant", description = f'You got given {afb} duckcoins')
    await ctx.send(embed = em)
  else:
    await ctx.send(embed=discord.Embed(title = "Looks like you don't have an account, Where do you think im gonna put the money? To create one: .createacc"))

# -----------------------------------------------------------------------------------------------------------------------------------
# Admin Commands

def is_it_me(ctx):
  return ctx.author.id == 624076054969188363

# List Keys
@client.command(aliases=['listkeys', 'keylist', 'klist', 'kl'])
@commands.check(is_it_me)
async def listk(ctx):
  await ctx.channel.purge(limit=1)
  keys = db.keys()
  await ctx.send(keys, delete_after=10)

# Delete Key
@client.command(aliases=['deletekey', 'dk', 'keydel'])
@commands.check(is_it_me)
async def delk(ctx, *, key):
  await ctx.channel.purge(limit=1)
  dkey = key
  del db[dkey]
  await ctx.send("done", delete_after=10)

# Key value
@client.command(aliases=['keyval', 'valkey', 'keyv', 'kv'])
@commands.check(is_it_me)
async def kval(ctx, *, key):
  await ctx.channel.purge(limit=1)
  value = db[key]
  await ctx.send(value, delete_after=10)

# Change Key Value
@client.command(aliases=['changekv', 'ckv'])
@commands.check(is_it_me)
async def ckval(ctx, key, *, val:int):
  await ctx.channel.purge(limit=1)
  db[key] = val
  print(val)
  await ctx.send(f"{key} has been changed to {val}", delete_after=10)

# Key info    
@client.command()
@commands.check(is_it_me)
async def keyhelp(ctx):
  em = discord.Embed(title="__Admin Key Commands__\n.dk, .ckv, .kv, kl", description="Delete Key: .dk <key>\nKey list: .kl\nChange Key Value: .kv <key> <value>\n")
  await ctx.send(embed=em, delete_after=5)
# Say stuff
@client.command(aliases=["s"])
@commands.check(is_it_me)
async def say(ctx, em : str, *, message):
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
async def eatmessage(ctx, ammount : int):
  await ctx.channel.purge(limit=ammount)

# Leave Cult
def leave_cult(index):
  members = db["members"]
  if len(members) >= index:
    del members[index]
    db["members"] = members

@client.command(aliases=['rcm'])
@commands.check(is_it_me)
async def removecm(ctx, lcname : int):
  members = db["members"]
  leavingmember = members[lcname]
  leave_cult(lcname)
  em = discord.Embed(title = f'{leavingmember} has been removed from the cult')
  await ctx.send(embed=em)
  
@client.command(aliases=["dms"])
@commands.check(is_it_me)
async def spamdm(ctx, amount:int, member:discord.Member, *, message):
  em = discord.Embed(title = message)
  for i in range(amount):
    await member.send(embed=em)
  await ctx.channel.purge(limit=1)

@client.command()
@commands.check(is_it_me)
async def admincmds(ctx):
  embed = discord.Embed(title = 'Admin Commands:', description = 'removecm <lcname:int>\ndms <amount> <member>\neatm <amount>\nsay <yt/yd/n> <text>\n.keyhelp for key/database commands')
  
  await ctx.send(embed=embed, delete_after=5)

# -----------------------------------------------------------------------------------------------------------------------------------

# Help and Command list

@client.group(invoke_without_command=True, aliases=["duckhelp", "help"])
async def duckcommandhelp(ctx):
  em = discord.Embed(title = "__**Duck Help**__", description = "use .help <command> for extended info on command", color = ctx.author.color)

  em.add_field(name = "__Cult__", value = "jc, lc, lcm")
  em.add_field(name = "__Fun/Questions__", value = "8ball, ducksearch, calc, duckroast, c, fact")
  em.add_field(name = "__Message__", value = "feedback, ducksearch, dm, sendroast")
  em.add_field(name = "__Music__", value = "play, skip, queue")
  em.add_field(name = "__Duckcoin__", value = "createacc, bal, beg")
  em.add_field(name = "__More Help:__", value = "Dm FusionSid")
  await ctx.send(embed = em)

# Command list
@client.command(aliases=["commandslist"])
async def commands(ctx):
  clembed = discord.Embed(title = "__List of Duck Bot Commands__", desciption = " ")
  clembed.add_field(name = "\n__.jc__", value="Join cult")
  clembed.add_field(name = "\n__.lc__", value="Leave cult")
  clembed.add_field(name = "\n__.lcm__", value="List cult members")
  clembed.add_field(name = "\n__.dm__", value="Duck God send DM")
  clembed.add_field(name = "\n__.createacc__", value="Create Account")
  clembed.add_field(name = "\n__.bal__", value="Balance")
  clembed.add_field(name = "\n__.beg__", value="Beg")
  clembed.add_field(name = "\n__.8ball__", value="8ball")
  clembed.add_field(name = "\n__.ducksearch__", value="Duck Search")
  clembed.add_field(name = "\n__.duckroast__", value="Duck Roast")
  clembed.add_field(name = "\n__.sendroast__", value="Send Roast")
  clembed.add_field(name = "\n__.queue__", value="Queue")
  clembed.add_field(name = "\n__.play__", value="Play Song")
  clembed.add_field(name = "\n__.skip__", value="Skip Song")
  clembed.add_field(name = "\n__.fact__", value="Random Fact")
  clembed.add_field(name = "\n__.c__", value="Counting - only do in counting channel")
  clembed.add_field(name = "\n__.calc__", value="Calculate.")
  clembed.add_field(name = "\nFor information about command:", value=".help <commandname(without . prefix)>\n")
  clembed.add_field(name = "Example(for help about the duckroast command):", value=".help duckroast")
  clembed.add_field(name = "For any help:", value=".help")
  await ctx.send(embed=clembed)

# Custom Help per command

@duckcommandhelp.command()
async def jc(ctx):
  em = discord.Embed(title = "Join Cult", description = "Joins the duck cult", color = ctx.author.color)
  em.add_field(name = "Command", value = ".jc <@name>")
  await ctx.send(embed=em)

@duckcommandhelp.command()
async def fact(ctx):
  em = discord.Embed(title = "Fact", description = "Tells a random fact", color = ctx.author.color)
  em.add_field(name = "Command", value = ".fact")
  await ctx.send(embed=em)

@duckcommandhelp.command()
async def skip(ctx):
  em = discord.Embed(title = "Skip Song", description = "Skips the song currently playing", color = ctx.author.color)
  em.add_field(name = "Command", value = ".skip")
  await ctx.send(embed=em)

@duckcommandhelp.command()
async def play(ctx):
  em = discord.Embed(title = "Play song", description = "Joins the duck cult", color = ctx.author.color)
  em.add_field(name = "Command", value = ".play <song name>")
  await ctx.send(embed=em)

@duckcommandhelp.command()
async def queue(ctx):
  em = discord.Embed(title = "List Queue", description = "Lists all the songs in the queue", color = ctx.author.color)
  em.add_field(name = "Command", value = ".q")
  await ctx.send(embed=em)

@duckcommandhelp.command()
async def sendroast(ctx):
  em = discord.Embed(title = "Send Roast", description = "Duck dms a roast to user of you choice", color = ctx.author.color)
  em.add_field(name = "Command", value = ".sendroast <@persontosendto>")
  await ctx.send(embed=em)

@duckcommandhelp.command()
async def lc(ctx):
  em = discord.Embed(title = "Leave Cult", description = "Leaves the duck cult", color = ctx.author.color)
  em.add_field(name = "Command", value = ".lc <index>\nIndex's start from 0")
  await ctx.send(embed=em)

@duckcommandhelp.command()
async def lcm(ctx):
  em = discord.Embed(title = "List Cult Members", description = "Lists all duck member, Pings them too", color = ctx.author.color)
  em.add_field(name = "Command", value = ".lcm")
  await ctx.send(embed=em)

@duckcommandhelp.command(aliases=["8ball"])
async def _8ball(ctx):
  em = discord.Embed(title = "8 Ball", description = "Asks the magical 8 ball a question", color = ctx.author.color)
  em.add_field(name = "Command", value = ".8ball <question>")
  await ctx.send(embed=em)

@duckcommandhelp.command()
async def duckroast(ctx):
  em = discord.Embed(title = "Duck Roast", description = "Duck god roasts you", color = ctx.author.color)
  em.add_field(name = "Command", value = ".duckroast")
  await ctx.send(embed=em)

@duckcommandhelp.command()
async def c(ctx):
  em = discord.Embed(title = "Counting", description = "The number you type must be 1 greater than the previous number. If you type the same number, a number less or too more, count resets to zero", color = ctx.author.color)
  em.add_field(name = "Command", value = ".c <number>")
  await ctx.send(embed=em)

@duckcommandhelp.command()
async def ducksearch(ctx):
  em = discord.Embed(title = "Duck Search\nThe Best Command", description = "Searches the web for a image of you choice", color = ctx.author.color)
  em.add_field(name = "Command", value = ".ducksearch <search>")
  await ctx.send(embed=em)

@duckcommandhelp.command()
async def bal(ctx):
  em = discord.Embed(title = "Duck Balance", description = "Displays you duckcoin bank balance", color = ctx.author.color)
  em.add_field(name = "Command", value = ".bal")
  await ctx.send(embed=em)

@duckcommandhelp.command()
async def dm(ctx):
  em = discord.Embed(title = "Duck DM", description = "Duck god DMs user of your choice", color = ctx.author.color)
  em.add_field(name = "Command", value = ".dm <@user> <message>")
  await ctx.send(embed=em)

@duckcommandhelp.command()
async def createacc(ctx):
  em = discord.Embed(title = "Create Account", description = "Creates you a duck bank account", color = ctx.author.color)
  em.add_field(name = "Command", value = ".createacc")
  await ctx.send(embed=em)

@duckcommandhelp.command()
async def beg(ctx):
  em = discord.Embed(title = "Beg", description = "Begs for duckcoins", color = ctx.author.color)
  em.add_field(name = "Command", value = ".beg")
  await ctx.send(embed=em)

@duckcommandhelp.command()
async def calc(ctx):
  em = discord.Embed(title = "Calculator", description = "Begs for duckcoins", color = ctx.author.color)
  em.add_field(name = "Command", value = ".calc <num1> <operator> <num2>\nOperators: +, -, /, x")
  await ctx.send(embed=em)


# Errors

@client.event
async def on_command_error(ctx, error):
  er = error
  if isinstance(error, CommandOnCooldown):
    em = discord.Embed(title = "Wow buddy, Slow it down\nThis command is on cooldown", description = f'Try again in {error.retry_after:,.2f}seconds.') 
    await ctx.send(embed=em)

  elif isinstance(error, CommandNotFound):
    em = discord.Embed(title = "Command not found", description = "This command either doesn't exist, or you typed it wrong.\n.commands to see list of commands")
    await ctx.send(embed=em)

  elif isinstance(error, MissingRequiredArgument):
    em = discord.Embed(title = "Missing a requred value/arg", description = "You haven't passed in all value/arg")
    await ctx.send(embed=em)

  else:
    print("An error has occured")
    errsee = input("Wanna see error? y/n ")
    if errsee.lower() == 'y':
      print(er)
      
# -----------------------------------------------------------------------------------------------------------------------------------
# Run

keep_alive()
client.run(os.environ['Token'])
