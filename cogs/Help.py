import os
import discord
from discord.ext import commands
import random
from discord.ext.commands import (
    CommandNotFound, MissingRequiredArgument, CommandOnCooldown)
from discord.ext import tasks


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @client.group(invoke_without_command=True, aliases=["duckhelp", "help"])
    async def duckcommandhelp(self, ctx):
        em = discord.Embed(title="__**Duck Help**__",
                        description="use .help <command> for extended info on command", color=ctx.author.color)

        em.add_field(name="__Cult__", value="jc, lc, lcm")
        em.add_field(name="__Fun/Questions__",
                    value="8ball, ducksearch, calc, duckroast, c")
        em.add_field(name="__Message__",
                    value="feedback, ducksearch, dm, sendroast")
        em.add_field(name="__Music__", value="play, skip, queue")
        em.add_field(name="__Duckcoin__",
                    value="send, bag, sell, buy, dep, with, shop, bal, beg, lb, gamble")
        em.add_field(name="__Source Code:__",
                    value="https://github.com/FusionSid/Duck-God-Discord-Bot")
        em.add_field(name="__More Help:__", value="Dm FusionSid")
        await ctx.send(embed=em)

    # Command list


    @client.command(aliases=["commandslist"])
    async def commands(self, ctx):
        clembed = discord.Embed(
            title="__List of Duck Bot Commands__", desciption=" ")
        clembed.add_field(name="\n__.jc__", value="Join cult")
        clembed.add_field(name="\n__.lc__", value="Leave cult")
        clembed.add_field(name="\n__.lcm__", value="List cult members")
        clembed.add_field(name="\n__.dm__", value="Duck God send DM")
        clembed.add_field(name="\n__.createacc__", value="Create Account")

        clembed.add_field(name="\n__.bal__", value="Balance")
        clembed.add_field(name="\n__.shop__", value="Shop")
        clembed.add_field(name="\n__.buy__", value="Buy")
        clembed.add_field(name="\n__.beg__", value="Beg")
        clembed.add_field(name="\n__.with__", value="Withdraw")
        clembed.add_field(name="\n__.dep__", value="Deposit")
        clembed.add_field(name="\n__.bag__", value="Bag")
        clembed.add_field(name="\n__.send__", value="Send Money")
        clembed.add_field(name="\n__.battle__", value="Duck Battle")
        clembed.add_field(name="\n__.gamble__", value="Gamble")
        clembed.add_field(name="\n__.sell__", value="Sell")

        clembed.add_field(name="\n__.8ball__", value="8ball")
        clembed.add_field(name="\n__.ducksearch__", value="Duck Search")
        clembed.add_field(name="\n__.duckroast__", value="Duck Roast")
        clembed.add_field(name="\n__.sendroast__", value="Send Roast")
        clembed.add_field(name="\n__.queue__", value="Queue")
        clembed.add_field(name="\n__.play__", value="Play Song")
        clembed.add_field(name="\n__.skip__", value="Skip Song")
        clembed.add_field(
            name="\n__.c__", value="Counting - only do in counting channel")
        clembed.add_field(name="\n__.calc__", value="Calculate.")
        clembed.add_field(name="\nFor information about command:",
                        value=".help <commandname(without . prefix)>\n")
        clembed.add_field(
            name="Example(for help about the duckroast command):", value=".help duckroast")
        clembed.add_field(name="For any help:", value=".help")
        await ctx.send(embed=clembed)

    # Custom Help per command


    @duckcommandhelp.command()
    async def jc(self, ctx):
        em = discord.Embed(
            title="Join Cult", description="Joins the duck cult", color=ctx.author.color)
        em.add_field(name="Command", value=".jc <@name>")
        await ctx.send(embed=em)


    @duckcommandhelp.command()
    async def skip(self, ctx):
        em = discord.Embed(
            title="Skip Song", description="Skips the song currently playing", color=ctx.author.color)
        em.add_field(name="Command", value=".skip")
        await ctx.send(embed=em)


    @duckcommandhelp.command()
    async def play(self, ctx):
        em = discord.Embed(
            title="Play song", description="Joins the duck cult", color=ctx.author.color)
        em.add_field(name="Command", value=".play <song name>")
        await ctx.send(embed=em)


    @duckcommandhelp.command()
    async def queue(self, ctx):
        em = discord.Embed(
            title="List Queue", description="Lists all the songs in the queue", color=ctx.author.color)
        em.add_field(name="Command", value=".q")
        await ctx.send(embed=em)


    @duckcommandhelp.command()
    async def sendroast(self, ctx):
        em = discord.Embed(
            title="Send Roast", description="Duck dms a roast to user of you choice", color=ctx.author.color)
        em.add_field(name="Command", value=".sendroast <@persontosendto>")
        await ctx.send(embed=em)


    @duckcommandhelp.command()
    async def lc(self, ctx):
        em = discord.Embed(
            title="Leave Cult", description="Leaves the duck cult", color=ctx.author.color)
        em.add_field(name="Command", value=".lc <index>\nIndex's start from 0")
        await ctx.send(embed=em)


    @duckcommandhelp.command()
    async def lcm(self, ctx):
        em = discord.Embed(title="List Cult Members",
                        description="Lists all duck member, Pings them too", color=ctx.author.color)
        em.add_field(name="Command", value=".lcm")
        await ctx.send(embed=em)


    @duckcommandhelp.command(aliases=["8ball"])
    async def _8ball(self, ctx):
        em = discord.Embed(
            title="8 Ball", description="Asks the magical 8 ball a question", color=ctx.author.color)
        em.add_field(name="Command", value=".8ball <question>")
        await ctx.send(embed=em)


    @duckcommandhelp.command()
    async def duckroast(self, ctx):
        em = discord.Embed(
            title="Duck Roast", description="Duck god roasts you", color=ctx.author.color)
        em.add_field(name="Command", value=".duckroast")
        await ctx.send(embed=em)


    @duckcommandhelp.command()
    async def c(self, ctx):
        em = discord.Embed(title="Counting", description="The number you type must be 1 greater than the previous number. If you type the same number, a number less or too more, count resets to zero", color=ctx.author.color)
        em.add_field(name="Command", value=".c <number>")
        await ctx.send(embed=em)


    @duckcommandhelp.command()
    async def ducksearch(self, ctx):
        em = discord.Embed(title="Duck Search\nThe Best Command",
                        description="Searches the web for a image of you choice", color=ctx.author.color)
        em.add_field(name="Command", value=".ducksearch <search>")
        await ctx.send(embed=em)


    @duckcommandhelp.command()
    async def bal(self, ctx):
        em = discord.Embed(title="Duck Balance",
                        description="Displays you duckcoin bank balance", color=ctx.author.color)
        em.add_field(name="Command", value=".bal")
        await ctx.send(embed=em)


    @duckcommandhelp.command()
    async def dm(self, ctx):
        em = discord.Embed(
            title="Duck DM", description="Duck god DMs user of your choice", color=ctx.author.color)
        em.add_field(name="Command", value=".dm <@user> <message>")
        await ctx.send(embed=em)


    @duckcommandhelp.command()
    async def createacc(self, ctx):
        em = discord.Embed(title="Create Account",
                        description="Creates you a duck bank account", color=ctx.author.color)
        em.add_field(name="Command", value=".createacc")
        await ctx.send(embed=em)


    @duckcommandhelp.command()
    async def beg(self, ctx):
        em = discord.Embed(
            title="Beg", description="Begs for duckcoins", color=ctx.author.color)
        em.add_field(name="Command", value=".beg")
        await ctx.send(embed=em)


    @duckcommandhelp.command()
    async def calc(self, ctx):
        em = discord.Embed(
            title="Calculator", description="Performs simple caluculations", color=ctx.author.color)
        em.add_field(name="Command",
                    value=".calc <num1> <operator> <num2>\nOperators: +, -, /, x")
        await ctx.send(embed=em)

def setup(client):
    client.add_cog(Help(client))