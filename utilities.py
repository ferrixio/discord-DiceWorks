#©Samuele Ferri 2023      Bot version: 3.2

from os import getenv
from random import choice
from dotenv import load_dotenv 
from discord import Embed
    
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
set_mess=(
    "Benvenuto su Otaku's House, {} :wave:",
    "È un piacere averti qui, {}",
    "Oh, vedo che abbiamo un nuovo amico. Benvenuto, {} :fox:"
    "Benvenuto all'inferno, {}",
    "{} benvenuto, sei forse tu il prossimo Re dei Pirati?",
    "{} È SALITO SUL QUEL CAZZO DI EVA! (finalmente)",
    "{}-kun, benvenuto :grin:",
    "La stavamo aspettando, {}-sensei",
    "Salutate il nuovo Hokage: {}",
    "{} è il DIO di un nuovo mondo?!",
    "Tuu tuu!! L'isekai bus sta arrivando, {} :bus:",
    "All hail {}!!!",
    "Ciao {}!",
    "{}, TATAKAE!",
    "{}, YASHASUIIN!!!",
    "Sono finalmente riuscita a legare l'anima di {} ad un'armatura d'acciaio",
    "Pesca la tua carta, {}",
    "Ohyo gozaimasu {} :smiling_face_with_3_hearts: ",
    "Ara ara, {}-kun :relieved: ",
    "Tutturuu! Ciao {} :wave:",
    "{} ci salverà dagli uomini del Pilastro :astonished:",
    "{} ci salverà dalle donne di Porta Pilastro :astonished: - cit. Nocoldiz feat. M¥ss Keta",
    "Abbiamo incontrato {} selvatico",
    "{} sei pronto a scendere nell'Abisso assieme a Hroki?",
    "{} è stato evocato per sbaglio",
    "Diamo il benvenuto al nuovo apprendista di Hroki: {}!",
    "{} kupò!",
    "{} è stato marchiato dalla mano di Dio",
    "Ho mandato {} per salvare questo server dalla distruzione",
    "{} è qui per partecipare al Toreno degli Sciamani",
    "{} è qui per assassinare Koro-sensei",
    "{}: STEEEEAL! \n Dama: Mi ha rubato le mutandine!:flushed:",
    "Gambare gambare {}",
    "Ecco lo sterminatore di goblin: {}",
    "È arrivato l'oppai dragon: {}",
    "Anche {} ha sconfitto Freezer :snowflake: ",
    "{} ha il potere del grembiule nudo",
    "{}, spero che questo server possa essere la casa che stai cercando",
    "Congratulazioni {}, hai sparato per primo",
    "{} vuoi assaggiare la mia coda?",
    "{} come osi sfacciare la cresta del vicedirettore Ni!?",
    "{} benvenuto nell'harem di Hroki",
    "Diamo il benvenuto alla nuova magical-girl {}",
    "{} è la nuova guerriera-sailor",
    "Benvenuto {}. Ti ricordi di Rem?",
    "Perché hai sfondato il cielo con un robottone scassato, {}?",
    "{}, benvenuto nel Server Errante di Hroki :european_castle: ",
    "Ecco il nuovo amico di Hroki: {} Tempest!",
    "{} prenditi i fazzoletti e goditi il server",
    "{} è il nuovo esponente dell'imanità",
    "È per i professionisti come {}",
    "{} è qui per imparare, imparare, imparare, imparare, imparare, imparare...",
    "Padroncino {}!",
    "Ecco il nuovo primatista del Ranking dei Re: {}!",
    "Le leggende narrano che {} abbia ucciso il Re Demone 300 anni orsono"
)

ACQUA=0x1ABC9C      #Color verde-acqua

dic_global_help={
        "standard":
            "**tira**: rolls dice with modifiers\n" +\
            "**tpc**: rolls a single d20; can add modifiers\n" +\
            "**cento**: rolls a single d100; can't add modifiers\n" +\
            "**coin**: tosses a coin\n" +"¬"*50,

        "advanced":
            "**adv**: advantage roll (with modifiers)\n" +\
            "**dis**: disadvantage roll (with modifiers)\n" +\
            "**elvenchad**: elven accuracy feature\n" +\
            "**explode**: explosive dice rolls (with modifiers)\n" +\
            "**forall**: rolls dice and add modifiers to each result\n" +\
            "**stats**: stats generator for d&d 5e\n" +"¬"*50,
        
        "miscellaneous":
            "**loli**: I leave this to your imagination; just try it!\n" +\
            "**member**: sends the number of member of this server as DM\n" +\
            "**ping**: shows bot current latency\n"+\
            "**reset**: reset the rng seed\n"+"¬"*50,

        "copyright":"©Samuele Ferri 2023\t\t\t\t Bot version: 3.2"}

dic_local_help={
        "adv":"Rolls dice and chooses the highest. The syntax is **!adv nds+c**, where " +\
                "n=number of dice, s=amplitude of dice, c=list of modifiers. " +\
                "Can make multiple rolls separating dice with a blank space.",

        "cento":"Rolls a single d100; no input required.",

        "coin":"Tosses a coin; no input required. It has a 1/256 chance to give a tie.",

        "dis":"Rolls dice and chooses the lowest. The syntax is **!dis nds+c**, where " +\
                "n=number of dice, s=amplitude of dice, c=list of modifiers. " +\
                "Can make multiple rolls separating dice with a blank space.",

        "elvenchad":"Rolls 2d20 (with also modifiers), rerolls the least and chooses the highest. " +\
                "The syntax is **!elvenchad k**, where k=list of modifiers.",

        "forall":"Rolls some dice and add modifiers to each result. The syntax is the same as !tira.",

        "help":"You are very mad if you've asked me this... why?",

        "loli":"Sends a random cute loli picture as direct message",

        "lc":"Rolls input dice and explode the result; it can sum modifiers. The syntax is\n**!lc dk+mods**, " +\
            "where k=dice and mods is a list of modifiers.",

        "member":"Sends as DM the number of member of this server; it doesn't count bots. Works only for admins.",

        "ping":"Shows the current bot latency.",

        "reset":"Reset the rng seed.",

        "stats":"Rolls 4 dice and sums the three highest. The syntax is **!stats x**, where x=many stats to generate (max 6).",

        "tira":"Rolls multiple dice (with also modifiers). The syntax is **!tira nds+c**, where n=number of dice, "+\
                "s=type of dice (among 2 and 256) and c=modifiers.\n If the user puts a +/- beetween dice "+\
                "it will sum the results, if it's a blank space it will return separated results. "+\
                "Isolated numbers will be ignored.",

        "tpc":"Rolls 1d20 and sums modifiers. The syntax is **!tpc x**, where x=modifiers (you must specify the sign)."}

help_desc = "Type !help [command] for more info on a specific command; \
works also with a list of commands separated by a blank space."

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
            em.add_field(name='Standard tools', value=dic_global_help["standard"], inline=False)
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

        em.set_footer(text=dic_global_help["copyright"])
        if em.fields:
            return em
    
    
    ### SPECIAL MESSAGE FUNCTIONS ###

    def loli() -> str:
        """Function that returns a random answer for !loli"""
        return choice(("https://cdn.discordapp.com/attachments/862702344395423810/864624192942899240/mayo-fbi.png",
               "https://cdn.discordapp.com/attachments/862702344395423810/912078312472473661/cystal_lizard1.png",
               "https://cdn.discordapp.com/attachments/862702344395423810/912078308391387156/angry_big_lizard.png"))

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
