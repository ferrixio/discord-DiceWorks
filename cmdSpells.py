from discord.ext import commands
from random import randint

@commands.command()
async def fireball(ctx, lv):
    """Cast fireball. lv is the requested level of the spell.
    This fireball comes from dnd 5e as 3rd level spell"""
    # converts the level and coerces it
    try:
        level = int(lv)
        if level >= 9:
            level = 9
        elif level < 3:
            level = 3
    except:
        level = 3
    
    rolled = [randint(1,6) for _ in range(5+level)]
    await ctx.channel.send(f"{ctx.message.author.global_name}'s level {level} fireball: `r`")
    
    await ctx.channel.send('kek')

# this method must be here. It adds the commands to the bot
async def setup(bot):
    SPELL_LIST = (fireball,)
    
    for i in SPELL_LIST:
        bot.add_command(i)