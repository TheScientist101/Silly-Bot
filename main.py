import discord
import requests
import json
import os
import threading
from lxml import html
from better_profanity import profanity
from bill import insult
from discord.ext import commands


threading.Thread(os.system("gunicorn app:app")).start()

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
        f"Hello there!!! Psst, guys, this {ctx.author.mention} kid seems dumb."
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
                await ctx.send(
                    "Clean memes were not found after 10 tries, please try again."
                )
                return
        profanity.load_censor_words()
        await ctx.send(
            embed=discord.Embed(
                title=profanity.censor(memejson["title"]), url=memejson["postLink"]
            ).set_image(url=memejson["url"])
        )


@client.command()
async def say(ctx, message="", channel: discord.TextChannel = ""):
    if message == "":
        await ctx.send("Bruh, what do I say?")
        return
    if channel == "":
        channel = ctx
    await channel.send(f"{message}\n\n\n\nSent By {ctx.message.author.mention}.")


@client.command()
async def channel(ctx, name=""):
    if name != "":
        await ctx.guild.create_text_channel(name)
        await ctx.send(f"{name} was created. Ok?")
    else:
        await ctx.send("What channel do I make, bruh?")


client.run(os.environ["TOKEN"])
