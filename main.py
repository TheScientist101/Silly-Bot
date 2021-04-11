import discord
import requests
import json
import os
from lxml import html
from better_profanity import profanity
from bill import insult
from discord.ext import commands

client = commands.Bot(command_prefix="", case_insensitive=True)

if not "TOKEN" in os.environ:
    print("Please set the TOKEN environment variable.")
    os._exit(1)


@client.event
async def on_ready():
    print("Bot is ready")


@client.command()
async def hello(ctx):
    await ctx.send(
        "Hello there!!! Psst, guys, this {0.author.mention} kid seems dumb.".format(
            ctx.message
        )
    )


@client.command()
async def roast(ctx):
    profanity.load_censor_words()
    await ctx.send(profanity.censor("You are a " + insult()))


@client.command()
async def compliment(ctx):
    profanity.load_censor_words()
    await ctx.send(
        profanity.censor(
            [
                e.text_content()
                for e in html.fromstring(
                    requests.get(
                        "http://toykeeper.net/programs/mad/compliments",
                    ).text
                ).xpath("//h3")
            ][0].replace("\n", "")
        )
    )


@client.command()
async def meme(ctx):
    memejson = json.loads(requests.get("https://meme-api.herokuapp.com/gimme").text)
    while memejson["nsfw"] == True:
        memejson = json.loads(requests.get("https://meme-api.herokuapp.com/gimme").text)
    await ctx.send(embed=discord.Embed().set_image(url=memejson["url"]))

client.run(os.environ["TOKEN"])
