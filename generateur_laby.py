import random
from random import randint

directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
              #Est     Ouest     Sud     Nord

mur_verticaux = []
for i in range(20):
    mur_verticaux.append([1] * 20)

mur_horizontaux = []
for i in range(20):
    mur_horizontaux.append([1] * 20)

case_visite = []
for i in range(20):
    case_visite.append([False for j in range(20)])

x_depart = randint(0, 19)
y_depart = randint(0, 19)

def apparition_coffres(nombre_de_coffre):
    liste_coffres = []
    coffres_places = 0

    while coffres_places < nombre_de_coffre:
        x = randint(0, 19)
        y = randint(0, 19)

        if (x, y) not in liste_coffres:
            liste_coffres.append((x, y))
            coffres_places += 1
    return liste_coffres

positions_des_coffres = apparition_coffres(4)

def apparition(x_depart, y_depart, case_visite) :
	case_visite[y_depart][x_depart] = True
	pile_visite = []
	pile_visite.append((y_depart, x_depart))
	return pile_visite

pile_visite = apparition(0, 0, case_visite)

while len(pile_visite) > 0:
    case_actuelle = pile_visite[-1]
    x = case_actuelle[0]
    y = case_actuelle[1]
    voisins_valides = []
    
    for (dx, dy) in directions:
        voisin_x = x + dx
        voisin_y = y + dy
        if 0 <= voisin_x < 20 and 0 <= voisin_y < 20:
            if case_visite[voisin_y][voisin_x] == False:
                voisins_valides.append((voisin_x, voisin_y))

    if len(voisins_valides) > 0 :
        prochain_voisin = random.choice(voisins_valides)
        nv_x = prochain_voisin[0]
        nv_y = prochain_voisin[1]

        if nv_x == x + 1:
            mur_verticaux[y][x] = 0
        elif nv_x == x - 1:
            mur_verticaux[y][x - 1] = 0
        elif nv_y == y + 1:
            mur_horizontaux[y][x] = 0
        elif nv_y == y - 1:
            mur_horizontaux[y - 1][x] = 0

        case_visite[nv_y][nv_x] = True
        pile_visite.append((nv_x, nv_y))
        
    else:
        pile_visite.pop()



def afficher_labyrinthe(mur_horizontaux, mur_verticaux, positions_des_coffres):
    hauteur = len(mur_verticaux)
    largeur = len(mur_verticaux[0])
    
    # 1. Le plafond
    print("+---" * largeur + "+")
    
    # 2. On parcourt les lignes et les colonnes
    for y in range(hauteur):
        ligne_verticale = "|"
        ligne_horizontale = "+"
        
        for x in range(largeur):
            # --- MODIFICATION ICI : On vérifie si la case (x, y) a un coffre ---
            if (x, y) in positions_des_coffres:
                ligne_verticale += " C "  # On met un C au milieu (3 caractères en tout)
            else:
                ligne_verticale += "   "  # 3 espaces vides classiques
            
            # Gestion des murs verticaux à droite
            if mur_verticaux[y][x] == 1:
                ligne_verticale += "|"
            else:
                ligne_verticale += " "
            
            # Gestion des murs horizontaux en bas
            if mur_horizontaux[y][x] == 1:
                ligne_horizontale += "---+"
            else:
                ligne_horizontale += "   +"
        
        print(ligne_verticale)
        print(ligne_horizontale)

print("Labyrinthe généré avec succès :\n")
afficher_labyrinthe(mur_horizontaux, mur_verticaux, positions_des_coffres)