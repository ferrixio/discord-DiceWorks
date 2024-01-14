from random import randint
from math import floor

kill_terms = ("I can roll al least 64 dice simultaneously",
              "255 is the maximal amplitude of the die",
              "2 is the minimal amplitude of the die")


"""Class to manage dice rolls. It is not an object, but only a collection of functions called
by the bot's commands.

There are two separate set of functions:
- Type-processing functions -> used to parse input strings and edit the output
- Dice rolls functions -> used to roll dice (in many ways)
"""

### TYPE-PROCESSING FUNCTIONS ###

def string2dice(L:list):
    """The first 'main' function of the bot. It prepares a dice-rolls-string from input. Logic behind:
        - Removes only the first +/- and the last +/-, if there were any
        - For each element of the input: 
            - if begins with +/-, attaches it to previous item (if first, don't)
            - if ends with +/-, join it with the next item
            - else appends it (isolated item)
        - Returns a list of strings (in lowercase)

    Example:\n
    INPUT from !command: ('3d20+1', '+2', '+1d4', '1-', '6d8-1', '-1d10', '-3')\n
    OUTPUT: ['3d20+1+2+1d4', '1-6d8-1-1d10-3']
    """

    C=[L[0].lower()]
    for i in range(1,len(L)):
        if L[i][0] in ('+','-'):
            C[-1] += L[i].lower()
        elif L[i][-1] in ('+','-'):
            L[i + 1] = L[i] + L[i + 1]
        else:
            C.append(L[i].lower())

    C = (i for i in C if 'd' in i)  #removes unused constants
    if C == []:
        return "No dice?"
    
    return C

def buildDice(v:str):
    """The second 'main' funtion of the bot. It builds the dice to roll. Logic behind:
        - For each piece of the input string-list it splits the +
        - For each piece of the splitted list it splits the -
        - For each piece of the splitted-splitted list, it builds the dice
        - Append everything in a int-list

    Blanks born by separating +/- are ignored
    """

    results, _dice = [], []

    plus_item = v.split("+")
    for k in plus_item:
        minus_item = k.split("-")
        first = True #first element of minus_item
        
        for z in minus_item:
            if z == '':
                first = False
                continue
            
            if first:
                first = False
                R,dado = check_roll(z,True)
            else:
                R,dado = check_roll(z,False)

            if R in kill_terms: # quit if there is an invalid die
                return R
            # appending the results to a list
            results.append(R)
            _dice.append(dado)

    return results, _dice

def check_roll(x:str, B:bool):
    """Function that manages the construction of the die to be pulled. Switch B is used for sums"""

    if "d" in x:
        #instruction for dice
        x=x.split("d")
        x[0]=x[0] + "1"*(x[0]=="")

        quantity=int(x[0])
        if quantity>64:
            #max number of dice rollable at the same moment.
            #Notice that one can make multiple '64-rolls' and still get 1000 rolls in one command...
            return kill_terms[0]

        die_amplitude = int(x[1])
        if die_amplitude > 256: #max amplitude of dice
            return kill_terms[1]
        if die_amplitude < 2: #min amplitude of dice
            return kill_terms[2]
        
        ZZ = roll(quantity,die_amplitude,B)

    else:
        #instruction for modifiers
        die_amplitude = 0
        ZZ = 0*(x=="") + (int(x)*(B)+(-int(x))*(not B))*(x!="")

    return ZZ, die_amplitude

def erase_parethesis(listData:list, key:str):
    """Function to edit the list of rolled dice to show in discord chat.\n
    It changes a 'list of list' in a single list of data. It adds the mono-format."""

    text = " "
    for i in range(len(listData)):
        text += f"`{listData[i]}`" #char `` used to have mono-type format
        if key == 'forall' and i == len(listData)-1:
            pass
        else:
            text += ", "
    return text


### DICE ROLLS FUNCTIONS ###

def roll(how_many:int, amplitude:int, B:bool) -> list:
    """This is the function that pulls all the dice of the form 'AdB'.\n
    Switch B is used for sums""" 

    return [(-1)**(int(B)+1) * randint(1,amplitude) for _ in range(how_many)]

