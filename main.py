import pandas as pd
from anytree import Node, RenderTree
from anytree.exporter import DotExporter


# import graphviz
from appartement import Appartement

POIDS = {
    "meuble" : 100,
    "balcon" : 50,
    "étage" : 10,
    "parking" : 50,
    "surface" : 100,
    "cuisine_equipe" : 20,
    "standing" : 100,
    "ascenseur" : 50,
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
    arrondissement = cible.arrondissement
    node_arrondissement = [child for child in root.children if child.name == arrondissement][0]
    nb_pieces = cible.nb_pieces
    node_piece = [child for child in node_arrondissement.children if child.name == nb_pieces][0]
    list_appart_similaires = []
    for child in node_piece.children:
        list_appart_similaires.append(child.name)

    return list_appart_similaires

def computeDelta(attribut, valeur_source, valeur_cible):
    if attribut == 'meuble' or attribut == 'cuisine_equipe' or attribut == 'cave':
        src = 1 if valeur_source else 0
        cible = 1 if valeur_cible else 0
        return (src - cible)*POIDS[attribut]

    # TODO:finir cette fonction
    """
    elif attribut = standing
        gérer catégorie
    elif attribut = etage
        gérer etage + ascenseuel
    else
        cas normaux
    
    
    
    
    
    """
# TODO Ecrire fonction calculant delta entre deux appartements, en faisant la somme des deltas
if __name__ == '__main__':
    root = Node('{}')
    df = pd.read_csv(filepath_or_buffer='Appartement.csv', sep=',')
    init_base_cas(root, df)
    descripteurs = []
    for column in df.columns:
        descripteurs.append(df[column][0])
    appart = Appartement(descripteurs)
    list = rememoration(appart,root)
    print(len(list))
    print(list[0].arrondissement)
    print(list[0].nb_pieces)
    print(f"appart : {appart.arrondissement}, {appart.nb_pieces}")
    print(f"appart_similaire : {list[0].arrondissement}, {list[0].nb_pieces}, {list[0].etage}")
    print(f"appart_similaire2 : {list[1].arrondissement}, {list[1].nb_pieces}, {list[1].etage}")
    print("delta meuble", computeDelta("meuble", True, False))


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
