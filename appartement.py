
def convertStanding(valeur):
    if (valeur == 'Vivable'):
        return 0
    elif (valeur == 'Moyen'):
        return 1
    elif (valeur == 'Bon'):
        return 2
    elif (valeur == 'Tres bon'):
        return 3


class Appartement:

    def __init__(self, descripteurs):

        self.DESCRIPTEURS = {
            "arrondissement": descripteurs[0],
            "nb_pieces": descripteurs[1],
            "meuble": int(descripteurs[2]),
            "balcon": descripteurs[3],
            "etage": descripteurs[4] if descripteurs[9] else -descripteurs[4], #par convention, étage positif si ascenseur, négatif sinon
            "parking": descripteurs[5],
            "surface": descripteurs[6],
            "cuisine_equipe": int(descripteurs[7]),
            "standing": convertStanding(descripteurs[8]),
            "cave": int(descripteurs[10]),
            "prix": descripteurs[11],
        }