def standard_roll(L:list):
    """Function that elaborates standard dice rolls"""

    G = string2dice(L)
    if isinstance(G, str):
        return G, None

    finalResults, S = [], []

    for item in G:
        tempResults, _ = buildDice(item)
        if isinstance(tempResults, str):
            return tempResults, None

        '''!tira 5d6+1d4 2d10 --> item 0 --> XX=[[1, 5, 2, 2, 6], [3]]
                                    item 1 --> XX=[[1, 7]]'''
        #preparing the output item
        total = 0
        for i in list(tempResults):
            if isinstance(i, list):
                finalResults.append(i)
                total += sum(i)
                continue
            
            total += i

        S.append(total)

    #Editing parenthesis in output
    finalResults = erase_parethesis(finalResults,'')

    return finalResults,S  

def van_svg(L:list, term:str, name:str):
    """Function that manages advantage/disavantage rolls for D&D.\n
    It's a copy of standard_roll, but the final sum contains only the max/min"""

    G = string2dice(L)
    if isinstance(G, str):
        return G, None, None

    finalResults, singleSums, dice = [], [], []

    for item in G:
        tempResults, die = buildDice(item)
        if isinstance(tempResults, str):
            return tempResults, None, None

        #preparing the output item
        total = 0
        for i in tempResults:
            if isinstance(i, list):
                finalResults.append(i)
                if term == "adv":
                    total += max(i)
                elif term == "dis":
                    total += min(i)
                continue
            
            total += i

        singleSums.append(total)
        dice += die
    
    #Cool custom answers. It checks only the first set of results
    for i in range(len(finalResults)):
        if max(finalResults[i]) == dice[i] and min(finalResults[i]) == dice[i]:
            ans = f'{name} lei è proprio fortunato'
            break
        elif max(finalResults[i]) == dice[i]:
            ans = f'Well duck, {name}!'
            break
        elif max(finalResults[i]) == 1:
            ans = f'{name}, lei è sfortunato :(\t'
            break           
        elif len(set(finalResults[i])) == 1 and len(finalResults[i]) != 1:
            ans = f'Uh?\t {name}:'
            break
        else:
            ans = f'La {"s"*(term == "dis")}fortuna di {name} dice'
            break
            
    finalResults = erase_parethesis(finalResults,'')

    return finalResults, singleSums, ans

def coin() -> str:
    """Function that tosses a simple coin. It has a chance of 1/257 to return a tie"""

    coinValue = randint(1,257)
    if coinValue in range(1,129):
        return 'Testa'
    elif coinValue in range(129,257):
        return 'Croce'
    
    return 'in piedi'

def _getModifier(numberList: list[int]) -> str:
    """Function that writes the sign of a number string"""
    modifier = floor((sum(numberList)-10)/2)
    return '+'*(modifier > 0) + str(modifier)

def stats(amount:int):
    """Function that generates up to 6 stats for D&D 5e. It rolls 4d6 and sums the three highest.\n
    Automatically convert the requested quantity in
        - a 6 if amount is above 6 or below -6
        - the nearest integer to itself and makes it positive 
    """

    output, serie = [], []
    if amount > 6 or amount < -6:
        amount = 6
        output.append("Input changed to value 6")
    else:
        amount = abs(int(amount))
    
    for i in range(0,amount):
        stats = roll(4,6,True)
        remainingValues = stats.pop(stats.index(min(stats)))  #remove min value of stats
        output.append(f"Stat {i+1}:\t\t`{stats+[remainingValues]}`\t`{sum(stats)} -> {_getModifier(stats)}`")
        serie.append(sum(stats))

    # if someone wanted to know the variance from the standard series (only in !stats 6)
    if amount == 6:
        stdSeries = (15,14,13,12,10,8)
        return output,sum(serie)-sum(stdSeries)

    return output,None

