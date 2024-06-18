
TAILLE = 4

class Voiture :


    def etats(self):
        # la liste des etats possibles
        etats = []
        for pos in range(TAILLE) :
            etats.append((pos,"haut"))
            etats.append((pos,"bas"))
        return etats

    def actions(self):
        # retourne la liste des actions
        actions = ["haut","bas"]
        return actions

    def etatSuivant(self, etat, action):
        # raisonner par action
        (pos,direction) = etat

        if action == "haut" :
            pos = pos + 1
            if pos < 0 and direction =="haut" :
                pos = 0

        if action == "bas" :
            pos = pos - 1
            if pos > TAILLE - 1 and direction =="bas":
                pos = TAILLE - 1
        return (pos,direction)




    def depart(self):
        return (3,False)

