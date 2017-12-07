from random import random, randint

def makeIfOpen(*vars):
    statement = 'if ('
    for v in vars:
        statement += makeVar(v[0], v[1]) # that is name, type
    statement += '){'

def makeIfBody(*vars):
    ???

def makeCloseIf():
    return '}'

def makeElseOpen(*vars):
    if len(vars) > 0:
        return 'else ' + makeIfOpen(vars)
    else:
        return 'else {'

def makeElseBody(*vars):
    ??

def makeCloseElse():
    return '}'


def makeRandIntEq(name, mn=-2147483648 mx=21474836):
    a = randint(mn,mx)
    op = choice(['<', '<=', '>' ,'>=', '==', '!='])
    return name + op + str(a)


def makeRandBoolEq(name):
    op = choice(['', '!'])
    return op + name

def makeRandDoubleEq(name, mn=-2147483648 mx=21474836):
    a = uniform(mn,mx)
    op = choice(['<', '<=', '>' ,'>=', '==', '!='])
    return name + op + str(a)

def makeRandFloatEq(name, mn=-2147483648 mx=2147483647):
    a = uniform(mn,mx)
    op = choice(['<', '<=', '>' ,'>=', '==', '!='])
    return name + op + str(a)
