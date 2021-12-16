import pandas as pd
from anytree import Node, RenderTree
from anytree.exporter import DotExporter


# import graphviz
from appartement import Appartement

# Utilisateur, Debug
MODE = "Debug"

APPARTEMENT_CIBLE = {
            "arrondissement": 8,
            "nb_pieces": 2,
            "meuble": 0,
            "balcon": 1,
            "etage": 0,
            "parking": 1,
            "surface": 43,
            "cuisine_equipe": 1,
            "standing": "Bon",
            "ascenseur" : 1,
            "cave": 0,
}
POIDS = {
    "meuble" : 100,
    "balcon" : 50,
    "etage" : 10,
    "parking" : 50,
    "surface" : 20,
    "cuisine_equipe" : 20,
    "standing" : 100,
    "cave" : 20,
}

# Rempli la base de cas à partir de données contenu dans le .csv
def init_base_cas (root, df):

    # On crée les différentes feuilles de notre arbre à partir des différents cas
    for i in df.index:
        # Le premier noeud correpond à l'arrondissement de l'appartement
        if df['Arrondissement'][i] not in [child.name for child in root.children]:
            node_arrondissement = Node(df['Arrondissement'][i], parent=root)
        else:
            node_arrondissement = [child for child in root.children if child.name == df['Arrondissement'][i]][0]

        # Le second noeud correspond au nombre de pièces de l'appartement
        if df['Nombre_pieces'][i] not in [child.name for child in node_arrondissement.children]:
            node_piece = Node(df['Nombre_pieces'][i], parent=node_arrondissement)
        else:
            node_piece = [child for child in node_arrondissement.children if child.name == df['Nombre_pieces'][i]][0]

        # On crée un apaprtement
        descripteurs = []
        for column in df.columns:
            descripteurs.append(df[column][i])
        appart = Appartement(descripteurs)

        # On ajoute un noeud pour son appartement
        node_appartement = Node(appart, parent=node_piece)

    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name))


# Renvoi l'appartement source le plus similaire à l'appartement cible
def rememoration(cible, root):
    list_appart_similaires = []
    appart_similaire = 0
    arrondissement = cible.DESCRIPTEURS["arrondissement"]
    exists = False
    for child in root.children:
        if child.name == arrondissement:
            node_arrondissement = child
            exists = True
    if exists:
        exists = False
        nb_pieces = cible.DESCRIPTEURS["nb_pieces"]
        for child in node_arrondissement.children:
            if child.name == nb_pieces:
                node_piece = child
                exists = True
    if exists:
        for child in node_piece.children:
            list_appart_similaires.append(child.name)

    if len(list_appart_similaires) != 0:
        index_source = 0
        delta_source = 10000000
        for i in range(len(list_appart_similaires)):
            delta = computeDelta(list_appart_similaires[i], cible)
            if abs(delta) <= delta_source:
                index_source = i
                delta_source = delta
        appart_similaire = list_appart_similaires[index_source]

    return appart_similaire

def computeDelta(source, cible):
    src = source.DESCRIPTEURS
    target = cible.DESCRIPTEURS
    delta = 0
    for a in POIDS.keys():
        sum = (target[a] - src[a]) * POIDS[a]
        print(sum)
        delta += sum
    return delta

# Calcul le delta de prix entre l'appartement cible et l'appartement source
def adaptation(source, cible):
    src = source.DESCRIPTEURS
    target = cible.DESCRIPTEURS
    delta = 0
    for a in POIDS.keys():
        sum = (target[a] - src[a]) * POIDS[a]
        print(sum)
        delta += sum
    return source.DESCRIPTEURS["prix"] + delta


def main():

    # Chargement des données et remplissage de la base de cas
    df = pd.read_csv(filepath_or_buffer='Appartement.csv', sep=',')
    root = Node('{}')
    init_base_cas(root, df)

    # Création d'un appartement cible
    if MODE == "Utilisateur":
        print("Entrer les descripteurs de l'appartement pour obtenir une estimation de son prix")
        descripteurs = []
        descripteurs.append(input("Arrondissement : entier de 1 à 9"))
        descripteurs.append(input("Nombre_pieces : entier de 1 à 7"))
        descripteurs.append(input("Meuble : 1 ou 0"))
        descripteurs.append(input("Balcon : entier"))
        descripteurs.append(input("Etage : entier"))
        descripteurs.append(input("Parking : 1 ou 0"))
        descripteurs.append(input("Surface : float"))
        descripteurs.append(input("Cuisine_equipee : 1 ou 0"))
        descripteurs.append(input("Standing : Vivable, Moyen, Bon, Tres bon"))
        descripteurs.append(input("Ascenseur : 1 ou 0"))
        descripteurs.append(input("Cave : 1 ou 0"))
        descripteurs.append(0)

    else:
        descripteurs = [APPARTEMENT_CIBLE["arrondissement"],APPARTEMENT_CIBLE["nb_pieces"],
                        APPARTEMENT_CIBLE["meuble"],APPARTEMENT_CIBLE["balcon"],
                        APPARTEMENT_CIBLE["etage"],APPARTEMENT_CIBLE["parking"],
                        APPARTEMENT_CIBLE["surface"],APPARTEMENT_CIBLE["cuisine_equipe"],
                        APPARTEMENT_CIBLE["standing"],APPARTEMENT_CIBLE["ascenseur"],
                        APPARTEMENT_CIBLE["cave"],0]

    cible = Appartement(descripteurs)

    # Rememoration et adaptation
    source = rememoration(cible, root)
    print(source)
    if source == 0:
        print("Aucun appartement comparable trouvé")
    else:
        print(f"Le prix de l'appartement est estimé à {adaptation(source, cible)}€")


if __name__ == '__main__':
    main()

