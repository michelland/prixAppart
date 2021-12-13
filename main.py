import pandas as pd
from anytree import Node, RenderTree
from anytree.exporter import DotExporter


# import graphviz
from appartement import Appartement

# Utilisateur, Debug
MODE = "Debug"

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


# Renvoi la liste des appartements similaire à l'appartement en paramètre
def rememoration(cible, root):
    arrondissement = cible.DESCRIPTEURS["arrondissement"]
    node_arrondissement = [child for child in root.children if child.name == arrondissement][0]
    nb_pieces = cible.DESCRIPTEURS["nb_pieces"]
    node_piece = [child for child in node_arrondissement.children if child.name == nb_pieces][0]
    list_appart_similaires = []
    for child in node_piece.children:
        list_appart_similaires.append(child.name)

    return list_appart_similaires


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
        descripteurs = [8,2,1,1,4,1,43,1,'Bon',1,0,0]

    cible = Appartement(descripteurs)

    # Rememoration et adaptation
    list = rememoration(cible, root)
    if len(list) == 0:
        print("Aucun appartement comparable trouvé")
    else:
        print(f"Le prix de l'appartement est estimé à {adaptation(list[0], cible)}€")



    
    
    

# TODO Ecrire fonction calculant delta entre deux appartements, en faisant la somme des deltas
if __name__ == '__main__':

    main()
    # root = Node('{}')
    # df = pd.read_csv(filepath_or_buffer='Appartement.csv', sep=',')
    # print(df)
    # init_base_cas(root, df)
    # descripteurs = []
    # descripteurs2 = []
    # for column in df.columns:
    #     descripteurs.append(df[column][0])
    # appart = Appartement(descripteurs)
    # for column in df.columns:
    #     descripteurs2.append(df[column][1])
    # appart2 = Appartement(descripteurs2)
    # print(adaptation(appart,appart2))
    # list = rememoration(appart,root)



    # print(len(list))
    # print(list[0].arrondissement)
    # print(list[0].nb_pieces)
    # print(f"appart : {appart.arrondissement}, {appart.nb_pieces}")
    # print(f"appart_similaire : {list[0].arrondissement}, {list[0].nb_pieces}, {list[0].etage}")
    # print(f"appart_similaire2 : {list[1].arrondissement}, {list[1].nb_pieces}, {list[1].etage}")


    """ # Le troisième noeud correspond à la surface (on fait par tranche de 10 m2)
     surface_intermedaire = (df['surface'][i] // 10)*10
     if surface_intermedaire not in [child.name for child in node_piece.children]:
         node_taille = Node(surface_intermedaire, parent=node_piece)
     else:
         node_taille = [child for child in node_piece.children if child.name == surface_intermedaire][0]

     #Le quatrième noeud correspond au standing de l'appartement
     if df['Standing'][i] not in [child.name for child in node_taille.children]:
         node_standing = Node(df['Standing'][i], parent=node_taille)
     else:
         node_standing = [child for child in node_taille.children if child.name == df['Standing'][i]][0]

     # Le cinquième noeud correspond au standing de l'appartement
     if df['Standing'][i] not in [child.name for child in node_taille.children]:
         node_standing = Node(df['Standing'][i], parent=node_taille)
     else:
         node_standing = [child for child in node_taille.children if child.name == df['Standing'][i]][0]

     # Le sixième noeud correspond au standing de l'appartement
     if df['meuble'][i] not in [child.name for child in node_standing.children]:
         node_standing = Node(df['meuble'][i], parent=node_taille)
     else:
         node_standing = [child for child in node_taille.children if child.name == df['meuble'][i]][0]"""

    # DotExporter(root).to_picture("udo.png")



    # print(root.children[0].children[0].name)
