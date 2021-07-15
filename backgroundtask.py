from replit import db
from discord.ext import tasks

db["hunger"] = 100

@tasks.loop(seconds=3600)
async def duckbotlowhunger(ctx):
  hungerrn = db["hunger"] - 5
  db["hunger"] = hungerrn
  if hungerrn <= 0:
    await ctx.send("duck god has died")
  if hungerrn == 75:
    await ctx.send("duck god hunger level is at 75%")
  if hungerrn == 50:
    await ctx.send("duck god hunger level is at 50%")
  if hungerrn == 25:
    await ctx.send("duck god hunger level is at 25%")
  if hungerrn == 15:
    await ctx.send("duck god hunger level is at 15%")
  if hungerrn == 10:
    await ctx.send("duck god hunger level is at 10%")
  if hungerrn == 5:
    await ctx.send("duck god hunger level is at 5%")

