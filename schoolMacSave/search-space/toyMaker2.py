from random import random, randint

def makeIfOpen(*vars):
    statement = 'if ('
    ands = randint(1,len(vars))
    andsList = '&&'.join(vars[:ands])
    orsList = '||'.join(andsList,vars[ands:])
    return orsList + '){\n'

def makeIfBody(**var):
    numIfs = var['ifs']
    numBodyVars = var['numBody']


def closeConditional():
    return '}'

def makeElseOpen(*vars):
    if len(vars) > 0:
        return 'else ' + makeIfOpen(vars)
    else:
        return 'else {\n'

def makeElseBody(*vars):
    ??





def makeRandIntEq(name, mn=-128 mx=127):
    a = randint(mn,mx)
    op = choice(['<', '<=', '>' ,'>=', '==', '!='])
    return name + op + str(a)


def makeRandBoolEq(name):
    op = choice(['', '!'])
    return op + name

def makeRandDoubleEq(name, mn=-128 mx=127):
    a = uniform(mn,mx)
    op = choice(['<', '<=', '>' ,'>=', '==', '!='])
    return name + op + str(a)

def makeRandFloatEq(name, mn=-128 mx=127):
    a = uniform(mn,mx)
    op = choice(['<', '<=', '>' ,'>=', '==', '!='])
    return name + op + str(a)


#combinations (+ - * / %)


# generate number of vars to include in this if statement
# generate number of vars to include in the body

# for if pass number of vars
    # generate names/types
    # generate combination groups (a + b < c vs a < 4 && b > 6 && c == 2)

numVars = randint(1,6)
numBody = randint(1,numVars)  # not necessarily only using variables from if def
numLayers # iteration variable

potentialVars =['a','b','c','x','y','z','d','f','g','tmp','h','i','j','k','l','m','n','o']
myVars = choice(potentialVars, numVars)
myBodyVars = choice(potentialVars, numBody)

potentialTypes = ['float', 'boolean', 'double', 'int']
myTypes = choice(potentialTypes,numVars)
myBodyTypes = choice(potentialTypes, numBody)

combinations = []
sumC = 0
while (sumC <= myVars):
    tmp = randint(1,myVars-sumC)
    combinations.append(tmp)
    sumC+=tmp

sumC = 0
clauses = []
for c in combinations:
    tmp = myVars[sumC:sumC+c]
    typesTmp = myTypes[sumC:sumC+c]
    sumC += c
    clauses.append(makeClause(tmp, typesTmp))

# how to decide when to nest IFs, when ELSEs,when to put a regular body and when to put another layer?
makeIfOpen(clauses)

makeIfBody(ifs=??, vars=??)  # need to decide if this is having an "if"
closeConditional()
makeElseOpen()
makeElseBody()
closeConditional()







# turn number into binary

# use 1/0 to decide whether to make the next thing an if/else, use length to decide how many to do

# !!! this only does all 1-element things.  For n-element things need...
