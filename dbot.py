import discord 
from discord.ext import commands
import pymongo
import random
import config
from pymongo import MongoClient
cluster = MongoClient(config.mongo_url)
db = cluster["logins"]
collection = db["logins"]
collection1 = db["keys"]

client = commands.Bot(command_prefix = '!')
client.remove_command('help')

@client.command()
async def delacc(ctx, username):
    if collection.find_one({"username": username}) is not None:
        if collection.delete_one({"username": username}):
            await ctx.send("**Account Deleted:** `" + username + "`")
        else:
            await ctx.send("**Account Deletion Failed**")
    else:
        await ctx.send("**Account Not Found**")

@client.command()
async def givesub(ctx, username):
    if collection.find_one({"username": username, "sub": False}) is not None:
        if collection.update_one({"username": username}, {"$set": {"sub": True}}):
            await ctx.send("**Subscription Granted:** `" + username + "`")
        else: 
            await ctx.send("**Subscription Failed**")
    else:
        await ctx.send("**Account Not Found**")

@client.command()
async def removesub(ctx, username):
    if collection.find_one({"username": username, "sub": True}) is not None:
        if collection.update_one({"username": username}, {"$set": {"sub": False}}):
            await ctx.send("**Subscription Removed:** `" + username + "`")
        else: 
            await ctx.send("**Subscription Failed**")
    else:
        await ctx.send("**Account Not Found**")

@client.command()
async def genkey(ctx):
    chars = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456%()`$£! "
    key=""
    for x in range(0,15):
        charc = random.choice(chars)
        key  = key + charc
    print(key)

    post = {"key": key, "redeemed": False}
    if collection1.insert_one(post):
        await ctx.send("**Key Generated: ** `" + key + "`")
        
    else:
        await ctx.send("**Key Generation Failed**")

@client.command()
async def accountinfo(ctx, username):
    if username != "":
        #get creation date of account
        if collection.find_one({"username": username}) is not None:
            creation = collection.find_one({"username": username})["creation"]
            #get subscription status of account
            if collection.find_one({"username": username, "sub": True}) is not None:
                sub = "Subscribed"
            else:
                sub = "Not Subscribed"
            #get admin status of account
            await ctx.send("**Account Info:** `" + username + "`\n**Creation Date:** `" + creation + "`\n**Subscription Status:** `" + sub +"`")
        else:
            await ctx.send("**Account Not Found**")


@client.command()
async def help(ctx):
        embed = discord.Embed(title="Help", color=0xFF0000) 
        embed.add_field(name="delacc", value="!delacc (username)", inline=False)
        embed.add_field(name="genkey", value="!genkey", inline=False)
        embed.add_field(name="givesub", value="!givesub (username)", inline=False)
        embed.add_field(name="removesub", value="!removesub (username)", inline=False)
        embed.add_field(name="accountinfo", value="!accountinfo (username)", inline=False)
        embed.set_footer(text="Made by TB#5767 | DM me for help")
        await ctx.send(embed=embed)


client.run(config.token)