class Appartement:

    def __init__(self, descripteurs, label):
        self.arrondissement = descripteurs[0]
        self.nb_pieces = descripteurs[1]
        self.meuble = descripteurs[2]
        self.balcon = descripteurs[3]
        self.etage = descripteurs[4]
        self.parking = descripteurs[5]
        self.surface = descripteurs[6]
        self.cuisine_equipe = descripteurs[7]
        self.cave = descripteurs[8]
        self.standing = descripteurs[9]
        self.ascenseur = descripteurs[10]

        self.prix = label

    def getDescripteurs(self):
        return [self.arrondissement, self.nb_pieces, self.meuble,
                self.balcon, self.etage, self.parking,
                self.surface, self.cuisine_equipe, self.cave,
                self.standing, self.ascenseur]

    #   def categorize(self):

    #   def normalize(self): -> choisit une norme, un quantité atomique, et un poids
    #   def rememoration(self) -> renvoit une liste de cas similaires au problème cible.
