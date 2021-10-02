import os
import discord
from discord.ext import commands
import random
from discord.ext.commands import (
    CommandNotFound, MissingRequiredArgument, CommandOnCooldown)
from discord.ext import tasks


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @client.command()
    async def c(self, ctx, num: int):
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
    async def _8ball(self, ctx, *, question):
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
    async def ducksearch(self, ctx, *, search):
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


    def calculator(self, num1, operator, num2):
        if operator == "+":
            return num1 + num2
        elif operator == "-":
            return num1 - num2
        elif operator == "/":
            return num1 / num2
        elif operator == "x":
            return num1 * num2


    @client.command()
    async def calc(self, ctx, n1: int, op, n2: int):
        ans = calculator(n1, op, n2)
        await ctx.send(embed=discord.Embed(title='Calculator Duck:', description=ans))

    # Message User


    @client.command(aliases=["dm"])
    async def duckdm(self, ctx, member: discord.Member, *, message):
        embeddm = discord.Embed(title=message)
        await member.send(embed=embeddm)
        await ctx.channel.purge(limit=1)

def setup(client):
    client.add_cog(Help(client))