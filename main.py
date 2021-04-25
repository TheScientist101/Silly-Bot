import discord
import requests
import json
import os
import shlex
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


@client.event
async def on_message(message):
    ctx = await client.get_context(message)
    command = message.content.split()[0].lower()
    commands = ['hello', 'roast', 'compliment', 'meme', 'say']
    if command in commands 
    await eval(
        command + f"(ctx, '{message.content.partition(' ')[2]}')"
    )
    print("await " + message.content.split()[0] + f"(ctx)")


async def hello(ctx, args=""):
    await ctx.send(
        f"Hello there!!! Psst, guys, this {ctx.author.mention} kid seems dumb."
    )


async def roast(ctx, args=""):
    profanity.load_censor_words()
    await ctx.send(profanity.censor("You are a " + insult()))


async def compliment(ctx, args=""):
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


async def say(ctx, args=""):
    if len(shlex.split(args)) >= 2:
        if shlex.split(args)[1].startswith("<"):
            channel = print(
                client.get_channel(
                    shlex.split(args)[1].strip("<").strip(">").strip("#")
                )
            )
        else:
            channel = discord.utils.get(
                ctx.guild.text_channels, name=shlex.split(args)[1]
            )
    else:
        channel = ""
    message = shlex.split(args)[0]
    if message == "":
        await ctx.send("Bruh, what do I say?")
        return
    if channel == "":
        channel = ctx
    await channel.send(f"{message}\n\n\n\nSent By {ctx.message.author.mention}.")


client.run(os.environ["TOKEN"])
