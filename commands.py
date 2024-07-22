from discord.ext import commands
from random import randint
from random import choice
import diceBlock as DB
from diceBlock import VARIABLES as var

##### ROLLS COMMANDS #####
@commands.command(aliases=('vantaggio',))
async def adv(ctx, *arg):
    """Command to resolve advantage rolls"""
    try:
        R,S,funny = DB.van_svg(list(arg),"adv",ctx.message.author.global_name)
        await ctx.channel.send(f'{funny} {R} `->` {S}')

    except Exception as e:
        await ctx.reply(e, mention_author=False)

@commands.command(aliases=('100',))
async def cento(ctx):
    """Command to roll only 1d100"""
    from random import randint
    result = randint(1,100)
    match result:
        case 69:
            result = ':peach:'
        case 100:
            result = ':100:'
        case _ :
            result = f'`[{result}]`'
    await ctx.channel.send(f"{ctx.message.author.global_name}'s d100: {result}")

@commands.command(alises=('moneta',))
async def coin(ctx):
    """Command to toss a coin"""
    c = DB.coin()
    if c == 'in piedi':
        await ctx.channel.send(f"Ohibò! La moneta di {ctx.message.author.global_name} dev'essere truccata... si è fermata `{c}`")
        return
    
    await ctx.channel.send(f"{ctx.message.author.global_name}, è uscito `{c}`")

@commands.command(aliases=('svantaggio',))
async def dis(ctx, *arg):
    """Command to resolve disavantage rolls"""
    try:
        R,S,funny = DB.van_svg(list(arg),"dis",ctx.message.author.global_name)
        await ctx.channel.send(f'{funny} {R} `->` {S}')

    except Exception as e:
        await ctx.reply(e, mention_author=False)

@commands.command()
async def elvenchad(ctx,*arg):
    """Command to handle elven accuracy"""
    A=['2d20']+list(arg)
    try:
        R,extra,remake,elven_acc=DB.elvenacc(A)
        #If there is a 20, sends the giga-chad gif
        if 20 in remake:
            await ctx.channel.send('https://tenor.com/view/giga-chad-gif-23143840')

        await ctx.channel.send(f"{ctx.message.author.global_name}'s elven accuracy: `{R}` + `{extra}` = `{remake}`,\t `->` {elven_acc}")     
    except Exception as e:
        await ctx.reply(e, mention_author=False)

@commands.command(aliases=('lc',))
async def explode(ctx,*arg):
    """Command to roll explosive dice"""
    try:
        R,S = DB.explosive_dice(list(arg))
        await ctx.channel.send(f"{ctx.message.author.global_name}'s explosion: {R} `->` {S} :boom:")

    except Exception as e:
        await ctx.reply(e, mention_author=False)

@commands.command()
async def forall(ctx,*arg):
    """Command to roll multuple dice and add modifiers to each roll"""
    try:
        R,S = DB.forall(list(arg))
        await ctx.channel.send(f"{ctx.message.author.global_name}'s forall: {R} `->` {S[1:-1]}")

    except Exception as e:
        await ctx.reply(e, mention_author=False)

@commands.command()
async def jennystats(ctx, *arg):
    """Command to generate stats for dnd 5e in an alternative way with respect to !stats"""
    try:
        text = ""
        if not arg:
            arg = ('6',)
        R,serie,dist = DB.stats(int(''.join(arg)), jenny=True)
        for i in range(len(R)):
            text += R[i]
            text = text + ("\t :four_leaf_clover:")*(serie[i] == 18) + ("\t :broken_heart:")*(serie[i] == 3)+"\n"
        message = f"{ctx.message.author.global_name}'s requested jenny-statblock\n" +\
            text + f'Distance from standard serie = {dist}'*(bool(dist))
        await ctx.channel.send(message)

    except Exception as e:
        await ctx.reply(e, mention_author=False)

