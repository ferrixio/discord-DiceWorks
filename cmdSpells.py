from discord.ext import commands
from random import randint
import diceBlock as DB

### CANTRIP SPELLS ###
@commands.command()
async def blast(ctx, *lv):
    """Casts eldritch blast. lv is the player level.
    This eldritch blast comes from dnd 5e as evocation cantrip"""
    level = DB.coercePlayerLevel(lv)
    await ctx.channel.send(DB._buildSpellSentence(author=ctx.message.author.global_name,
                                                  level=level,
                                                  spellName='eldritch blast',
                                                  rolled=[randint(1,10) for _ in range(DB._getCantripLevel(level))],
                                                  dmgType='force'))

@commands.command()
async def chilltouch(ctx, *lv):
    """Casts chill touch. lv is the player level.
    This eldritch blast comes from dnd 5e as necromancy cantrip"""
    level = DB.coercePlayerLevel(lv)
    await ctx.channel.send(DB._buildSpellSentence(author=ctx.message.author.global_name,
                                                  level=level,
                                                  spellName='chill touch',
                                                  rolled=[randint(1,8) for _ in range(DB._getCantripLevel(level))],
                                                  dmgType='necrotic'))

@commands.command()
async def firebolt(ctx, *lv):
    """Casts fire bolt. lv is the player level.
    This fire bolt comes from dnd 5e as evocation cantrip"""
    level = DB.coercePlayerLevel(lv)
    await ctx.channel.send(DB._buildSpellSentence(author=ctx.message.author.global_name,
                                                  level=level,
                                                  spellName='fire bolt',
                                                  rolled=[randint(1,10) for _ in range(DB._getCantripLevel(level))],
                                                  dmgType='fire'))

### 1ST LEVEL SPELLS ###
@commands.command()
async def guidingbolt(ctx, *lv):
    """Casts fire bolt. lv is the used spell slot.
    This guiding bolt comes from dnd 5e as 1st-level evocation"""
    level = DB.coerceSlotLevel(lv, 1)
    await ctx.channel.send(DB._buildSpellSentence(author=ctx.message.author.global_name,
                                                  level=level,
                                                  spellName='guiding bolt',
                                                  rolled=[randint(1,6) for _ in range(3+level)],
                                                  dmgType='fire'))

@commands.command()
async def wounds(ctx, *lv):
    """Casts inflict wounds. lv is the used spell slot.
    This inflict wounds comes from dnd 5e as 1st-level necromancy"""
    level = DB.coerceSlotLevel(lv, 1)
    await ctx.channel.send(DB._buildSpellSentence(author=ctx.message.author.global_name,
                                                  level=level,
                                                  spellName='inflict wounds',
                                                  rolled=[randint(1,10) for _ in range(2+level)],
                                                  dmgType='necrotic'))
    
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

### 2ND LEVEL SPELLS ###
@commands.command()
async def shadowblade(ctx, *lv):
    """Casts shadow blade. lv is the used spell slot.
    This inflict wounds comes from dnd 5e as 2nd-level illusion"""
    level = DB.coerceSlotLevel(lv, 2)
    await ctx.channel.send(DB._buildSpellSentence(author=ctx.message.author.global_name,
                                                  level=level,
                                                  spellName='shadow blade',
                                                  rolled=[randint(1,8) for _ in range(DB._getShadowBlade(level))],
                                                  dmgType='psychic'))
    

# this method must be here. It adds the commands to the bot
async def setup(bot):
    SPELL_LIST = (blast, chilltouch, firebolt, guidingbolt, wounds, shadowblade, sleep)
    
    for i in SPELL_LIST:
        bot.add_command(i)