from os import getenv
from dotenv import load_dotenv
from discord import Embed, ui, ButtonStyle, Interaction
from discord.utils import get
from diceBlock import VARIABLES as var

ACQUA=0x1ABC9C      #Color verde-acqua

load_dotenv()
BOT = getenv('BOT')
CHAT_T = getenv('chat_in_test')
TEST = getenv('TEST_GIULD')
DANIEL = getenv('DANIEL')
FERRI = getenv('FERRI')
OMAR = getenv('OMAR')
LAPO = getenv('LAPO')
VISCO = getenv('VISCO')
CENTO = getenv('CENTO')

nomi=(FERRI,CENTO,OMAR,LAPO,VISCO,DANIEL)
copyright = "©"+var["copyright"]
help_desc = var["help_description"]
help_short = var["help_short"]
help_spell = var["help_spell"]
dic_global_help = var["dic_global_help"]
dic_local_help = var["dic_local_help"]
dic_spell_list = var["spell_list"]
aliases = var["aliases"]


class ServerUtilities:
    """Class containing the utilities for discord servers. It is not an object, but only a 
    collection of functions called by the bot's commands.
    
    There are three sets of functions:
    - Custom help function -> used to create a custom help command
    - Special message functions -> used to send custom message
    - Voice functions -> used to manage voice chatting
    """

    ### CUSTOM EMBEDDED MESSAGES ###
    def custom_help(terms:tuple, name:str) -> tuple[Embed, bool]:
        """Custom help function build using embed from discord"""
        fullPresence = False
        if terms == ():
            # do nothing and activate the new help message in the main
            return None, None
    
        elif "full" in terms or "all" in terms:
            fullPresence = True
            em = Embed(title=f":notebook_with_decorative_cover: {name}'s full command list", colour=ACQUA, description="Sorted in alphabetic order")
            for i in dic_local_help:
                try:
                    als = f" (aliases: {', '.join(aliases[i])})"
                except:
                    als = ''
                em.add_field(name=i+als, value=dic_local_help[i], inline=False)

        else:
            em = Embed(colour=ACQUA)
            for i in terms:
                if i in dic_local_help:
                    try:
                        als = f" (aliases: {', '.join(aliases[i])})"
                    except:
                        als = ''
                    em.add_field(name=i+als, value=dic_local_help[i], inline=False)

        em.set_footer(text=copyright)
        if not em.fields:
            raise TypeError('Command not found')
        
        return em, fullPresence
    
    def spellList():
        """Returns the embedded message of the spell list"""
        em = Embed(title=f":scroll: Spell list", colour=ACQUA)
        for key, value in dic_spell_list.items():
            if value:
                em.add_field(name=key, value='\n'.join(value), inline=True)

        em.add_field(name="Rules", value=help_spell, inline=False)
        em.set_footer(text=copyright)
        return em    
    
    ### SPECIAL MESSAGE FUNCTIONS ###
    def _getChangelog(name:str, text:str = '') -> Embed:
        """Function that returns an embed version of the changelog"""
        em = Embed(title=f"What's new in {name}?", colour=ACQUA, description=help_short)
        em.add_field(name="", value=text, inline=False)
        em.add_field(name="", value="Complete changelog at https://github.com/ferrixio/discord-DiceWorks/blob/main/CHANGELOG.txt", inline=False)
        em.set_footer(text=copyright)
        return em
    
    def _text2Embed(name:str, text:str) -> Embed:
        """Function that converts text to Embed message"""
        em = Embed(title=f"Message from {name}", colour=ACQUA)
        em.add_field(name="", value=text)
        return em

    def master(username:str,user_id:int) -> str:
        """Helping function to message "master" (it's a pseudo-ping-pong command)"""

        return 'Mio supremo creatore, sono al tuo servizio'*(str(user_id)==FERRI)+\
            'Padroncino Omar, che cosa posso fare per te?'*(str(user_id)==OMAR)+\
            'Lapo-sama, farò tutto ciò che desidera'*(str(user_id)==LAPO)+\
            'Rusnejat caro, sono uscita dal Cubespace solo per te :heart:. In che modo posso esserti utile?'*(str(user_id)==CENTO)+\
            'Visco-sensei, mi ha chiamato?'*(str(user_id)==VISCO)+\
            'Daniel nya! Swono al tuwo sewizio UwU'*(str(user_id)==DANIEL)+\
            (username+", sarò l'incarnazione della tua fortuna. !help per sapere cosa sono in grado di fare.")*(str(user_id) not in nomi)
    
    ### VOICE FUNCTIONS ###
    def is_connected(ctx) -> bool:
        """Returns true if the bot is currently connected to a voice chat"""
        voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
        return voice_client and voice_client.is_connected()


