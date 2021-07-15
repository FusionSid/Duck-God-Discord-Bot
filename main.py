import os
import discord
from discord.ext import commands
import random
from keep_alive import keep_alive
from replit import db
from googleapiclient.discovery import build
from roastlist import roastlistpy
from discord.ext.commands import (CommandNotFound, MissingRequiredArgument, CommandOnCooldown)

# DUCK Bot is the best bot
# Please Don't Ruin This Bot

isapi_key = "AIzaSyCj52wnSciil-4JPd6faOXXHfEb1pzrCuY"

prefix = '.'

client = commands.Bot(prefix, help_command=None)


# Bot is online
@client.event
async def on_ready():
  await client.change_presence(activity=discord.Game("Hunting Frogs"))
  print("A wild duck god has spawned\n\nDuck god is ready to eat")


# New Member Join
@client.event
async def on_member_join(member):
  embeddm = discord.Embed(title = "__Welcome Message!__", description = f"Hey there {member.name}, Welcome to the discord server. My name is duck god. You shall worship me or else.\nIf you want to live - Join the duck cult. Command is .jc \nIt wont work here so type it in the server.\n.help = Help and Command List")
  await member.send(embed=embeddm)

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


# Leave Cult
def leave_cult(index):
  members = db["members"]
  if len(members) >= index:
    del members[index]
    db["members"] = members

@client.command(aliases=['lc'])
async def leavecult(ctx, lcname : int):
  members = db["members"]
  leavingmember = members[lcname]
  leave_cult(lcname)
  em = discord.Embed(title = f'{leavingmember} has left the cult')
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


# Duck Roast
@client.command(aliases=["rm"])
async def duckroast(ctx):
  roast = random.choice(roastlistpy)
  em = discord.Embed(title = roast)
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


# Message User
@client.command(aliases=["dm"])
async def duckdm(ctx, member:discord.Member, *, message):
  embeddm = discord.Embed(title = message)
  await member.send(embed=embeddm)
  await ctx.channel.purge(limit=1)
  await ctx.send("Message Sent!!!")


# send roastlistpy
@client.command(aliases=["sr"])
async def sendroast(ctx, member:discord.Member):
  message = random.choice(roastlistpy)
  author = ctx.author.name
  embeddm = discord.Embed(title = message, description = f"Sent by: {author}")
  await member.send(embed=embeddm)
  await ctx.channel.purge(limit=1)
  await ctx.send("Roast Sent")

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


# Beg
@client.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def beg(ctx):
  if ctx.author.name in db.keys():
    afb = random.randint(1, 100)
    abrn = db[ctx.author.name] + afb
    db[ctx.author.name] = abrn
    em = discord.Embed(title = "Here you little peasant", description = f'You got given {afb} duckcoins')
    await ctx.send(embed = em)
  else:
    await ctx.send(embed=discord.Embed(title = "Looks like you don't have an account, Where do you think im gonna put the money? To create one: .createacc"))



# Admin Commands

# List Keys
@client.command()
async def listkeys(ctx):
  if ctx.author.name == "FusionSid":  
    keys = db.keys()
    await ctx.send(keys)
  else:
    await ctx.send("You dont have permission to use this command")

# Delete Key
@client.command()
async def delkey(ctx, *, key): 
  if ctx.author.name == "FusionSid":
    dkey = key
    del db[dkey]
    await ctx.send("done")
  else: 
    await ctx.send("You dont have permission to use this command")


# Key value
@client.command()
async def keyval(ctx, *, key):
  if ctx.author.name == "FusionSid":
    value = db[key]
    await ctx.send(value)
  else:
    await ctx.send("You dont have permission to use this command")


# Eat Messages 
@client.command(aliases=['eatm'])
async def eatmessage(ctx, ammount : int):
  if ctx.author.name == "FusionSid":
    await ctx.channel.purge(limit=ammount)
    await ctx.send("Yum!")
  else:
    await ctx.send("You dont have permission to use this command")



# Help and Errors

@client.group(invoke_without_command=True, aliases=["duckhelp", "help"])
async def duckcommandhelp(ctx):
  em = discord.Embed(title = "__**Duck Help**__", description = "use .help <command> for extended info on command", color = ctx.author.color)

  em.add_field(name = "Cult", value = "jc, lc, lcm")
  em.add_field(name = "Lol", value = "8ball, ducksearch, dm")
  em.add_field(name = "Roast", value = "duckroast, sendroast")
  em.add_field(name = "Duckcoin", value = "createacc, bal, beg")
  em.add_field(name = "More Help:", value = "Dm FusionSid")
  await ctx.send(embed = em)


@duckcommandhelp.command()
async def jc(ctx):
  em = discord.Embed(title = "Join Cult", description = "Joins the duck cult", color = ctx.author.color)
  em.add_field(name = "Command", value = ".jc <@name>")
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
  clembed.add_field(name = "\nFor information about command:", value=".help <commandname(without . prefix)>\n")
  clembed.add_field(name = "Example(for help about the duckroast command):", value=".help duckroast")
  clembed.add_field(name = "For any help:", value=".help")
  await ctx.send(embed=clembed)

# Errors

@client.event
async def on_command_error(ctx, error): 
  if isinstance(error, CommandOnCooldown):
    em = discord.Embed(title = "Wow buddy, Slow it down\nThis command is on cooldown", description = f'Try again in {error.retry_after:,.2f}seconds.') 
    await ctx.send(embed=em)

  elif isinstance(error, CommandNotFound):
    em = discord.Embed(title = "Command not found", description = "This command either doesn't exist, or you typed it wrong.\n.commands to see list of commands")
    await ctx.send(embed=em)

  elif isinstance(error, MissingRequiredArgument):
    em = discord.Embed(title = "Missing a requred value/arg", description = "You haven't passed in all value/arg")
    await ctx.send(embed=em)


# Run 
keep_alive()
client.run(os.environ['Token'])