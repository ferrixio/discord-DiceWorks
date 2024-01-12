from gettext import translation
from discord.ext import commands
from json import load
import diceBlock as DB

@commands.command()
async def tira(ctx, *arg):
    """Standard command to roll dice"""

    try:
        R,S = DB.standard_roll(list(arg))
        if not S:
            await ctx.channel.send(R)
        else:
            #non mettere la virgola prima di totale perché c'è già nell'output
            if len(S)==1:
                S=S[0]
            await ctx.channel.send(f"Tiro di {ctx.message.author.global_name}: {R} totale: {S}")

    except:
        await ctx.channel.send("Type error")


@commands.command()       
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


@commands.command()       
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


@commands.command()
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


@commands.command()
async def superstats(ctx):
    """Command to roll 3 set of 6-stats simultaneously"""
    
    await ctx.channel.send(f"{ctx.message.author.global_name}'s superstats:\n{DB.superstats()}")


@commands.command()       
async def tpc(ctx, *arg):
    """Command to roll only 1d20"""
    A = ['1d20']+list(arg)
    try:
        R,S = DB.standard_roll(A)
        if len(S)==1:
            S=S[0]
        await ctx.channel.send(f"{ctx.message.author.global_name}'s tpc: {R} totale: {S}")

    except:
        await ctx.channel.send("Type error")


@commands.command()
async def ts(ctx, *arg):
    """Command to perform saving throws. The reqired character to properly activate the saving
    throw is '<', since a successful st is greater or equal to DC."""

    # looking for the DC
    dcPieces, temp = [], []
    for i in range(len(list(arg))):
        if '<' in arg[i]:
            dcPieces.append(arg[i])
            try:
                dcPieces.append(arg[i+1])
            except IndexError:
                pass
            break
        temp.append(arg[i])
    
    try:
        dc = int(float(((''.join(dcPieces)).split('<')[1])))
        if dc < 0:  # negative dc does not have any sense...
            dc = 0
    except:
        dc = 0

    A = ['1d20']+temp
    try:        
        R,S = DB.standard_roll(A)
        if len(S)==1:
            S=S[0]
        ans = ''
        if dc:
            ans = f' over {dc} -> ' + 'Success!'*(S>=dc) + 'Failed'*(S<dc)
        await ctx.channel.send(f"{ctx.message.author.global_name}'s saving throw: {R} {S}{ans}")
    except:
        await ctx.channel.send("Type error")


@commands.command()       
async def coin(ctx):
    """Command to toss a coin"""

    c = DB.coin()
    if c == 'in piedi':
        await ctx.channel.send(f"Ohibò! La moneta di {ctx.message.author.global_name} dev'essere truccata... si è fermata `{c}`")
        return
    
    await ctx.channel.send(f"{ctx.message.author.global_name}, è uscito `{c}`")


@commands.command()
async def forall(ctx,*arg):
    """Command to roll multuple dice and add modifiers to each roll"""
    
    try:
        R,S = DB.forall(list(arg))
        if not S:
            await ctx.channel.send(R)
        else:
            if len(S) == 1:
                S = S[0]
            await ctx.channel.send(f"{ctx.message.author.global_name}'s forall: {R} totale: {S[1:-1]}")

    except:
        await ctx.channel.send("Type error")


@commands.command()
async def cento(ctx):
    """Command to roll only 1d100"""
    from random import randint
    await ctx.channel.send(f"{ctx.message.author.global_name}'s d100: `[{randint(1,100)}]`")


@commands.command()
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

        await ctx.channel.send(f"{ctx.message.author.global_name}'s elven accuracy: `{R}` + `{extra}` = `{remake}`,\t `->` {elven_acc}")
            
    except:
        await ctx.channel.send("Type error")


@commands.command()
async def explode(ctx,*arg):
    """Command to roll explosive dice"""

    try:
        R,S = DB.explosive_dice(list(arg))

        if not S:
            await ctx.channel.send(R)
        else:
            if len(S) == 1:
                S = S[0]
            await ctx.channel.send(f"{ctx.message.author.global_name}'s explosion: {R} `->` {S}")

    except:
        await ctx.channel.send("Type error")


@commands.command()
async def race(ctx, *arg):
    """Generates the height and weight of specified race"""
    try:
        term = ' '.join(arg)
        with open("variables.json", "r") as f:
            var = load(f)
            key = [k for k, val in var["race_translator"].items() if term in val].pop()
            table = var["dimension_table"][key]
            
        height, weight = DB.evaluateSize(table, key)
        await ctx.channel.send(f"{ctx.message.author.global_name}'s {key} sizes: {height} cm and {weight} kg")
    except:
        await ctx.channel.send("Type error")

@commands.command()
async def reset(ctx):
    """Command to reset the rng seed"""
    DB.reset_seed()
    await ctx.channel.send(f"Random number generator seed reset by {ctx.message.author.global_name}")



# this method must be here. It adds the commands to the bot
async def setup(bot):
    CMD_LIST = (tira, adv, dis, stats, superstats, tpc, ts, coin, forall, cento,
               elvenchad, explode, reset, race)
    
    for i in CMD_LIST:
        bot.add_command(i)