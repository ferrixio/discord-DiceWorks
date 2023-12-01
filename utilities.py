#©Samuele Ferri 2023      Bot version: 3.5.0

from os import getenv
from random import choice
from dotenv import load_dotenv 
from json import load
from discord import Embed

ACQUA=0x1ABC9C      #Color verde-acqua

load_dotenv()
BOT = getenv('BOT')
CHAT_T = getenv('chat_in_test')
CHAT_O = getenv('chat_in_OH')
OT_GUILD = getenv('OTAKUS_GIULD')
TEST = getenv('TEST_GIULD')
DANIEL = getenv('DANIEL')
FERRI = getenv('FERRI')
OMAR = getenv('OMAR')
LAPO = getenv('LAPO')
VISCO = getenv('VISCO')
CENTO = getenv('CENTO')

nomi=(FERRI,CENTO,OMAR,LAPO,VISCO,DANIEL)
with open("variables.json", "r") as f:
    var = load(f)
    set_mess = var["welcome_messages"]
    copyright = "©"+var["copyright"]
    help_desc = var["help_description"]
    help_short = var["help_short"]
    dic_local_help = var["dic_local_help"]


dic_global_help={
        "standard":
            "**tira**: rolls dice with modifiers\n" +\
            "**tpc**: rolls a single d20; can add modifiers\n" +\
            "**ts**: makes a saving throw (add '<x' for the dc)\n" +\
            "**cento**: rolls 1d100; can't add modifiers\n" +\
            "**coin**: tosses a coin\n" +"¬"*50,

        "advanced":
            "**adv**: advantage roll (with modifiers)\n" +\
            "**dis**: disadvantage roll (with modifiers)\n" +\
            "**elvenchad**: elven accuracy feature\n" +\
            "**explode**: explosive dice rolls (with modifiers)\n" +\
            "**forall**: rolls dice and add modifiers to each result\n" +\
            "**stats**: stats generator for d&d 5e\n" +\
            "**superstats**: select a statblock among 3\n" +"¬"*50,
        
        "miscellaneous":
            "**member**: sends the number of member of this server as DM\n" +\
            "**ping**: shows bot current latency\n"+\
            "**redo**: repeat any command by replying to it\n"+\
            "**reset**: reset the rng seed\n"+"¬"*50}


class ServerUtilities:
    """Class containing the utilities for discord servers. It is not an object, but only a 
    collection of functions called by the bot's commands.
    
    There are three sets of functions:
    - Custom help function -> used to create a custom help command
    - Special message functions -> used to send custom message
    - Welcome functions -> used to manage custom welcome message
    """

    ### CUSTOM HELP FUNCTION ###

    def custom_help(terms:tuple, name:str):
        """Custom help function build using embed from discord"""
        if terms == ():
            em = Embed(title=f"{name}'s command list", colour=ACQUA, description=help_desc)
            em.add_field(name="Standard tools", value=dic_global_help["standard"], inline=False)
            em.add_field(name="Advanced tools", value=dic_global_help["advanced"], inline=False)
            em.add_field(name="Miscellaneous", value=dic_global_help["miscellaneous"])
    
        elif "full" in terms:
            em = Embed(title=f"{name}'s full command list", colour=ACQUA, description="Sorted in alphabetic order")
            for i in dic_local_help:
                em.add_field(name=i, value=dic_local_help[i], inline=False)

        else:
            em = Embed(colour=ACQUA)
            for i in terms:
                if i in dic_local_help:
                    em.add_field(name=i, value=dic_local_help[i], inline=False)

        em.set_footer(text=copyright)
        if em.fields:
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
                (username+", sarò l'incarnazione della tua fortuna. !help per sapere quali sono i miei servizi.")*(str(user_id) not in nomi)


    ### WELCOME FUNCTIONS ###

    def welcome() -> str:
        """Random welcome message for OtakusHouse"""
        return choice(set_mess)
