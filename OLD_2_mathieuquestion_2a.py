import numpy as np
import matplotlib.pyplot as plt
import time

# Enregistrez l'heure de début
start_time = time.time()

#Conversion en milimètre
mm = 10**(-3)

# Initialisation de la matrice pour r <= 0
longueur_z = 12*mm
hauteur_r = 3*mm

pas = 0.1*mm

dimension_en_z = longueur_z/pas #+ 1 # Pour le 0
dimension_en_r = hauteur_r/pas #+ 1 # Pour le 0

matrice_pot = np.zeros((int(dimension_en_r), int(dimension_en_z))) # (31 x 121), (r x z)


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


def diffusion(ancien_pot):
    #nouveau_pot = Potentiel_initial.copy() # On reprend la matrice qui a les conditions initiales
    nouveau_pot = ancien_pot
    for r in range(28,-1, -1):  # On itère sur le rayon mais du plafond vers le centre (pour que ça aille plus vite)
        if r == 0:
            for z in range(0,45):  # On mets à jour le potentiel pour chaque ligne
            #for z in range(1,44): # On mets à jour le potentiel pour la ligne à r=0
                nouveau_pot[r, z] = (4*ancien_pot[1,z]+ancien_pot[0,z+1]+ancien_pot[0,z-1])/6

        else:
            for z in range(118, -1, -1):  # On mets à jour le potentiel pour chaque ligne
                if ancien_pot[r, z] == -300:
                    #print('break')
                    break
                #if pot_fixe(r,z):
                   # continue
                #print(r,z)
                #R = ancien_pot[r, z] # rayon actuel
                nouveau_pot[r,z] = (ancien_pot[r+1, z]+ancien_pot[r-1, z]+ancien_pot[r, z+1]+ancien_pot[r,z-1])/4\
                    +(pas/(8*r*10))*(ancien_pot[r+1, z]-ancien_pot[r-1, z])
                
    return nouveau_pot


rouler = True

iterations = 0 

epsilon = 0.00001
while rouler :
    iterations += 1
    old = matrice_pot.copy()
    matrice_pot = diffusion(matrice_pot)
    diff = np.abs(np.mean(matrice_pot)) - np.abs(np.mean(old))
    #diff = matrice_pot-old
    #if np.linalg.norm(diff,ord=np.inf) < epsilon:
    if diff < epsilon:
    #if iterations == 1:
        rouler = False
    #tmp_potentiel = new_potentiel

end_time = time.time()
# Calculez la différence, qui est le temps d'exécution de votre code
execution_time = end_time - start_time

print(f"Le temps d'exécution est {execution_time} secondes.")

print(f"Took {iterations} miam miam iterations")

plt.imshow(matrice_pot, cmap='magma', origin='lower', extent=[0, 12*mm, -3*mm, 3*mm])
plt.imshow(matrice_pot, cmap='inferno', origin='lower')
plt.colorbar(label='Potentiel électrique (V)')
plt.xlabel('r (mm)')
plt.ylabel('z (mm)')
plt.title('Potentiel dans la chambre à ionisation')
plt.show()

V_miroir = np.flip(matrice_pot, axis=0)

#test