### Embeded menu with buttons ###
class PaginationView(ui.View):

    def __init__(self, *, timeout: float | None = 180, botName:str):
        self.botName = botName
        super().__init__(timeout=timeout)

    async def send(self, ctx):
        self.message = await ctx.channel.send(view=self)
        await self.update_message(1)
        
    @staticmethod
    def _addField(em:Embed, dictKey:str) -> Embed:
        """Add field of the selected dictionary key to the embed"""
        for k in dic_global_help[dictKey]:
            try:
                als = f" (aliases: {', '.join(aliases[k])})"
            except:
                als = ''
            em.add_field(name=k+als, value=dic_local_help[k], inline=False)

        return em

    def create_embed(self, page:int):
        """Creates the embedded message of the respective page.
        Page list:
        - 1 = standard rolls
        - 2 = advanced rolls
        - 3 = characters creation
        - 4 = spell list
        - 5 = miscellaneous"""
        em = Embed(colour=ACQUA, description=help_desc)
        match page:
            case 1: # standard rolls
                em.title = f":notebook_with_decorative_cover: {self.botName}'s standard commands"
                em = self._addField(em, "standard")
            
            case 2: # advanced rolls
                em.title = f":bookmark: {self.botName}'s advanced commands"
                em = self._addField(em, "advanced")
                
            case 3: # char creation
                em.title = f":star2: {self.botName}'s characters creation commands"
                em = self._addField(em, "characters")
            
            case 4: # spell list
                em.title = f":scroll: {self.botName}'s Spell list"
                for key, value in dic_spell_list.items():
                    if value:
                        em.add_field(name=key, value='\n'.join(value), inline=True)
                em.add_field(name="Rules", value=help_spell, inline=False)
            
            case 5: # miscellaneous
                em.title = f":placard: {self.botName}'s miscellaneous commands"
                em = self._addField(em, "miscellaneous")
            
            case _:
                pass

        em.set_footer(text=copyright)
        return em

    async def update_message(self, newPage:int):
        """Updates the embedded message with the new page"""
        await self.message.edit(embed=self.create_embed(newPage), view=self)

    def update_buttons(self):
        """Update the graphics of the buttons in the embed"""
        pass

    @ui.button(label='Standard',
               style=ButtonStyle.primary)
    async def std_button(self, interaction:Interaction, button: ui.Button):
        await interaction.response.defer()
        await self.update_message(1)

    @ui.button(label='Advanced',
               style=ButtonStyle.primary)
    async def adv_button(self, interaction:Interaction, button: ui.Button):
        await interaction.response.defer()
        await self.update_message(2)

    @ui.button(label='Characters',
               style=ButtonStyle.success)
    async def chr_button(self, interaction:Interaction, button: ui.Button):
        await interaction.response.defer()
        await self.update_message(3)

    @ui.button(label='Spell list',
               style=ButtonStyle.danger)
    async def spl_button(self, interaction:Interaction, button: ui.Button):
        await interaction.response.defer()
        await self.update_message(4)

    @ui.button(label='Miscellaneous',
               style=ButtonStyle.secondary)
    async def msc_button(self, interaction:Interaction, button: ui.Button):
        await interaction.response.defer()
        await self.update_message(5)

    
    