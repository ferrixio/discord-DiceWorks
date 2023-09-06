#### Dice Generator for Discord ####
#©Samuele Ferri 2023      Bot version: 3.2.1

import discord
from discord.ext import commands
from os import getenv
from dotenv import load_dotenv
import diceBlock as DB
from utilities import ServerUtilities as SU

load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')

intento = discord.Intents.all()   #threading to handle on_event status
acty = discord.Activity(type=discord.ActivityType.listening) #defunes activity
bot = commands.Bot(command_prefix="!", intents=intento, activity=acty, status=discord.Status.idle)
bot.remove_command("help")

##### BEGINNING AND EVENT #####
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.group(invoke_without_permission=True)
async def help(ctx,*arg):
    """Custom help command with Embed"""
    em = SU.custom_help(arg, bot.user.name)
    await ctx.channel.send(embed=em)


@bot.event
async def on_member_join(member):
    """Handling welcome message for Otaku's House"""

    sentence = SU.welcome().format(member.mention)

    if member.guild.id == int(getenv('OTAKUS_GUILD')):
        await bot.get_channel(int(getenv('chat_in_OH'))).send(sentence)
    
    elif member.guild.id == int(getenv('TEST_GUILD')): 
        await bot.get_channel(int(getenv('chat_in_test'))).send(sentence)


@bot.event
async def on_message(ctx):
    """Function to handle some events during chitchat"""
    if ctx.author.id==int(getenv('BOT')):
        pass

    if "master" in ctx.content or "Master" in ctx.content:
        response=SU.master(ctx.author.global_name,ctx.author.id)
        await ctx.channel.send(response)

    elif "fate" in ctx.content:
        await ctx.channel.send(f'Le fate sono sempre dalla tua parte, {ctx.author.global_name} :smirk:')

    elif "soap" in ctx.content:
        await ctx.channel.send("Sto piangendo dalla gioia! È stato davvero eccezionale, bellissimo, MERAVIGLIOSO!!! :cry:")

    #needs to make the bot realise that other commands may arrive
    await bot.process_commands(ctx)


##### COMMAND LIST #####
@bot.command()
async def tira(ctx, *arg):
    """Standard command to roll dice"""
    
    try:
        R,S = DB.standard_roll(list(arg))
        if not S:
            await ctx.channel.send(R)
        else:
            if len(S)==1:
                S=S[0]
            await ctx.channel.send(f"Tiro di {ctx.message.author.global_name}: {R} totale: {S}")

    except:
        await ctx.channel.send("Type error")


@bot.command()       
async def adv(ctx, *arg):
    """Command to resolve advantage rolls"""

    try:
        R,S,funny = DB.van_svg(list(arg),"adv",ctx.message.author.global_name)
    
        if not S:
                await ctx.channel.send(R)
        else:
            #non mettere la virgola prima di totale perché c'è già nell'output
            if len(S)==1:
                S=S[0]

            await ctx.channel.send(f'{funny} {R} quindi {S}')

    except:
        await ctx.channel.send("Type error")


@bot.command()       
async def dis(ctx, *arg):
    """Command to resolve disavantage rolls"""

    try:
        R,S,funny = DB.van_svg(list(arg),"dis",ctx.message.author.global_name)
    
        if not S:
                await ctx.channel.send(R)
        else:
            #non mettere la virgola prima di totale perché c'è già nell'output
            if len(S) == 1:
                S = S[0]

            await ctx.channel.send(f'{funny} {R} quindi {S}')

    except:
        await ctx.channel.send("Type error")      


@bot.command()
async def stats(ctx, arg):
    """Command to generate stats for dnd 5e"""

    try:
        text = ""
        R,S = DB.stats(int(arg))
        for i in R:
            text += i
            copy = i.split('\t')   #looking for 18 & 3. Char " x" is needed because of the nature of command split 
            text = text + ("\t :four_leaf_clover:")*(copy[1] == " 18") + ("\t :broken_heart:")*(copy[1] == " 3") + "\n"
        
        await ctx.channel.send(f"{ctx.message.author.global_name}, queste sono le stats che mi hai chiesto" + 
                               f" (è già stato rimosso il dado col valore più basso)\n" + text)

        if S:
            await ctx.channel.send(f'La distanza dalla serie standard è {S}')

    except:
        await ctx.channel.send("Type error")


