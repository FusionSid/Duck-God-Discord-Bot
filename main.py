import os
import discord
from discord.ext import commands
import random
from keep_alive import keep_alive
from replit import db
from googleapiclient.discovery import build
from roastlist import roasts

# Please Don't Ruin This Bot

isapi_key = "AIzaSyCj52wnSciil-4JPd6faOXXHfEb1pzrCuY"

prefix = '.'

client = commands.Bot(prefix)

# Bot is online
@client.event
async def on_ready():
  await client.change_presence(activity=discord.Game("Hunting Frogs"))
  print("A wild duck god has spawned\n\nDuck god is ready to eat")


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
  await ctx.send(f'{leavingmember} has left the cult')


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


# Eat Messages 
@client.command(aliases=['eatm'])
async def eatmessage(ctx, ammount : int):
  if ctx.author.name == "FusionSid" or "kevinsoup721":
    await ctx.channel.purge(limit=ammount)
    await ctx.send("Yum!")
  else:
    ctx.send("You dont have permission to do that")


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
  await ctx.send(f'__Duck 8 Ball__\n\nQuestion: {question}\nAnswer: {random.choice(_8ballans)}')


# Duck Roast
@client.command(aliases=["rm"])
async def duckroast(ctx):
  roast = random.choice(roasts)
  await ctx.send(roast)

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


# Command list
@client.command(aliases=["commandslist"])
async def commands(ctx):
  commandslist = "__List of Duck Bot Commands__\n\n.jc [@name] = Registers your name in the duck cult member database.\n.lc [index] = Removes your name from the data base (Useless command, no one wants to leave the duck god).\n.ducksearch [yoursearch] = searches for an image\n.8ball [question] = uses the magical 8 ball to answers you life questions\n.duckroast = Roast you\n.duckhelp = asks for help\n.lcm = Lists all members of the duck cult (frogs stay away from these people if you wanna live)\n\nThats all the commands at the moment, When a new command is added it will be added to the list."
  await ctx.send(commandslist)


# .Help
@client.command()
async def duckhelp(ctx):
  await ctx.send("__Duck Bot Help__\n\nIf you need help DM FusionSid,\n\nIf you need a list of commands: .commands or .commandslist")


# Errors
@client.event
async def on_command_error(ctx, error):
  insultswrongcmd = ["Are you dumb?", "U retarted?", "Do me a favour and go get a brain cause you clearly dont have one", "Retard", "You fool", "Ducking Hell", "Duck You"]
  await ctx.send(random.choice(insultswrongcmd), "Ducking Hell\nBecause of you little ducker, I've encountered an error")


# Run 
keep_alive()
client.run(os.environ['Token'])