@commands.command(aliases=('character', 'char'))
async def pg(ctx, *arg):
    """Generates a pg (statblock and sizes) according to dnd 5e"""
    statBlock, statList, distance = DB.stats(6)  # generates the statblock in standard format
    statText = '\n'.join(statBlock)
    parameters = DB.parseKwargs(set(arg))
    
    # Generate the race
    dndRace = parameters["race"]
    if not dndRace:
        dndRace = choice(list(var["dimension_table"]))
    height, weight = DB.evaluateSize(var["dimension_table"][dndRace], dndRace)

    # Generate the class
    dndClass = parameters["class"]
    if not dndClass:
        dndClass = choice(list(var["classes"]))
        
    # Get the level
    dndLevel = parameters["level"]
    if not dndLevel:
        dndLevel = 1
    ap = DB._getAP(dndClass, dndLevel)

    # Build the output
    outputStr = f"{ctx.message.author.global_name}'s random character:\n" +\
        f"Lv {dndLevel}\t{dndClass}\t{dndRace} ({height} cm and {weight} kg)\n" +\
        f"{statText}\nThe distance from standard serie is {distance}, and " +\
        f"you have **{ap} extra ability score** to use"

    await ctx.channel.send(outputStr)

@commands.command(aliases=('razza', 'misure', 'misura'))
async def race(ctx, *arg):
    """Generates the height and weight of specified race"""
    try:
        term = ' '.join(arg)        
        race = DB.translateRace(term)
        height, weight = DB.evaluateSize(var["dimension_table"][race], race)
        await ctx.channel.send(f"{ctx.message.author.global_name}'s **{race}** sizes:\n:straight_ruler: {height} cm \t\t :scales: {weight} kg")

    except:
        await ctx.channel.send("I don't know this race")

@commands.command()
async def reset(ctx):
    """Command to reset the rng seed"""
    DB.reset_seed()
    await ctx.channel.send(f"Random number generator seed reset by {ctx.message.author.global_name} :recycle:")

@commands.command()
async def stats(ctx, *arg):
    """Command to generate stats for dnd 5e"""
    try:
        text = ""
        if not arg:
            arg = ('6',)
        R,serie,dist = DB.stats(int(''.join(arg)))
        for i in range(len(R)):
            text += R[i]
            text = text + ("\t :four_leaf_clover:")*(serie[i] == 18) + ("\t :broken_heart:")*(serie[i] == 3)+"\n"
        message = f"{ctx.message.author.global_name}'s requested statblock\n" +\
            text + f'Distance from standard serie = {dist}'*(bool(dist))
        await ctx.channel.send(message)

    except Exception as e:
        await ctx.reply(e, mention_author=False)
        
@commands.command()
async def superstats(ctx):
    """Command to roll 3 set of 6-stats simultaneously"""
    await ctx.channel.send(f"{ctx.message.author.global_name}'s superstats:\n{DB.superstats()}")

@commands.command(aliases=('roll',))
async def tira(ctx, *arg):
    """Standard command to roll dice"""
    try:
        R,S = DB.standard_roll(list(arg))
        await ctx.channel.send(f"Tiro di {ctx.message.author.global_name}: {R} `->` {S}")

    except Exception as e:
        await ctx.reply(e, mention_author=False)

@commands.command(aliases=('venti',))       
async def tpc(ctx, *arg):
    """Command to roll only 1d20"""
    A = ['1d20']+list(arg)
    try:
        R,S = DB.standard_roll(A)
        await ctx.channel.send(f"{ctx.message.author.global_name}'s tpc: {R} `->` {S}")

    except Exception as e:
        await ctx.reply(e, mention_author=False)

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
        ans = ''
        if dc:
            ans = f' over {dc} = ' + 'Success!'*(S>=dc) + 'Failed'*(S<dc)
        await ctx.channel.send(f"{ctx.message.author.global_name}'s saving throw: {R} {S}{ans}")

    except Exception as e:
        await ctx.reply(e, mention_author=False)



##### CANTRIP SPELLS #####
@commands.command(aliases=('eldritchblast',))
async def blast(ctx, *lv):
    """Casts eldritch blast. lv is the player level.
    This eldritch blast comes from dnd 5e as evocation cantrip"""
    level = DB.coercePlayerLevel(lv)
    await ctx.channel.send(DB._buildSpellSentence(author=ctx.message.author.global_name,
                                                  level=level,
                                                  spellName='eldritch blast',
                                                  rolled=[randint(1,10) for _ in range(DB._getCantripLevel(level))],
                                                  dmgType='force', emoji=':punch:'))

