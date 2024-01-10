from discord.ext import commands
import diceBlock as DB

@commands.command()
async def test(ctx):
    await ctx.channel.send('kek')

# this method must be here. It adds the commands to the bot
async def setup(bot):
    SPELL_LIST = (test,)
    
    for i in SPELL_LIST:
        bot.add_command(i)