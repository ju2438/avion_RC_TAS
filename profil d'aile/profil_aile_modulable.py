## script python généré par IA (c'était pas difficile à faire) à partir du site https://skyhubgp.github.io/skyhub/article/profils-aero-NACA.html
###regarder le site pour bien comprendre les différents paramètres

import numpy as np
import matplotlib.pyplot as plt

def naca4_digits(m, p, t, c=1.0, n=200):
    """
    Génère les coordonnées d'un profil NACA à 4 chiffres.

    Paramètres :
    - m : Cambrure maximale (en % de la corde)
    - p : Position de la cambrure maximale (en dixième de % de la corde)
    - t : Épaisseur maximale (en % de la corde)
    - c : Longueur de la corde (par défaut 1.0)
    - n : Nombre de points à générer (par défaut 200)

    Retourne :
    - xu, yu : Coordonnées de l'extrados
    - xl, yl : Coordonnées de l'intrados
    """
    # Conversion des paramètres en valeurs utilisables
    m = m / 100.0
    p = p / 10.0
    t = t / 100.0

    # Génération des points x le long de la corde
    x = np.linspace(0, c, n)

    # Calcul de la ligne de cambrure yc
    yc = np.zeros_like(x)
    for i in range(len(x)):
        if x[i] < p * c:
            yc[i] = (m / (p ** 2)) * (2 * p * (x[i] / c) - (x[i] / c) ** 2)
        else:
            yc[i] = (m / ((1 - p) ** 2)) * ((1 - 2 * p) + 2 * p * (x[i] / c) - (x[i] / c) ** 2)

    # Calcul de l'épaisseur yt
    yt = 5 * t * c * (0.2969 * np.sqrt(x / c) - 0.1260 * (x / c) - 0.3516 * (x / c) ** 2 + 0.2843 * (x / c) ** 3 - 0.1015 * (x / c) ** 4)

    # Calcul de l'angle θ
    dyc_dx = np.gradient(yc, x)
    theta = np.arctan(dyc_dx)

    # Calcul des coordonnées de l'extrados et de l'intrados
    xu = x - yt * np.sin(theta)
    yu = yc + yt * np.cos(theta)
    xl = x + yt * np.sin(theta)
    yl = yc - yt * np.cos(theta)

    return xu, yu, xl, yl



def affiche_profil(m,p,t):
    # Exemple d'utilisation pour un profil NACA 2412
    xu, yu, xl, yl = naca4_digits(m, p, t)

    # Affichage du profil
    plt.figure(figsize=(10, 5))
    plt.plot(xu, yu, label='Extrados')
    plt.plot(xl, yl, label='Intrados')
    plt.axis('equal')
    plt.title(f'Profil NACA {m}{p}{t}')
    plt.xlabel('x/c')
    plt.ylabel('y/c')
    plt.legend()
    plt.grid(True)
    plt.show()


m, p, t = 2, 4, 12
affiche_profil(m,p,t)

###il faut maintenant créer le profil en 3D et exporter les points en SVG


