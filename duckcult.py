lol = ["
# Duck Hunger Cowntdown

hunger = 100
db["hunger"] = hunger

while hunger > 0:
  t.sleep(5)
  hunger = hunger - 1
  db["hunger"] = hunger

@client.command(aliases=["feed"])

async def feedduck(ctx):
    
  if hunger >= 100:
    await ctx.send("Duck is full right now")
  if hunger < 100:
    hunger = hunger + 1
    db["hunger"] = hunger
    await ctx.send("Thank you for feeding me\nI've decided to let you live")

@client.command(aliases=["hunger"])
async def checkhunger(ctx):
  await ctx.send(f'Duck Hunger: {hunger}')"]