def superstats() -> str:
    """Function that performs three times !stats, returning a fancy table to the user."""

    tableStr = ""
    for i in range(6):
        # roll dice and pop the least value
        R1, R2, R3 = roll(4,6,True), roll(4,6,True), roll(4,6,True)
        R1.pop(R1.index(min(R1)))
        R2.pop(R2.index(min(R2)))
        R3.pop(R3.index(min(R3)))

        tableStr += f"Stat {i+1}:\t\t`{sum(R1)} -> {_getModifier(R1)}`\t\t" + \
                    f"`{sum(R2)} -> {_getModifier(R2)}`\t\t`{sum(R3)} -> {_getModifier(R3)}`\n"

    return tableStr[:-1]

def forall(L:list):
    """Function that rolls n dice and add modifiers to ALL results without sum them together"""

    G = string2dice(L)
    if isinstance(G, str):
        return G, None
    
    #a questo punto hai una lista di stringhe compatte
    rolledResults, moddedResults = [], []

    for item in G:
        tempResults, _ = buildDice(item)
        if isinstance(tempResults, str):
            return tempResults, None

        #preparing the output item
        to_add = 0
        rolledResults.append(tempResults[0])

        for i in range(1,len(tempResults)):
            if isinstance(tempResults[i], list):
                rolledResults.append(tempResults[i])
                to_add += sum(tempResults[i])
                continue
            
            to_add += tempResults[i]

        moddedResults.append([k+to_add for k in tempResults[0]])

    rolledResults = erase_parethesis(rolledResults,'')
    return rolledResults,str(moddedResults)

def elvenacc(L:list):
    """Function that manages Elven Accuracy feat of D&D 5e. Rolls 2d20 and reroll the lowest. 
    Then chooses the highest."""

    G = string2dice(L)
    if isinstance(G, str):
        return G, None, None, None

    rolledDice = None

    for item in G:
        tempResults, _ = buildDice(item)
        if isinstance(tempResults, str):
            return tempResults, None, None, None

        to_add = 0
        for i in tempResults:
            if isinstance(i, list):
                rolledDice = i
                continue
            
            to_add += i
    
    P = randint(1,20)       #extra d20
    finalResults = rolledDice*(P < min(rolledDice)) + [max(rolledDice),P]*(P >= min(rolledDice))

    return rolledDice, P, finalResults, max(finalResults)+to_add

def explode(L:int, amp:int) -> list[int]:
    """Auxiliary function to roll explosive dice"""
    listExplosions = [L]
    while listExplosions[-1] == amp:
        listExplosions.append(randint(1,amp))

    return listExplosions

def explosive_dice(L:list):
    """Function that rolls explosive dice (used in Savage World system).
    It pulls a die and if the result is the maximal amplitude of it, it pulls another one, 
    recursively."""

    G = string2dice(L)
    if isinstance(G, str):
        return G, None

    finalResults, sums = [], []

    for item in G:
        tempResults, die = buildDice(item)
        if isinstance(tempResults, str):
            return tempResults, None

        localTotal = 0
        for i in tempResults:
            if isinstance(i, list) and len(i)==1:
                shian = explode(i[0],die[0])
                finalResults.append(shian)
                localTotal += sum(shian)
                continue
            
            localTotal += i
            
        sums.append(localTotal)

    finalResults=erase_parethesis(finalResults,'')

    return finalResults,sums

def reset_seed():
    """Function that reset the rng seed"""
    from random import seed
    seed()
    return

def evaluateSize(L:list, race:str):
    """Evaluate the sizes of the character from its table"""
    roll_h = [randint(1,L[2]) for _ in range(2)]
    if race in ('elf', 'wood_elf', 'drow'):
        roll_w = [randint(1,L[3])]
    elif race in ('halfling', 'gnome'):
        roll_w = [1]
    else:
        roll_w = [randint(1,L[3]) for _ in range(2)]
    
    # size generation according to dnd 5e
    h = L[0] + 2.5*sum(roll_h)
    w = L[1] + 0.5*sum(roll_h)*sum(roll_w)
    
    return h, w
