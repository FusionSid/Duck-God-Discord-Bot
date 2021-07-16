import discord
from discord.ext import commands
import youtube_dl

class music(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  @commands.command()
  async def join(self, ctx):
    if ctx.author.voice is None:
      await ctx.send("Get yo ass into a vc")
    voice_channel = ctx.author.voice_channel
    if ctx.voice_client is None:
      await voice_channel.connect()
    else:
      await ctx.voice_client.move_to(voice_channel)
    
  @commands.command()
  async def leave(self, ctx):
    await ctx.voice_client.disconect()
  
  @commands.command()
  async def play(self,ctx,url):
    ctx.voice_client.stop()
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    YDL_OPTIONS = {'format':'bestaudio'}
    vc = ctx.voice_client

    with youtube_dl.Youtube(YDL_OPTIONS) as ydl:
      info = ydl.extract_info(url, download=False)
      url2 = info['format'][0]['url']
      source = await discord.FFmpegOpusAudip.from_probe(url2, **FFMPEG_OPTIONS)
      vc.play(source)

  @commands.command()
  async def pause(self, ctx):
    await ctx.voice_client.pause()
    await ctx.send("Paused")

  @commands.command()
  async def resume(self, ctx):
    await ctx.voice_client.resume()
    await ctx.send("Resumed")

def setup(client):
  client.add_cog(music(client))