@commands.command()
async def chilltouch(ctx, *lv):
    """Casts chill touch. lv is the player level.
    This eldritch blast comes from dnd 5e as necromancy cantrip"""
    level = DB.coercePlayerLevel(lv)
    await ctx.channel.send(DB._buildSpellSentence(author=ctx.message.author.global_name,
                                                  level=level,
                                                  spellName='chill touch',
                                                  rolled=[randint(1,8) for _ in range(DB._getCantripLevel(level))],
                                                  dmgType='necrotic', emoji=':skull:'))

@commands.command()
async def firebolt(ctx, *lv):
    """Casts fire bolt. lv is the player level.
    This fire bolt comes from dnd 5e as evocation cantrip"""
    level = DB.coercePlayerLevel(lv)
    await ctx.channel.send(DB._buildSpellSentence(author=ctx.message.author.global_name,
                                                  level=level,
                                                  spellName='fire bolt',
                                                  rolled=[randint(1,10) for _ in range(DB._getCantripLevel(level))],
                                                  dmgType='fire', emoji=':fire:'))
    
    # aggiungere fiamma sacra

##### 1ST LEVEL SPELLS #####
@commands.command()
async def guidingbolt(ctx, *lv):
    """Casts fire bolt. lv is the used spell slot.
    This guiding bolt comes from dnd 5e as 1st-level evocation"""
    level = DB.coerceSlotLevel(lv, 1)
    await ctx.channel.send(DB._buildSpellSentence(author=ctx.message.author.global_name,
                                                  level=level,
                                                  spellName='guiding bolt',
                                                  rolled=[randint(1,6) for _ in range(3+level)],
                                                  dmgType='radiant', emoji=':sparkles:'))

@commands.command()
async def wounds(ctx, *lv):
    """Casts inflict wounds. lv is the used spell slot.
    This inflict wounds comes from dnd 5e as 1st-level necromancy"""
    level = DB.coerceSlotLevel(lv, 1)
    await ctx.channel.send(DB._buildSpellSentence(author=ctx.message.author.global_name,
                                                  level=level,
                                                  spellName='inflict wounds',
                                                  rolled=[randint(1,10) for _ in range(2+level)],
                                                  dmgType='necrotic', emoji=':skull:'))
    
@commands.command()
async def sleep(ctx, *lv):
    """Casts sleep. lv is the used spell slot.
    This sleep comes from dnd 5e as 1st-level enchantment"""
    level = DB.coerceSlotLevel(lv, 1)
    await ctx.channel.send(DB._buildSpellSentence(author=ctx.message.author.global_name,
                                                  level=level,
                                                  spellName='sleep',
                                                  rolled=[randint(1,8) for _ in range(3+2*level)],
                                                  dmgType='hit points'))

##### 2ND LEVEL SPELLS #####
@commands.command()
async def shadowblade(ctx, *lv):
    """Casts shadow blade. lv is the used spell slot.
    This inflict wounds comes from dnd 5e as 2nd-level illusion"""
    level = DB.coerceSlotLevel(lv, 2)
    await ctx.channel.send(DB._buildSpellSentence(author=ctx.message.author.global_name,
                                                  level=level,
                                                  spellName='shadow blade',
                                                  rolled=[randint(1,8) for _ in range(DB._getShadowBlade(level))],
                                                  dmgType='psychic', emoji=':crystal_ball:'))

##### 3RD LEVEL SPELLS #####
@commands.command()
async def fireball(ctx, *lv):
    """Casts fireball. lv is the used spell slot.
    This inflict wounds comes from dnd 5e as 3rd-level evocation"""
    level = DB.coerceSlotLevel(lv, 3)
    await ctx.channel.send(DB._buildSpellSentence(author=ctx.message.author.global_name,
                                                  level=level,
                                                  spellName='fireball',
                                                  rolled=[randint(1,6) for _ in range(5+level)],
                                                  dmgType='fire', emoji=':fire:'))


# This method must be here. It adds the commands to the bot
async def setup(bot):
    CMD_LIST = (adv, cento, coin, dis, elvenchad, explode, forall, jennystats, pg, race, reset, stats,
                superstats, tira, tpc, ts)
    SPELL_LIST = (blast, chilltouch, firebolt, fireball, guidingbolt, wounds, shadowblade, sleep)
    
    for i in CMD_LIST+SPELL_LIST:
        bot.add_command(i)
