import numpy as np
import matplotlib.pyplot as plt

#Conversion en milimètre
mm = 10**(-3)

# Initialisation de la matrice pour r <= 0
longueur_z = 12*mm
hauteur_r = 3*mm

pas = 0.1*mm

dimension_en_z = longueur_z/pas
dimension_en_r = hauteur_r/pas

matrice_pot = np.zeros((int(dimension_en_r), int(dimension_en_z))) # (30 x 120), (r x z)


""" Conditions frontières """

# L'électrode central (r=0) longue de 7,5 mm est maintenue à 0V
    # Puisque la matrice que nous avons créé contient déjà des zéro, nous n'avons pas besoin de changer quoi que ce soit
""" Useless:
    longueur_tige = 7.5*mm
    nbr_pas_tige = longueur_tige/pas # Le nombre de carré de la grille qu'ooccupe la tige

    for i in matrice[dimension_en_z-nbr_pas_tige:,0]:
"""
# Mur de droite, z = 12: potentiel = 0V
    # Puisque la matrice que nous avons créé contient déjà des zéro, nous n'avons pas besoin de changer quoi que ce soit

# Mur en angle: potentiel = -300 V. 
    # L'angle est tel que la ligne tracé par le mur a une pente de 1
for i in range(30):
    matrice_pot[(i,i)] = -300


# Mur du haut, r=30: -300V
for i in range(29,119): # Indice pour les dimension de z = [3 ; 12[ mm
    matrice_pot[(29,i)] = -300

# Initialisation d'une copie de la matrice pour toujours avoir accès à une matrice qui représente t=0
Potentiel_initial = matrice_pot.copy()

""" Définition de fonctions """


def pot_fixe(r,z):
    """
    Fonction servant à vérifier si on se situe à un endroit où le potentiel est fixe: 
        - L'électrode, r = 0, z = [4.5;120[  : 0V
        - Mur droit, r = [0;3], z = 12       : 0V
        - Mur en angle, r = z = [0;3]        : -300V
        - Mur haut, r = 30, z = [3;12[       : -300V
    Entré: Point de la matrice (r, z)
    Sortie: Bool
    """
    bool_electrode = r == 0 and z>=44
    bool_mur_droit = r<=29 and z == 119
    bool_mur_angle = r>= z and z<= 29
    bool_mur_haut = r == 29 and z>= 29

    return bool_electrode or bool_mur_droit or bool_mur_angle or bool_mur_haut

def maj_r_pas_0(V_avant_r, V_arrière_r, V_avant_z, V_arrière_z, R):
    """
    Utilise la formule trouvé en #1 a) pour trouver le potentiel mis à jour pour 
    les points au alentour données.
    """
    V_maj = (V_avant_r + V_arrière_r + V_avant_z + V_arrière_z)/4 + pas(V_avant_r-V_arrière_r)/8*R
    return V_maj


def diffusion(ancien_pot):
    nouveau_pot = Potentiel_initial.copy() # On reprend la matrice qui a les conditions initiales

    for r in range(29,-1, -1):  # On itère sur le rayon mais du plafond vers le centre (pour que ça aille plus vite)
        if r == 0:
            for z in range(0,119):  # On mets à jour le potentiel pour chaque ligne
                if pot_fixe(r,z):
                    continue
            #for z in range(1,44): # On mets à jour le potentiel pour la ligne à r=0
                nouveau_pot[r, z] = (4*ancien_pot[1,z]+ancien_pot[0,z+1]+ancien_pot[0,z-1])/6

        else:
            for z in range(0,119):  # On mets à jour le potentiel pour chaque ligne
                if pot_fixe(r,z):
                    continue

                R = ancien_pot[r, z] # rayon actuel
                nouveau_pot[r,z] = (ancien_pot[r+1, z]+ancien_pot[r-1, z]+ancien_pot[r, z+1]+ancien_pot[r,z-1])/4\
                    +pas*(ancien_pot[r+1, z]-ancien_pot[r-1, z])/8*R
                
    return nouveau_pot


interer = True

iterations = 0 

epsilon = 0.001
while run :
    iterations += 1
    old = matrice_pot.copy()
    matrice_pot = diffusion(matrice_pot)
    diff = matrice_pot-old
    if np.linalg.norm(diff,ord=np.inf) < epsilon:
        run = False
    #tmp_potentiel = new_potentiel

print(f"Took {iterations} miam miam iterations")

plt.imshow(matrice_pot, cmap='magma', origin='lower')
plt.colorbar(label='Potentiel électrique (V)')
plt.xlabel('r (mm)')
plt.ylabel('z (mm)')
plt.title('Potentiel dans la chambre à ionisation')
plt.show()

#test