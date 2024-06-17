
TAILLE = 4

class Voiture :


    def etats(self):
        # la liste des etats possibles
        etats = []
        for pos in range(TAILLE) :
            etats.append((pos,True))
            etats.append((pos,False))
        return etats

    def actions(self):
        # retourne la liste des actions
        actions = ["haut" ,"bas"]
        return actions

    def etatSuivant(self, etat, action):
        # raisonner par action
        (pos,cafe) = etat

        if action == "gauche" :
            pos = pos - 1
            if pos < 0 :
                pos = 0

        if action == "droite" :
            pos = pos + 1
            if pos > TAILLE - 1 :
                pos = TAILLE - 1

        if action == "poser" :
            cafe = False

        if action == "prendre":
            if pos == 0:
                cafe = True

        return (pos,cafe)


    def recompense(self, etat, action, etatF):
        # recompenses spéciales
        (pos,cafe) = etat
        # si au debut pose et a le cafe
        if (pos == TAILLE-1) and (cafe == True) and (action == "poser") :
            return 10

        # sinon retourne -1
        if (action == "rien") :
            return 0

        return -1



    def depart(self):
        return (3,False)

