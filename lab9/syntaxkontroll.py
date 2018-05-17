# Syntaxkontroll

from linkedQFile import LinkedQ

atoms = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr",
"Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd",
"In", "Sn", "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf",
"Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm",
"Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Fl", "Lv"]

class Syntaxfel(Exception):
    pass

# <mol> ::= <group> | <group><mol>
def readMolecule(q):
    if q.isEmpty():
        return
    else:
        #Fall 1 - Grupp
        readGroup(q)
        #Fall 2 - Grupp med ytterligare en molekyl efter
        readMolecule(q)

# <group> ::= <atom> | <atom><num> | (<mol>) <num>
def readGroup(q):
    firstValue = q.currentQ()

    #Fall 0 - Parantesgrupp börjar
    if (firstValue == "("):
        q.dequeue()
        return readMolecule(q)

    #Fall 3 - Molekyl med nummer efter
    if(firstValue == ")"):
        q.dequeue()
        if(q.currentQ().isdigit()):
            if(readNumber(q.currentQ())):
                q.dequeue()
                return readMolecule(q)
            else: 
                raise Syntaxfel("Felaktig siffra i slutet av...")

    # Fall 1 - Enkel atom
    readAtom(q)

    # Fall 2 - Atom med nummer efter
    if not q.isEmpty():
        qnu = q.currentQ()
        if(qnu.isdigit()):
            readNumber(qnu)
            q.dequeue()

    return

# <atom>  ::= <LETTER> | <LETTER><letter>
def readAtom(q): 
    characterList = []
    first = q.currentQ()
    second = q.peek()
    print(first)
    print(second)

    # Fall 1 - en STOR bokstav
    if (readCapitalLetters(first)):
        characterList.append(first)
        q.dequeue()
    else:
        raise Syntaxfel(first + "Är inte en stor bokstav")

    if not q.isEmpty():
        # Fall 2 - En STOR bokstav följs av en liten bokstav
        if(readLowerCaseLetters(second)):
            q.dequeue()   
            characterList.append(second)

        # Undantagsfall:
        elif(second.isdigit() or second == ")"):
            # Om peek är en siffra eller slutparantes vill vi
            # Hantera det i readGroup och inte här. Denna check borde
            # flyttas ut ur readAtom. 
            pass
        elif(readCapitalLetters(second)):
            # Om peek är en stor bokstav så har vi en sammansättning
            # t.ex. COOH, denna ska läsas atom för atom så vi skickar bara vidare q
            pass
        else:
            raise Syntaxfel(first + " Är inte en liten bokstav")

    atom = ''.join(characterList)
    if not (isAtom(atom)):
        raise Syntaxfel(atom + " Är inte en TRUE atom")
    return

#<LETTER>::= A | B | C | ... | Z
def readCapitalLetters(letter):
    if letter.isupper():
        return letter

#<letter>::= a | b | c | ... | z
def readLowerCaseLetters(letter): 
    if letter.islower():
        return letter

#<num>::= 2 | 3 | 4 | ...
def readNumber(number): 
    number = int(number)
    if number >=2:
        return number

def storeFormula(formel):
    q = LinkedQ()
    numlist = []
    formel = list(formel)
    for tecken in formel:
        if tecken.isdigit():
            numlist.append(tecken)
        else:
            if numlist:
                num_node = ''.join(numlist)
                q.enqueue(num_node)
                numlist = []
            q.enqueue(tecken)

    if numlist:
        num_node = ''.join(numlist)
        q.enqueue(num_node)

    return q

def isAtom(atom):
    if(atom in atoms):
        return True


# <formel> ::= <molekyl>
def kollaSyntax(formel):
    q = storeFormula(formel)
    try:
        readMolecule(q)
        return "Formeln är syntaktiskt korrekt"
    except Syntaxfel as fel:
        return str(fel)

def main():
    formel = input("Skriv en formel: ")
    resultat = kollaSyntax(formel)
    print(resultat)

if __name__ == "__main__":
    main()

