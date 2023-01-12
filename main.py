import numpy as np
import numpy.random as rd
import math
import ppvoisin
import optimiseppvoisin
import apminimum
import pvcprim
import esdemisomme

import matplotlib.pyplot as plt

#---------------------------------------
#Variables globales

#initialisation des abscisses
X = []
#initialisation des ordonnées
Y = []
#--------------------------------------


# initMatrice : initialise la matrice des poids D de dimension n x n contenant la
#               distance euclidienne entre chaque sommet
def initMatrice(n):
    #--------------------------------
    global X
    X = [ rd.rand() for _ in range(n) ]
    global Y
    Y = [ rd.rand() for _ in range(n) ]
    #initialisation de la matrice des poids
    D = np.zeros((n, n))

    #--------------------------------
    #pour chaque valeur de la matrice, on calcule la distance euclidienne
    for i in range (n):
        x = X[i]
        y = Y[i]
        for j in range (n):
            x2 = X[j]
            y2 = Y[j]
            D[i][j] = math.sqrt((x2 - x)**2 + (y2 - y)**2)
    #on renvoie la matrice des poids


    return D

#-------------------------------------- Fonction principale---------------------

def main(n):
    D = initMatrice(n)
    print("Matrice des distances pour ", n, "points dans l'invervalle [0; 1]:\n", D)
    #afficheMatrice(X, Y)
    #----Ppvoisin-----------------------
    cycle = Ppvoisin(D, 0)
    print("Le cycle pour Ppvoisin :\n", cycle)
    print("De poids : ", longueurCycle(D, cycle), "\n")
    afficheCycle(X, Y, cycle)
    #---OptimisePpvoisin----------------
    cycle = OptimisePpvoisin(cycle, D, X, Y)
    print("Le cycle pour OptimisePpvoisin :\n", cycle)
    print("De poids : ", longueurCycle(D, cycle), "\n")
    afficheCycle(X, Y, cycle)
    #---Apminimum-----------------------
    cycle = Apminimum(D)
    print("Le cycle pour Apminimum :\n", cycle)
    print("De poids : ", longueurCycle(D, cycle), "\n")
    afficheCycle(X, Y, cycle)
    #---Pvcprim------------------------
    cycle = Pvcprim(D, 0, X, Y)
    print("Le cycle pour Pvcprim :\n", cycle)
    print("De poids : ", longueurCycle(D, cycle), "\n")
    afficheCycle(X, Y, cycle)
    #---Esdemisomme--------------------
    cycle = Esdemisomme(D, 0)
    print("Le cycle pour Esdemisomme : \n", cycle)
    print("De poids : ", longueurCycle(D, cycle), "\n")
    afficheCycle(X, Y, cycle)


#---------------------------------------

# sommeListe : calcule la somme des éléments d'une liste
def sommeListe(list):
    somme = 0
    for i in list:
        somme += i
    return somme

# pourcentageChemin : calcule le pourcentage à partir de deux moyennes
# des distances des chemins
def pourcentageChemin(v1, v2):
    return 100 - (v1/v2) * 100

#-------------------------------------- Fonction statistique--------------------

# statFonction : teste sur 100 essais les différents algorithmes définis
#                et  évalue la longueur moyenne des cycles
def statFonction():
    #on définit les listes qui contiendront les cycles des différents algo
    cyclePpvoisin = []
    cycleOptimisePpvoisin = []
    cycleApminimum = []
    cyclePvcprim = []
    cycleEsdemisomme = []

    #et des listes contenant les sommes des poids pour chaque algo
    sommePpvoisin = []
    sommeOptimisePpvoisin = []
    sommeApminimum = []
    sommePvcprim = []
    sommeEsdemisomme = []
    #On calcule pour 100 essais
    for i in range(100):
        D = initMatrice(9)
        cycle = Ppvoisin(D, 0)
        cyclePpvoisin.append(cycle)
        sommePpvoisin.append(longueurCycle(D, cycle))

        cycle = OptimisePpvoisin(cycle, D, X, Y)
        cycleOptimisePpvoisin.append(cycle)
        sommeOptimisePpvoisin.append(longueurCycle(D, cycle))

        cycle = Apminimum(D)
        cycleApminimum.append(cycle)
        sommeApminimum.append(longueurCycle(D, cycle))

        cycle = Pvcprim(D, 0, X, Y)
        cyclePvcprim.append(cycle)
        sommePvcprim.append(longueurCycle(D, cycle))

        cycle = Esdemisomme(D, 0)
        cycleEsdemisomme.append(cycle)
        sommeEsdemisomme.append(longueurCycle(D, cycle))
    result = []
    result.append(("Ppvoisin", sommeListe(sommePpvoisin)/100))
    result.append(("OptiPpvoisin", sommeListe(sommeOptimisePpvoisin)/100))
    result.append(("Apminimum", sommeListe(sommeApminimum)/100))
    result.append(("Pvcprim", sommeListe(sommePvcprim)/100))
    result.append(("Esdemisomme", sommeListe(sommeEsdemisomme)/100))
    #--------------------Calcul des pourcentage---------------------------------
    Abscisses = []
    Ordonnees = []
    for i in range(5):
        x, y = result[i]
        Abscisses.append(x)
        Ordonnees.append(y)
        for j in range(5):
            if i <= j:
                continue
            x2, y2 = result[j]

            pourcentage = pourcentageChemin(y, y2)
            if pourcentage < 0 :
                print(x + " est " + str(-pourcentage) + " % plus long que " + x2)
            else :
                print(x + " est " + str(pourcentage) + " % plus court que " + x2)

    plt.bar(Abscisses, Ordonnees)
    plt.show()
    return result

#---------------------------------------

#affiche le graphique représentant la matrice donnée par son abscisses et son
# ordonnée
def afficheMatrice(X, Y):
    #--------------------------------
    #Représentation graphique des points
    plt.cla()
    for i in range(len(X)):
        for j in range(i+1, len(X)):
            plt.plot([X[i]] + [X[j]], [Y[i]] + [Y[j]], "o-")
    for i in range(len(X)):
        x = X[i]
        y = Y[i]
        plt.text(x, y, '%d' % i)
    plt.show()
    #--------------------------------

#affiche le graphique représentant le cycle passé en paramètre ainsi que les
# abscisses et ordonnées de la matrice des poids/distances
def afficheCycle(X, Y, cycle):
    #-----------------------------------
    #On récupère les abscisses et ordonnées
    # du cycle
    xo = [X[o] for o in cycle]
    yo = [Y[o] for o in cycle]

    #Puis on affiche le graphe
    plt.cla()
    plt.plot(xo, yo, "o-")
    for i in range(len(X)):
        x =xo[i]
        y = yo[i]
        plt.text(x, y, '%d' % cycle[i])
    #--------------------------------
    plt.show()


#Variable de test
N = 9
#D = initMatrice(N)
#afficheMatrice(X, Y)
#------------------------------------------------------
#Test Ppvoisin
s = 0
#P = Ppvoisin(D, s)
#afficheCycle(X, Y, P)
#------------------------------------------------------
#Test optimisePpvoisin
#Op = OptimisePpvoisin(P, D, X, Y)
#afficheCycle(X, Y, Op)
#------------------------------------------------------
#Test Apminimum
#AM = Apminimum(D)
#afficheCycle(X, Y, AM)
#------------------------------------------------------------------
#Test PVCPRIM
s = 0
#Pv = Pvcprim(D, s, X, Y)
#afficheCycle(X, Y, Pv)
#------------------------------------------------------------------
#Test Esdemisomme
#Es = Esdemisomme(D, s)
#afficheCycle(X, Y, Es)