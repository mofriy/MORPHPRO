aminos = {"ala" : "a",
        "arg" : "r",
        "asn" : "n",
        "asp" : "d",
        "cys" : "c",
        "glu" : "e",
        "gln" : "q",
        "gly" : "g",
        "his" : "h",
        "ile" : "i",
        "leu" : "l",
        "lys" : "k",
        "met" : "m",
        "phe" : "f",
        "pro" : "p",
        "ser" : "s",
        "thr" : "t",
        "trp" : "w",
        "tyr" : "y",
        "val" : "v"
        }

aminosrev = {j:i for i,j in aminos.items()}

def c3to1(amino3):
    return aminos[amino3]

def c1to3(amino1):
    return aminosrev[amino1]
