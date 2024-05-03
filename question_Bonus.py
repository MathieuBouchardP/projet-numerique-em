""" Sur-Relaxation et Gauss-Seidel, 
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


""" Conditions frontières, on change la matrice initiale:

Le potentiel est fixe au endroits suivants: 
    - L'électrode, R = 0, Z = [4.5;120[ mm : 0V      => Fixe pour indices: r == 0 and z>=45
    - Mur droit, R = [0;3], Z = 12 mm      : 0V      => Fixe pour indices: r<=30 and z == 120
    - Mur en angle, R >= Z = [0;3]  mm      : -300V  => Fixe pour indices: r>= z and z<= 30
    - Mur haut, R = 30, Z = [3;12[ mm      : -300V   => Fixe pour indices: r == 30 and z>= 30
"""

# L'électrode central (R=0) longue de 7,5 mm est maintenue à 0V => OK

# Mur de droite, Z = 12: potentiel = 0V => OK

# Mur en angle: potentiel = -300 V. 
    # L'angle est tel que la ligne tracé par le mur a une pente de 1
for i in range(31):
    matrice_pot[(i,i)] = -300

# Mur du haut, r=30: -300V
for i in range(30,121): # Indice pour Z = [3 ; 12[ mm
    matrice_pot[(30,i)] = -300

# On crée une copie de la matrice original pour toujours y avoir accès (style un 'template')
matrice_initiale = matrice_pot.copy()



""" Définition de fonctions """
w = 0.878
def diffusion(potentiel):
    """
    Entré: np array, Grille de potentiel
    Sortie: np array, Grille de potentiel après diffusion """
    
    for r in range(29,-1, -1):  
        # On itère sur le rayon à partir du plafond vers le centre (excluant r=30, soit R=3mm, puisque le potentiel y est fixe)
        if r == 0:
            for z in range(1,46):  
                # On itère sur Z jusqu'au début de l'électrode (soit z=46 ou Z < 45mm)
                potentiel[r, z] = (1+w)*(4*potentiel[1,z]+potentiel[0,z+1]+potentiel[0,z-1])/6 - w*potentiel[r, z]

        else:
            for z in range(119, -1, -1):  
                # On itère sur Z du fond ver l'avant en excluant le fond et ce qui se situe par dessus le mur en angle et 
                if potentiel[r, z] == -300:
                    # Fait en sorte qu'on itère par pour les indices qui dépasse le mur en angle
                    break

                R = r*10 # rayon actuel
                potentiel[r,z] = (1+w)*((potentiel[r+1, z]+potentiel[r-1, z]+potentiel[r, z+1]+potentiel[r,z-1])/4\
                    +(pas/(8*R))*(potentiel[r+1, z]-potentiel[r-1, z])) - w*potentiel[r, z]
                
    return potentiel


rouler = True           # Servira à arrêter les itérations
iterations = 0          # Compteur d'itérations
arrêt = 1e-9            # Lorsque chaque itération ne différerons entre elles que de ce facteurs, on arrête
max_interation = 20000  # Nombre max d'itérations pour éviter que ça roule à l'infinie si ça converge pas.

while rouler :
    iterations += 1

    ancien_potentiel = matrice_pot.copy()
    matrice_pot = diffusion(matrice_pot)
    différence = matrice_pot-ancien_potentiel

    if np.linalg.norm(différence,ord=np.inf) < arrêt or iterations > max_interation:
        rouler = False

    #diff = np.abs(np.mean(matrice_pot)) - np.abs(np.mean(ancien_potentiel))                 #Autre moyen de faire la différence
    #if diff < arrêt:                                                         #lié à l'autre moyen de vérifier la différence

# Calculez la différence, qui est le temps d'exécution du code
temps_fin = time.time()
temps_exécution = temps_fin - temps_début


# Imprimer le nombre d'itération
print(f"Le temps d'exécution est {temps_exécution} secondes.")
print(f"{iterations} itération ont été nécessaires.")

# Créer une matrice à miroire de la matrice du potentiel et la concaténer avec la première.
matrice_pot_inv = np.flip(matrice_pot, axis=0)
Potentiel_plan_r_z = np.concatenate((matrice_pot_inv, matrice_pot[1:,:]), axis=0)

# Faire la figure
plt.imshow(Potentiel_plan_r_z, cmap='turbo', extent=[0, 12, -3, 3])
plt.colorbar(label='Potentiel électrique [V]')
plt.xlabel('Z [mm]')
plt.ylabel('Rayon [mm]')
#plt.title("Potentiel de la chambre d'ionisation")

# Ajouter le nombre d'itération et le délais d'exécution sur le graphique
plt.text(0, -4.5, f"Nombre d'itérations: {iterations}", color='black')
plt.text(0, -5.1, f"Temps d'exécution: {round(temps_exécution, 2)} [s]", color='black')


plt.show()