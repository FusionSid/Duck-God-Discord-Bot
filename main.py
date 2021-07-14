import os
import discord
from discord.ext import commands
import random
from keep_alive import keep_alive
from replit import db
import json
import time as t

# Please Don't Ruin This Bot

prefix = '.'

client = commands.Bot(prefix)

# Bot is online
@client.event
async def on_ready():
  await client.change_presence(activity=discord.Game("Eating Frogs"))
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
  if ctx.author.name == "FusionSid":
    await ctx.channel.purge(limit=ammount)
    await ctx.send("Yum!")
  else:
    ctx.send("You dont have permission to do that")


# Duck Hunger
db["dhb"] = 0
@client.command(aliases=['feed'])
#async def feedduck(ctx):


# Errors
@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
        insultswrongcmd = ["Are you dumb?", "U retarted?", "Do me a favour and go get a brain cause you clearly dont have one", "Retard", "You fool", "Ducking Hell", "Duck You"]

        await ctx.send(f'{random.choice(insultswrongcmd)} Thats not a real command')
  else:
    await ctx.send("Ducking Hell, I've encountered an error")


# Run 
keep_alive()
client.run(os.environ['Token'])