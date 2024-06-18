TAILLE = 4


class ProblemeCafe:

    def etats(self):
        # la liste des etats possibles
        etats = []
        etatsRobot = []
        etatsVoiture = []
        for pos in range(TAILLE):
            etatsRobot.append((pos, True))
            etatsRobot.append((pos, False))
            if pos == TAILLE - 1:
                for posv in range(TAILLE):
                    if posv == 0 :
                        etatsVoiture.append((f"{posv}v", "bas"))
                    elif posv == TAILLE-1 :
                        etatsVoiture.append((f"{posv}v", "haut"))
                    else :
                        etatsVoiture.append((f"{posv}v", "haut"))
                        etatsVoiture.append((f"{posv}v", "bas"))
        etats.append(etatsRobot)
        etats.append(etatsVoiture)
        return etats

    def actions(self):
        # retourne la liste des actions
        actions = ["gauche", "droite", "poser", "prendre", "rien"]
        return actions

    def etatSuivant(self, etats, action):
        # raisonner par action
        (pos, cafe) = etats[0]
        (posv, direction)=etats[1]
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
            if pos == TAILLE-1:
                cafe = True
        return [(pos, cafe),(posv, direction)]

    def recompense(self, etat, action, etatF):
        # recompenses spéciales
        (pos, cafe) = etat
        # si au debut pose et a le cafe
        if (pos == TAILLE - 1) and (cafe == True) and (action == "poser"):
            return 10

        # sinon retourne -1
        if (action == "rien"):
            return 0

        return -1

    def depart(self):
        return ((0,False), ("1v","bas"))
