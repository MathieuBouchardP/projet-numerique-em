import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    h, r = 1.5, 1.5
    a, b = (2*r+h)/(8*r), (2*r-h)/(8*r)

    # On crée la matrice Q à partir des noeuds choisis (voir pdf)
    # On peut trouver les probabilités des transitions à l'aide des équation trouvé en 1 a)
    Q = np.array([
        [0, 1/4, 0, 0, 0, 0, 0, 0],
        [1/4, 0, 1/4, 0, 0, 0, 0, 0],
        [0, 1/4, 0, 1/4, 0, 0, 0, 0],
        [0, 0, 1/4, 0, 1/4, 0, 0, 0],
        [0, 0, 0, 1/4, 0, 1/4, 0, 0],
        [0, 0, 0, 0, 1/4, 0, b, 0],
        [0, 0, 0, 0, 0, 2/3, 0, 1/6],
        [0, 0, 0, 0, 0, 0, 1/6, 0]
    ])
    
    # En faisant la matrice Q on peut faire la matrice R pour que le total des lignes égale à 1
    R = np.array([
        [0, 0, 0, 0, b, 0, 1/4, 0, a, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, b, 0, 0, 0, 0, 0, a, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, b, 0, 0, 0, 0, 0, 0, 0, a, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, b, 0, 0, 0, 0, 0, 0, 0, 0, 0, a, 0, 0, 0, 0, 0, 0, 0,],
        [b, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, a, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, a, 0, 0, 0, 1/4, 0,],
        [1/6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2/3, 1/6,]
    ])

    # On impose les potentiels aux frontières
    Vr = np.array([0, 0, 0, 0, 0, 0, 0, 0, -300, -300, -300, -300, -300, -300, -300, -300, -300, -300, -300,]).transpose()

    # La matrice np.eye(8) est notre premier supposition du potentiel aux noeuds transistoires
    N = np.linalg.inv(np.eye(8)-Q)

    # On obtient ensuite les valeurs aux noeuds transistoire en régime permanent
    B = np.matmul(N, R)
    Vt = np.matmul(B, Vr)
    # Les potentiels sont maintenant connues et le problème est résolu

    # Le reste du code sert à la mise en page du graphique etc
    V = np.array([
        [np.NAN, np.NAN, Vr[13], Vr[12], Vr[11], Vr[10], Vr[9], Vr[8], Vr[7],],
        [np.NAN, Vr[17], Vt[5], Vt[4], Vt[3], Vt[2], Vt[1], Vt[0], Vr[6]],
        [Vr[18], Vt[7], Vt[6], Vr[0], Vr[1], Vr[2], Vr[3], Vr[4], Vr[5],]
    ])

    fig = plt.figure(figsize=(12, 6),)
    ax = fig.subplots()
    
    V = np.concatenate((V, np.flip(V, axis=0)[1:,:]))
    im = ax.imshow(V, extent=[0,13.5,-3,3], cmap='turbo')

    cbar = fig.colorbar(im)
    cbar.set_label('Potentiel électrique [V]')
    ax.set_xticks(np.arange(0, 13.5, 1.5))
    ax.set_yticks(np.arange(-3, 4.5, 1.5))
    ax.set_xlabel('z [mm]')
    ax.set_ylabel('Rayon [mm]')
    ax.set_title("Potentiel de la chambre d'ionisation")
    
    for (i, j), z in np.ndenumerate(V):
        print(i,j)
        if z is not np.NAN:
            y = 0
            if i == 0:
                y = 2.4
            elif i == 1:
                y = 1.2
            elif i == 3:
                y = -1.2
            elif i == 4:
                y = -2.4
            ax.text(1.5*j+.75, y, '{:0.1f}'.format(z), ha='center', va='center',
                    bbox=dict(boxstyle='round', facecolor='white', edgecolor='0.3'),)
            
    plt.show()
