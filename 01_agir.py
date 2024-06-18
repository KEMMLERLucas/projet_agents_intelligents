import random

import Cafe

# test importation
pb = Cafe.ProblemeCafe()
print(pb.etats())
print(pb.actions())
robot,voiture = pb.depart()
etatSuivant = pb.etatSuivant([robot,voiture],"droite")
print(etatSuivant)
etatSuivant = pb.etatSuivant(etatSuivant,"droite")
print(etatSuivant)
etatSuivant = pb.etatSuivant(etatSuivant,"droite")
print(etatSuivant)
etatSuivant = pb.etatSuivant(etatSuivant,"prendre")
print(etatSuivant)
etatSuivant = pb.etatSuivant(etatSuivant,"gauche")
print(etatSuivant)
etatSuivant = pb.etatSuivant(etatSuivant,"gauche")
print(etatSuivant)
etatSuivant = pb.etatSuivant(etatSuivant,"gauche")
print(etatSuivant)
etatSuivant = pb.etatSuivant(etatSuivant,"poser")
print(etatSuivant)
etatSuivant = pb.etatSuivant(etatSuivant,"rien")
print(etatSuivant)
etatSuivant = pb.etatSuivant(etatSuivant,"rien")
print(etatSuivant)
etatSuivant = pb.etatSuivant(etatSuivant,"rien")
print(etatSuivant)
etatSuivant = pb.etatSuivant(etatSuivant,"rien")
print(etatSuivant)
# On appel l'état de départ de café
def agirFixe():
    print(pb.depart())
    state = pb.depart()
    # On execute l'action gauche une première fois
    print("Etat actuel: " + str(state))
    state = pb.etatSuivant(state, "gauche")
    print("Etat suivant: " + str(state))
    # On execute l'action gauche une première fois
    print("Etat actuel: " + str(state))
    state = pb.etatSuivant(state, "gauche")
    print("Etat suivant: " + str(state))


# On récupère les différentes actions disponibles
availableActions = pb.actions()


# Fonction permettant d'agir un nombre de fois
def agirNb(nbIterations):
    #On initialise l'état de départ
    stateD = pb.depart()
    #On intialise les récompenses
    recompense = 0
    # Pour nbIteration
    for i in range(nbIterations):
        # On choisis une action au hasar
        rng = random.choice(availableActions)
        # On execute, et on obtiens l'état d'arrivé
        stateA = pb.etatSuivant(stateD, rng)
        #On obtiens la récompense
        recompense += pb.recompense(stateD, rng, stateA)
        print("Etat actuel: " + str(stateD))
        print("Etat suivant: " + str(stateA))
        print("Recompense: " + str(recompense))
        # On donne la valeur d'arrivée à la valeur de départ
        stateD = stateA

# agirNb(500)

# Voir pour faire un agir au hasard infini