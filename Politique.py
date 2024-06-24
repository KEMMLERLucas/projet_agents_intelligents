# Import des classes random pour le RNG, et café
import random
import Cafe
# Taille maximale de la grille, non utilisée
TAILLE = 4
# test importation
pb = Cafe.ProblemeCafe()

# Fonction permettant de créer une politique aléatoire
# Return la politique aléatoire créée
def creerPolitique():
    states = pb.etats()[0]
    actions = pb.actions()
    #Créer un dictionnaire contenant la politique avec le choix de l'action
    politique = {}
    for state in states:
        rng = random.choice(actions)
        politique[state] = rng
    return politique

#Création de la politique
politique = creerPolitique()

# Fonction utilisée pour executer la politique, uniquement pour la politique aléatoire, qui n'est pas faite de la même façon que la politique finale
# Return nothing, simplement des print de les actions
def executerPolitique(nbIterations, politique):
    stateD = pb.depart()
    recompense = 0
    pol = politique
    for i in range(nbIterations):
        action = pol.get(stateD[0])
        stateA = pb.etatSuivant(stateD, action)
        recompense += pb.recompense(stateD, action, stateA)
        if pb.recompense(stateD, action, stateA) == -10:
            stateA = pb.death(stateA[1])
        print("Action: " + str(action))
        print("Etat actuel: " + str(stateD))
        print("Etat suivant: " + str(stateA))
        print("Recompense: " + str(recompense))
        stateD = stateA

#Méthode à utiliser pour tester la politique créée
# executerPolitique(10, politique)

# Fonction utilisée pour retourner les etats possibles du monde
# Return les etats possibles du monde dans un dictionnaire
def return_etats_monde():
    etat_monde = {}
    for etat in pb.etats()[0]:
        for etat_voiture in pb.etats()[1]:
            etat_monde[(etat, etat_voiture)] = 0  # Initialiser chaque combinaison à 0
    return etat_monde

# Fonction utilisée pour calculer les Q value
# Return un tableau avec le GAIN MAXIMAL possible pour chaque etat du monde, à un nombre d'itération max
def sansPasDeTempsQValues(n):
    # Initialiser les valeurs d'état avec le dictionnaire fourni
    etat_value_0 = return_etats_monde()
    # Pour chaque itération
    for i in range(n):
        # On copie la première valeur de etat value
        etat_plus_un = etat_value_0.copy()
        #Pour chaque etat de l'agent
        for etat in pb.etats()[0]:
            # Pour chaque etat de l'agent
            for etat_voiture in pb.etats()[1]:
                # Etat du monde
                s = (etat, etat_voiture)
                # Gain maximal à l'état actuel
                # On met l'état actuel à -inf au cas ou les valeurs peut-être très négatives
                gain_max_etat_actuel = float('-inf')
                # Pour chaque actions
                for a in pb.actions():
                    # On calcule l'état suivant
                    state_plus_un = pb.etatSuivant([etat, etat_voiture], a)
                    # On calcule la récompense immédiate
                    recompense_immmediate = pb.recompense([etat, etat_voiture], a, state_plus_un)
                    # On prend la récompense immédiate + la récompense à l'état plus un
                    valeur = recompense_immmediate + etat_plus_un.get((state_plus_un[0], state_plus_un[1]), 0)
                    # Si la valeur est supérieur au gain max etat actuel
                    if valeur > gain_max_etat_actuel:
                        gain_max_etat_actuel = valeur
                # On remplace l'état plus un par le gain max etat actuel
                etat_plus_un[s] = gain_max_etat_actuel
        # L'état value 0 est ) etat plus un
        etat_value_0 = etat_plus_un
    return etat_value_0

# Fonction utilisée pour calculer la politique optimale en fonction des Qvaleurs
# Return un tableau avec la politique optimale
def sansPasDeTempsQValuesPolitique(n):
    # Initialiser les valeurs d'état avec le dictionnaire fourni
    etat_value_0 = return_etats_monde()
    #On initialise la politique
    politique = {}
    # Pour chaque itération
    for i in range(n):
        # On copie la première valeur de etat value
        etat_plus_un = etat_value_0.copy()
        # Pour chaque etat de l'agent
        for etat in pb.etats()[0]:
            # Pour chaque etat de la voiture
            for etat_voiture in pb.etats()[1]:
                # Etat du monde
                s = (etat, etat_voiture)
                # Gain maximal à l'état actuel
                # On met l'état actuel à -inf au cas ou les valeurs peut-être très négatives
                gain_max_etat_actuel = float('-inf')
                # On initialise la meilleure action
                meilleure_action = None
                # Pour chaque actions
                for a in pb.actions():
                    # On calcule l'état suivant
                    state_plus_un = pb.etatSuivant([etat, etat_voiture], a)
                    # On calcule la récompense immédiate
                    recompense_immmediate = pb.recompense([etat, etat_voiture], a, state_plus_un)
                    # On prend la récompense immédiate + la récompense à l'état plus un
                    valeur = recompense_immmediate + etat_plus_un.get((state_plus_un[0], state_plus_un[1]), 0)
                    # Si la valeur est supérieur au gain max etat actuel
                    if valeur > gain_max_etat_actuel:
                        gain_max_etat_actuel = valeur
                        #On applique la meilleure action à cet état la
                        meilleure_action = a
                        # On remplace l'état plus un par le gain max etat actuel
                etat_plus_un[s] = gain_max_etat_actuel
                # La politique de l'état S est égale à la meilleure action disponible pour cette action
                politique[s] = meilleure_action
        #On affecte etat value plus un à etat value 0
        etat_value_0 = etat_plus_un
    return politique

# Fonction nous permettant de lancer la meilleure politique
# Return la recompense à la fin
def executerPolitiqueOptimale(nbIterations, politique_optimale):
    stateD = pb.depart()
    recompense = 0
    for i in range(nbIterations):
        etat_courant = (stateD[0], stateD[1])
        action = politique_optimale.get(etat_courant)
        if action is None:
            break
        stateA = pb.etatSuivant(stateD, action)
        recompense_actuelle = pb.recompense(stateD, action, stateA)
        recompense += recompense_actuelle

        # Print l'état précédent, l'état actuel et la récompense
        print(f"Étape {i + 1}:")
        print(f"État précédent: {stateD}")
        print(f"Action: {action}")
        print(f"État actuel: {stateA}")
        print(f"Récompense: {recompense}")
        print("---------")

        if recompense_actuelle == -10:
            stateA = pb.death(stateA[1])
        stateD = stateA
    return recompense


politique_optimale = sansPasDeTempsQValuesPolitique(10)

# Exécuter la politique optimale et calculer le gain maximum
gain_max = executerPolitiqueOptimale(13, politique_optimale)

gain_max = sansPasDeTempsQValues(10)
print ("Gain max: ", gain_max)
