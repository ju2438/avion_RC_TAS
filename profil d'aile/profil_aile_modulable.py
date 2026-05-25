## script python généré par IA (c'était pas difficile à faire) à partir du site https://skyhubgp.github.io/skyhub/article/profils-aero-NACA.html
###regarder le site pour bien comprendre les différents paramètres

import numpy as np
import matplotlib.pyplot as plt
from stl import mesh

def naca4_digits(m, p, t,n,c=1.0):
    """
    Génère les coordonnées d'un profil NACA à 4 chiffres.

    Paramètres :
    - m : Cambrure maximale (en % de la corde)
    - p : Position de la cambrure maximale (en dixième de % de la corde)
    - t : Épaisseur maximale (en % de la corde)
    - c : Longueur de la corde (par défaut 1.0)
    - n : Nombre de points à générer

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


def profil3D(m, p, t,l,emax,emin,n):
    nz=2*n#on choisit résolution identique selon z que selon x et y
    xu, yu, xl, yl = naca4_digits(m, p, t,n)
    x=np.concatenate((xu,xl))#taille 2*n
    y=np.concatenate((yu,yl))#taille 2*n
    z=np.linspace(0,l,nz)#taille nz=2*n

    #generation of regression on z axis
    scale1=np.linspace(emax,emin+5*(emax-emin)/6,nz//3)
    scale2=np.linspace(emin+5*(emax-emin)/6,emin+3*(emax-emin)/6,nz//3)
    scale3=np.linspace(emin+3*(emax-emin)/6,emin,nz//3)
    scale_X=np.concatenate((scale1,scale2,scale3))

    scale4=np.linspace(emax,emin+5*(emax-emin)/6,nz//3)
    scale5=np.linspace(emin+5*(emax-emin)/6,emin+3*(emax-emin)/6,nz//3)
    scale6=np.linspace(emin+3*(emax-emin)/6,emin,nz//3)
    scale_Y=np.concatenate((scale4,scale5,scale6))

    X=np.outer(scale_X,x)#taille n*2*n
    Y=np.outer(scale_Y,y)#taille n*2*n
    Z=np.outer(z,np.ones(2*n))#taille n*2*nz
    return X,Y,Z
    



def affiche_profil2D(m,p,t,n,export):
    # Exemple d'utilisation pour un profil NACA 2412
    xu, yu, xl, yl = naca4_digits(m, p, t,n)

    # Affichage du profil
    plt.figure(figsize=(10, 5))
    plt.plot(xu, yu, label='Extrados')
    plt.plot(xl, yl, label='Intrados')
    plt.axis('equal')
    plt.grid(True)
    plt.title(f'Profil NACA {m}{p}{t}')
    plt.xlabel('x/c')
    plt.ylabel('y/c')
    plt.legend()
    plt.show()

    if export:
        export_nervure_svg(m,p,t,xu,yu,xl,yl)

def export_stl(X, Y, Z,m,p,t):
    """
    Crée un fichier STL à partir des matrices X, Y, Z de plot_surface.
    Chaque cellule de la grille est découpée en 2 triangles.
    """
    nz, np_ = X.shape  # nz tranches, np_ points par tranche

    triangles = []

    for i in range(nz - 1):
        for j in range(np_ - 1):
            # 4 coins de la cellule
            p0 = [X[i,   j],   Y[i,   j],   Z[i,   j]]
            p1 = [X[i+1, j],   Y[i+1, j],   Z[i+1, j]]
            p2 = [X[i+1, j+1], Y[i+1, j+1], Z[i+1, j+1]]
            p3 = [X[i,   j+1], Y[i,   j+1], Z[i,   j+1]]

            # Triangle 1 : p0, p1, p2
            triangles.append([p0, p1, p2])
            # Triangle 2 : p0, p2, p3
            triangles.append([p0, p2, p3])

    triangles = np.array(triangles)  # shape (N, 3, 3)

    # Création du mesh STL
    aile = mesh.Mesh(np.zeros(len(triangles), dtype=mesh.Mesh.dtype))
    for i, tri in enumerate(triangles):
        for j in range(3):
            aile.vectors[i][j] = tri[j]
    aile.save(f"NACA_{m}{p}{t}.stl")
    print(f"Fichier STL sauvegardé : fichier_STL ({len(triangles)} triangles)")



def export_nervure_svg(m,p,t,xu,yu,xl,yl):
    """ crée un fichier svg avec les points de la nervure"""

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(xu, yu, color='black')
    ax.plot(xl, yl, color='black')
    ax.axis('equal')
    # Sauvegarde en SVG
    fig.savefig(f"nervure_{m}{p}{t}.svg", format='svg')
    plt.close(fig)
    print(f"Profil 2D sauvegardé en SVG : {f"nervure_{m}{p}{t}.stl"}")


def affiche_profil3D(m,p,t,l,emax,emin,n,export):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    X, Y, Z = profil3D(m, p, t, l,emax,emin,n)
    #show figure"""e"""""
    ax.plot_surface(X, Y, Z, cmap="coolwarm")
    ax.set_aspect('equal')
    plt.show()
    #export
    if export:
        export_stl(X,Y,Z,m,p,t)

n=300#nbr points pleaaase multiple de 3
m, p, t = 4, 4, 18
emax,emin,l=1,0.4,3
export=True#true if want to create a STL file
affiche_profil2D(m,p,t,n,export)
affiche_profil3D(m,p,t,l,emax,emin,n,export)



