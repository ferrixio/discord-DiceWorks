#### Dice Generator for Discord ####
#©Samuele Ferri 2024      Bot version: 3.6.0

import discord
from discord.ext import commands
from os import getenv
from dotenv import load_dotenv
from utilities import ServerUtilities

load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')

intento = discord.Intents.all()   #threading to handle on_event status
acty = discord.Activity(type=discord.ActivityType.listening) #defines activity
bot = commands.Bot(command_prefix="!", intents=intento, activity=acty, status=discord.Status.idle)
bot.remove_command("help")

##### BEGINNING AND EVENT #####
@bot.event
async def on_ready():
    await bot.load_extension("commands")     # load commands
    owner = await bot.fetch_user(getenv('FERRI'))   # retrieve owner user by its ID
    await owner.send("The bot has successfully connected to Discord")

@bot.event
async def on_member_join(member):
    """Handling welcome message for Otaku's House"""
    sentence = ServerUtilities.welcome().format(member.mention)

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
        response=ServerUtilities.master(ctx.author.global_name,ctx.author.id)
        await ctx.channel.send(response)

    elif "fate" in ctx.content:
        await ctx.channel.send(f'Le fate sono sempre dalla tua parte, {ctx.author.global_name} :smirk:')

    elif "soap" in ctx.content:
        await ctx.channel.send("Sto piangendo dalla gioia! È stato davvero eccezionale, bellissimo, MERAVIGLIOSO!!! :cry:")

    #needs to make the bot realise that other commands may arrive
    await bot.process_commands(ctx)

@bot.event
async def on_command_error(ctx, error):
    """Method that handles the errors"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Invalid command")
    else:
        owner = await bot.fetch_user(getenv('FERRI'))
        await owner.send(error)

##### UTILITY COMMAND LIST #####
@bot.group(invoke_without_permission=True)
async def help(ctx,*arg):
    """Custom help command with Embed. Also it sends a memo to the owner"""
    em = ServerUtilities.custom_help(arg, bot.user.name)
    await ctx.channel.send(embed=em)
    if ctx.author.id == int(getenv('FERRI')):
        await ctx.author.send('Ricordati che hai anche il gruppo ferri guilds/upgrade/send')

@bot.command()
async def member(ctx):
    """Command to count the users in current guild. Doesn't include bots"""
    if ctx.guild is None:
        await ctx.send("We are in a private chat")
        return None
    
    await ctx.author.send(f'Number of members in server {ctx.guild.name} = '+\
                          f'{len([m for m in ctx.guild.members if not m.bot])}')
    
@bot.command()
async def ping(ctx):
    """Command that sends the bot latency"""
    await ctx.channel.send(f"Bot current latency = {round(bot.latency, 4)} sec")

@bot.command()
async def redo(ctx):
    """Command to redo another command"""
    message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    t = message.content.split()
    if t[0] == '!redo':
        await ctx.channel.send("You can't redo a redo")
    elif '!' not in t[0]:
        await ctx.channel.send("No command to redo")
    else:
        ctx.command = bot.get_command(t[0].replace('!',''))
        await ctx.invoke(ctx.command, *t[1:])

@bot.command()
async def spell(ctx):
    """Prints the list of available spells and their syntax to be casted"""
    em = ServerUtilities.spellList()
    await ctx.channel.send(embed=em)
    
    
##### OWNER-ONLY COMMAND GROUP #####
@bot.group(invoke_without_command=True)
async def ferri(ctx):
    await ctx.send('Subcommand not found')

@ferri.command()
@commands.is_owner()
async def guilds(ctx):
    """Command for bot's owner to get the list of servers in which the bot is in"""
    ans=''
    for guild in bot.guilds:
        ans += f'{guild.name} (id: {guild.id})\n'
    await ctx.author.send(f'The bot is connected to the following servers:\n{ans}')

@ferri.command()
@commands.is_owner()
async def upgrade(ctx, *, msg):
    """Command that sends to all guilds that the bot was updated"""
    em = ServerUtilities._getChangelog(bot.user.name, msg)
    for guild in bot.guilds:
        for channel in guild.text_channels:
            try:
                await channel.send(embed=em)
            except Exception:
                continue
            else:
                break    

@ferri.command()
@commands.is_owner()
async def send(ctx, *, msg):
    """Command for bot's owner to send a message to ALL guilds where the bot is currently active"""
    em = ServerUtilities._text2Embed(bot.user.name, msg)
    for guild in bot.guilds:
        for channel in guild.text_channels:
            try:
                await channel.send(embed=em)
            except Exception:
                continue
            else:
                break


bot.run(TOKEN)      # Starting the bot