""" Méthode de Jacobi, 
notation:
    - R correspond à une mesure du rayon
    - Z correspond à une mesure sur l'axe Z
    - r indice lié au rayon
    - z indice lié à l'axe Z
    """
import numpy as np
import matplotlib.pyplot as plt
import time


# Enregistrez l'heure de début
temps_début = time.time()

#Conversion en milimètre
mm = 10**(-3)

# Initialisation de la matrice pour r <= 0
longueur_Z = 12*mm
hauteur_R = 3*mm

pas = 0.1*mm

dimension_en_z = longueur_Z/pas + 1 # Pour le 0
dimension_en_r = hauteur_R/pas + 1 # Pour le 0

matrice_pot = np.zeros((int(dimension_en_r), int(dimension_en_z))) # (31 x 121), (r x z)


""" Conditions frontières """

# L'électrode central (R=0) longue de 7,5 mm est maintenue à 0V
    # Puisque la matrice que nous avons créé contient déjà des zéro, nous n'avons pas besoin de changer quoi que ce soit
##########################################

# Mur de droite, Z = 12: potentiel = 0V
    # Puisque la matrice que nous avons créé contient déjà des zéro, nous n'avons pas besoin de changer quoi que ce soit
#########################################

# Mur en angle: potentiel = -300 V. 
    # L'angle est tel que la ligne tracé par le mur a une pente de 1
for i in range(31):
    matrice_pot[(i,i)] = -300
########################################

# Mur du haut, r=30: -300V
for i in range(30,120): # Indice pour les dimension de z = [3 ; 12[ mm
    matrice_pot[(30,i)] = -300
#################################

"""
Le potentiel est fixe au endroits suivants: 
    - L'électrode, R = 0, Z = [4.5;120[ mm : 0V      => Fixe pour indices: r == 0 and z>=45
    - Mur droit, R = [0;3], Z = 12 mm      : 0V      => Fixe pour indices: r<=30 and z == 120
    - Mur en angle, R >= Z = [0;3]  mm      : -300V  => Fixe pour indices: r>= z and z<= 30
    - Mur haut, R = 30, Z = [3;12[ mm      : -300V   => Fixe pour indices: r == 30 and z>= 30
"""
#########################################################################################

# On crée une copie de la matrice original pour toujours y avoir accès 
matrice_initiale = matrice_pot.copy()

""" Définition de fonctions """

def diffusion(potentiel):
    """
    Entré: np array, Grille de potentiel
    Sortie: np array, Grille de potentiel après diffusion """
    nouveau_pot = matrice_initiale.copy()
    for r in range(29,-1, -1):
        # On itère sur le rayon à partir du plafond vers le centre (excluant r=30, soit R=3mm, puisque le potentiel y est fixe)
        if r == 0:
            for z in range(1,46):  
                # On itère sur Z jusqu'au début de l'électrode (soit z=46 ou Z < 45mm)
                nouveau_pot[r, z] = (4*potentiel[1,z]+potentiel[0,z+1]+potentiel[0,z-1])/6

        else:
            for z in range(119, -1, -1):  
                # On itère sur Z du fond ver l'avant en excluant le fond et ce qui se situe par dessus le mur en angle et 
                if nouveau_pot[r, z] == -300:
                    # Fait en sorte qu'on itère par pour les indices qui dépasse le mur en angle
                    break

                R = r*10 # rayon actuel
                nouveau_pot[r,z] = (potentiel[r+1, z]+potentiel[r-1, z]+potentiel[r, z+1]+potentiel[r,z-1])/4\
                    +(pas/(8*R))*(potentiel[r+1, z]-potentiel[r-1, z])
                
    return nouveau_pot



rouler = True           # Servira à arrêter les itérations
iterations = 0          # Compteur d'itérations
arrêt = 1e-9            # Lorsque chaque itération ne différerons entre elles que de ce facteurs, on arrête
max_interation = 20000  # Nombre max d'itérations pour éviter que ça roule à l'infinie si ça converge pas.


while rouler :
    iterations += 1

    ancien_potentiel = matrice_pot.copy()

    matrice_pot = diffusion(matrice_pot)
    #diff = np.abs(np.mean(matrice_pot)) - np.abs(np.mean(old))                 #Autre moyen de faire la diff
    diff = matrice_pot-ancien_potentiel
    if np.linalg.norm(diff,ord=np.inf) < arrêt or iterations > max_interation:
    #if diff < epsilon:                                                         #lié à l'autre moyen de vérifier la dif
    #if iterations == 300:
        rouler = False

# Calculez la différence, qui est le temps d'exécution de votre code
temps_fin = time.time()
temps_exécution = temps_fin - temps_début


# Imprimer le nombre d'itération
print(f"Le temps d'exécution est {temps_exécution} secondes.")
print(f"Took {iterations} miam miam iterations")

# créer une matrice à l'enver de la matrice du potentiel et la concaténer avec la première.
matrice_pot_inv = np.flip(matrice_pot, axis=0)
Potentiel_plan_r_z = np.concatenate((matrice_pot_inv, matrice_pot[1:,:]), axis=0)

# Faire le graphique
plt.imshow(Potentiel_plan_r_z, cmap='turbo', origin='lower', extent=[0, 12, -3, 3])
plt.colorbar(label='Potentiel électrique (V)')
plt.xlabel('Z [mm]')
plt.ylabel('Rayon [mm]')
plt.title('Potentiel dans la chambre à ionisation')

# Ajouter le nombre d'itération et le délais d'exécution sur le graphique
plt.text(0, -5, f"Nombre d'itération: {iterations}", color='black')
plt.text(0, -5.6, f"Temps d'exécusion: {round(temps_exécution, 2)} [s]", color='black')


plt.show()