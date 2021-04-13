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
async def meme(ctx, args=""):
    memejson = json.loads(
        requests.get("https://meme-api.herokuapp.com/gimme/" + args).text
    )
    if not "url" in memejson:
        await ctx.send("The subreddit you gave me is currently not available.")
    else:
        i = 0
        while memejson["nsfw"] == True:
            memejson = json.loads(
                requests.get("https://meme-api.herokuapp.com/gimme/" + args).text
            )
            i += 1
            if i == 10:
                ctx.send("Clean memes were not found after 10 tries, please try again.")
                break
        profanity.load_censor_words()
        await ctx.send(
            embed=discord.Embed(
                title=profanity.censor(memejson["title"]), url=memejson["postLink"]
            ).set_image(url=memejson["url"])
        )


client.run(os.environ["TOKEN"])
