import random

import Cafe

TAILLE = 4
# test importation
pb = Cafe.ProblemeCafe()


# print(pb.etats())
# print(pb.actions())


# A ^ S politiques différentes

def creerPolitique():
    states = pb.etats()
    actions = pb.actions()
    # Créer un dictionnaire
    politique = {}

    for state in states:
        rng = random.choice(actions)
        politique[state] = rng

    return politique


politique = creerPolitique()


# print("Politique: " + str(politique))


def executerPolitique(nbIterations, politique):
    # On initialise l'état de départ
    stateD = pb.depart()
    # On intialise les récompenses
    recompense = 0
    # On récupère la politique
    pol = politique
    # Pour nbIteration
    for i in range(nbIterations):
        # On récupère l'action dans le dictionnaire
        action = pol.get(stateD)
        # On execute, et on obtiens l'état d'arrivé
        stateA = pb.etatSuivant(stateD, action)
        # On obtiens la récompense
        recompense += pb.recompense(stateD, action, stateA)
        print("Action: " + str(action))
        print("Etat actuel: " + str(stateD))
        print("Etat suivant: " + str(stateA))
        print("Recompense: " + str(recompense))
        # On donne la valeur d'arrivée à la valeur de départ
        stateD = stateA


# executerPolitique(10, politique)


def creerPolitique(taille, states):
    politique = {}
    for state in states:
        (pos, cafe) = state
        if pos == 0:
            if cafe == False:
                politique[state] = 'prendre'
            else:
                politique[state] = 'droite'
        elif pos == taille - 1:
            if cafe == True:
                politique[state] = 'poser'
            else:
                politique[state] = 'gauche'
        else:
            if cafe:
                politique[state] = 'droite'
            else:
                politique[state] = 'gauche'
    return politique


pol = creerPolitique(4, pb.etats())


# print("Politique: " + str(pol))

# executerPolitique(1000, pol )

# La Q valeur est le gain que l'on pourrait avoir dans le futur, en effectuant une action
# Pi1 (s) =argmax<Q(s,d)
def unPasDeTemps(s, a):
    reward = {}
    (pos, cafe) = s
    if a == "droite" or a == "gauche":
        reward[s] = 0
    elif a == "rien":
        reward[s] = 0
    elif a == "prendre" and pos == 0 and cafe == False:
        reward[s] = -1
    elif a == "prendre" and pos == 0 and cafe == True:
        reward[s] = 0
    elif a == "poser" and pos == TAILLE - 1 and cafe == True:
        reward[s] = 10
    else:
        reward[s] = -1
    return reward


# A 1 pas de temps, la meilleure action à faire est de ne rien faire
# Ce n'est donc pas suffisant pour choisir la meilleure action à entreprendre

def deuxPasDeTemps(s):
    gains = {}
    for action in pb.actions():
        state_plus_un = pb.etatSuivant(s, action)
        reward = pb.recompense(s, action, state_plus_un)
        gt = reward
        for action in pb.actions():
            state_plus_un = pb.etatSuivant(s, action)
            reward2 = pb.recompense(s, action, state_plus_un)
            gt += reward2

        gains[action] = gt
    return gains


def sansPasDeTemps(n):
    total_esp_gain = 0

    for i in range(n):
        for s in pb.etats():
            recomp = {}
            for a in pb.actions():
                # On prend l'état suivant
                state_plus_un = pb.etatSuivant(s, a)
                # On calcul la récompense immédiate
                recomp_immediate = pb.recompense(s, a, state_plus_un)
                # Calcul de l'espérance de gain pour les états suivants
                # Tableau composé des récomposens futures
                future_rewards = []
                # Action suivante
                for next_action in pb.actions():
                    # On calcul la récompense suivante
                    state_plus_deux = pb.etatSuivant(state_plus_un, next_action)
                    # On l'ajoute dans les récompenses futures
                    future_rewards.append(pb.recompense(state_plus_un, next_action, state_plus_deux))
                # Une fois toutes les récompenses future récupérées, on prend le maximum
                recomp[a] = recomp_immediate + max(future_rewards)
            # On prend le maximum des valeurs (nécessaire ???)
            esp_gain = max(recomp.values())
            # Espérance de gain totale
            total_esp_gain += esp_gain

    return total_esp_gain


m_gain = sansPasDeTemps(10)


def sansPasDeTemps2(n):
    etat_value_0 = {etat: 0 for etat in pb.etats()}
    for i in range(n):
        etat_plus_un = etat_value_0.copy()

        for s in pb.etats():

            gain_max_etat_actuel = float('-inf')

            for a in pb.actions():
                state_plus_un = pb.etatSuivant(s, a)

                recompense = pb.recompense(s, a, state_plus_un)

                valeur = recompense + etat_plus_un[state_plus_un]

                if valeur > gain_max_etat_actuel:

                    gain_max_etat_actuel = valeur
            etat_plus_un[s] = gain_max_etat_actuel
    return etat_value_0[pb.depart()]


m_gain = sansPasDeTemps2(10)

print(m_gain)


def sansPasDeTemps3(n):
    # On sauvegarde les valeurs quand on viens de commencer le parcours
    etat_value_0 = {etat: 0 for etat in pb.etats()}
    # Pour chaque itération
    for i in range(n):
        # On fait une copy d'etat 0 pour bien s'assurer de reprendre ce que l'on a calculé avant
        etat_plus_un = etat_value_0.copy()
        # Pour chaque état
        for s in pb.etats():
            #On intialise le gain maximum pour l'état actuel ) -inf, car on peut avoir des gains négatifs (-10 suffirait par exemple, mais il vaut mieux s'assurer)
            gain_max_etat_actuel = float('-inf')
            # Pour chaque actions
            for a in pb.actions():
                # On calcul l'état suivant
                state_plus_un = pb.etatSuivant(s, a)
                # On calcul la récompense immédiate
                recompense_immmediate = pb.recompense(s, a, state_plus_un)
                # La valeur actuelle est égale à la récompense immédiate + la récompense maximum pour l'etat Q'(s',a')
                valeur = recompense_immmediate + etat_plus_un[state_plus_un]
                # Si la valeur actuelle est plus élevée
                if valeur > gain_max_etat_actuel:
                    # On remplace le gain maximum
                    gain_max_etat_actuel = valeur
            #La valeur sauvegardée pour l'état actuelle est égale au gain max de cet etat actuel
            etat_value_0[s] = gain_max_etat_actuel
    # On retourne la valeur pour laquelle, dans le tableau à l'état 0, on peut avoir le gain maximum
    return etat_value_0[pb.depart()]


gain_max = sansPasDeTemps3(10)

print(gain_max)

