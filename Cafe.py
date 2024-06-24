# Maximum size of the problem
TAILLE = 4

# Classe définissant le problème café avec :
# L'agent et son objectif
# La voiture parcourant le tableau
class ProblemeCafe:
    # Fonction utilisée pour créer une liste d'état pour le problè
    def etats(self):
        # la liste des etats possibles
        etats = []
        etatsRobot = []
        etatsVoiture = []
        # Pour chaque position
        for pos in range(TAILLE):
            # On ajoute l'état du robot avec ses 2 états possibles dans le monde
            etatsRobot.append((pos, True))
            etatsRobot.append((pos, False))
            # Si pos == Taille-1
            if pos == TAILLE - 1:
                #Pour chaque positionv (position voiture)
                for posv in range(TAILLE):
                    # Si la pos est = 0
                    if posv == 0:
                        # La voiture change de sens (en haut de la route)
                        etatsVoiture.append((f"{posv}v", "bas"))
                        # La voiture change de sens (en bas de la route)
                    elif posv == TAILLE - 1:
                        etatsVoiture.append((f"{posv}v", "haut"))
                    else:
                        #On ajoute de façon classique la position de la voiture et sa direction possible
                        etatsVoiture.append((f"{posv}v", "haut"))
                        etatsVoiture.append((f"{posv}v", "bas"))
        # Pour chaque etat, on ajoute les etats voiture et etat robots
        etats.append(etatsRobot)
        etats.append(etatsVoiture)
        return etats
    # Fonction retournant les actions possibles pour un agent
    # Seul le robot en a (voir compte rendu)
    def actions(self):
        # retourne la liste des actions possible pour le robot
        actions = ["gauche", "droite", "poser", "prendre", "rien"]
        return actions
    # Fonction prenant un etat et une action et retournant l'état d'après
    # Return l'état du monde après
    def etatSuivant(self, etats, action):
        # raisonner par action
        (pos, cafe) = etats[0]
        (posv, direction) = etats[1]
        # Switch pour les déplacement de la voiture qui se déplace avant le robot (elle avant plus vite)
        match direction:
            case "haut":
                if posv == "1v":
                    posv = "0v"
                    direction = "bas"
                else:
                    posv = f"{int(posv[0]) - 1}v"
            case "bas":
                if posv == "2v":
                    posv = "3v"
                    direction = "haut"
                else:
                    posv = f"{int(posv[0]) + 1}v"
        if action == "gauche":
            pos = pos - 1
            if pos < 0:
                pos = 0
        if action == "droite":
            pos = pos + 1
            if pos > TAILLE - 1:
                pos = TAILLE - 1

        if action == "poser":
            cafe = False

        if action == "prendre":
            if pos == TAILLE - 1:
                cafe = True
        return [(pos, cafe), (posv, direction)]
    # Fonction calculant la récompense en fonction de l'état actuel et de l'état suivant
    # Return la récompense
    def recompense(self, etats, action, etatsF):
        # recompenses spéciales
        (pos, cafe) = etats[0]
        (posv, direction) = etats[1]
        (posf, cafef) = etatsF[0]
        (posvf, directionf) = etatsF[1]
        if (pos == 0) and cafe and (action == "poser"):
            return 10
        if (int(posvf[0]) == 2 and posf == 2) or (int(posvf[0]) == 2 and pos == 2):
            return -10
        if pos == 3 and action == "prendre" and not cafe:
            return 0
            # sinon retourne 0
        if action == "rien":
            return 0
        return -1
    # Fonction effectuant la mort de l'agent, car celui-ci meurt s'il se fait rentrer dedans
    def death(self, voiture):
        return ((0, False), voiture)
    # Fonction initialisant le départ de l'agent
    def depart(self):
        return ((0, False), ("1v", "bas"))
