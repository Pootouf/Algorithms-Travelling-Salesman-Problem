import numpy as np
import numpy.random as rd
import math

#-------------------------------------------------------------------------------

#Ppvoisin : à partir d'une matrice M et d'un sommet s
def Ppvoisin(M, s):
    #------------------------------------
    n = np.shape(M)[0] #nombre de colonnes
    #On réalise une copie de la matrice pour
    # ne pas modifier M
    N = np.copy(M)
    #------------------------------------

    #On récupère la chaîne eulérienne
    # à partir d'un sommet s
    Sommets = [i for  i in range(0, n)]
    Sommets.remove(s)
    L = Successeur(N, s, [s], Sommets)

    #On la transforme en cycle hamiltonien
    L.append(s)
    return L




#-----------------------------------------
#Successeur : à partir d'une matrice M et d'un sommet s; ajoute à une liste L
#           les successeurs du sommet s selon la liste de tous les sommets S
def Successeur(M, s, L, S):

    #-------------------------------------
    # Nombre de colonnes
    n = np.shape(M)[0]

    #-------------------------------------
    # Teste si on a appliqué la fonction à tous les sommets
    if(len(L) == n):
        return L

    #Variable initialisée au premier sommet non traité
    #du graphe, représenté par la liste S
    indiceMin = S[0]

    #-------------------------------------

    for j in range(1, n) :

        # Si j vaut le sommet,
        # on passe au prochain tour de boucle
        if (j == s or j in L):
            continue

        #Si on trouve une valeur inférieure au minimum,
        #on change la valeur du minimum
        if (M[s][j] < M[s][indiceMin]):
            indiceMin = j
    #-------------------------------------

    #On met une valeur impossible à atteindre pour
    # signifier que la fonction est passée par ces valeurs
    M[s][indiceMin] = math.inf
    M[indiceMin][s] = math.inf

    #On enlève le sommet de la liste des sommets à traiter
    S.remove(indiceMin)

    #On ajoute le sommet traité à la liste des résultats
    L.append(indiceMin)

    #-------------------------------------
    return Successeur(M, indiceMin, L, S)