@bot.command()
async def superstats(ctx):
    """Command to roll 3 set of 6-stats simultaneously"""

    await ctx.channel.send(f"{ctx.message.author.global_name}, le tue superstats sono\n{DB.superstats()}")


@bot.command()       
async def tpc(ctx, *arg):
    """Command to roll only 1d20"""
    A = ['1d20']+list(arg)
    try:
        R,S = DB.standard_roll(A)
        await ctx.channel.send(f"{ctx.message.author.global_name}'s tpc: {R}\t totale: {S}")

    except:
        await ctx.channel.send("Type error")
        

@bot.command()       
async def coin(ctx):
    """Command to toss a coin"""

    c = DB.coin()
    if c == 'in piedi':
        await ctx.channel.send(f"Ohibò! La moneta di {ctx.message.author.global_name} dev'essere truccata... si è fermata `{c}`")
        return
    
    await ctx.channel.send(f"{ctx.message.author.global_name}, è uscito `{c}`")


@bot.command()
async def forall(ctx,*arg):
    """Command to roll multuple dice and add modifiers to each roll"""
    
    try:
        R,S = DB.forall(list(arg))
        if not S:
            await ctx.channel.send(R)
        else:
            if len(S) == 1:
                S = S[0]
            await ctx.channel.send(f"Forall di {ctx.message.author.global_name}: {R} totale: {S[1:-1]}")

    except:
        await ctx.channel.send("Type error")


@bot.command()
async def cento(ctx):
    """Command to roll only 1d100"""
    from random import randint
    await ctx.channel.send(f"Tiro percentuale di {ctx.message.author.global_name}: `[{randint(1,100)}]")


@bot.command()
async def elvenchad(ctx,*arg):
    """Command to handle elven accuracy"""
    A=['2d20']+list(arg)
    try:
        R,extra,remake,elven_acc=DB.elvenacc(A)
        if not extra:
            await ctx.channel.send(R)

        #If there is a 20, sends the giga-chad gif
        if 20 in remake:
            await ctx.channel.send('https://tenor.com/view/giga-chad-gif-23143840')

        await ctx.channel.send(f"Elvenchad di {ctx.message.author.global_name}: `{R}` + `{extra}` = `{remake}`,\t quindi: {elven_acc}")
            
    except:
        await ctx.channel.send("Type error")


@bot.command()
async def explode(ctx,*arg):
    """Command to roll explosive dice"""

    try:
        R,S = DB.explosive_dice(list(arg))

        if not S:
            await ctx.channel.send(R)
        else:
            if len(S) == 1:
                S = S[0]
            await ctx.channel.send(f"Lc di {ctx.message.author.global_name}: {R} quindi {S}")

    except:
        await ctx.channel.send("Type error")


##### UTILITY COMMAND LIST #####
@bot.command()
@commands.cooldown(5,30)
async def loli(ctx):
    """Command to get cute loli pictures as direct message"""
    await ctx.author.send(SU.loli())


@bot.command()
async def member(ctx):
    """Coomand to count the users in current guild. Doesn't include bots"""

    if ctx.guild is None:
        await ctx.send("We are in a private chat")
        return None
    
    await ctx.author.send(f'Number of members in server {ctx.guild.name} = '+\
                          f'{len([m for m in ctx.guild.members if not m.bot])}')


@bot.command()
@commands.is_owner()
async def login(ctx):
    """Command for bot's owner to get the list of servers in which the bot is in"""
    ans=''
    for guild in bot.guilds:
        ans += f'{guild.name} (id: {guild.id})\n'
    await ctx.author.send(f'The bot is connected to the following servers:\n{ans}')


@bot.command()
async def reset(ctx):
    """Command to reset the rng seed"""
    DB.reset_seed()
    await ctx.channel.send(f"Random number generator seed reset by {ctx.message.author.global_name}")


@bot.command()
async def ping(ctx):
    """Command that sends the bot latency"""
    await ctx.channel.send(f"Bot current latency = {round(bot.latency, 4)} sec")


bot.run(TOKEN)      # Starting the bot
