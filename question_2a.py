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

matrice = np.zeros((int(dimension_en_r), int(dimension_en_z))) # (30 x 120), (r x z)


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
    matrice[(i,i)] = -300


# Mur du haut, r=30: -300V
for i in range(29,119): # Indice pour les dimension de z = [3 ; 12[ mm
    matrice[(29,i)] = -300


""" Définition de fonctions """

# Fonction servant à vérifier si on se situe à un endroit où le potentiel est fixe:

def pot_fixe(i,j):
    pass


plt.imshow(matrice, cmap='gist_ncar', origin='lower')
plt.colorbar(label='Potentiel électrique (V)')
plt.xlabel('r (mm)')
plt.ylabel('z (mm)')
plt.title('Potentiel dans la chambre à ionisation')
plt.show()
