import numpy as np
import numpy.random as rd
import math

#------------------------------------------------------
# intersection : A partir du cycle hamiltonien L,
#                renvoie si les arêtes ayant comme
#                sommet i et i+1 et j et j+1 se croisent
#                à partir des coordonnées X et Y
def intersection(L, i, j, X, Y):
    # Nombre de sommets len(X) = len(Y)
    n = len(X)
    #-----------------------------
    # La distance entre les abscisses de A et B
    # à partir de la variable X
    ABx = X[L[(i + 1)%n]] - X[L[i]]
    # A et B étant à la suite dans la liste L, on désignera
    # l'indice de leur abscisse respectivement par i et i+1
    # dans X

    # La distance entre les ordonnées de A et B
    # à partir de la variable Y
    ABy = Y[L[(i + 1)%n]] - Y[L[i]]
    # A et B étant à la suite dans la liste L, on désignera
    # l'indice de leur ordonnée respectivement par i et i+1
    # dans Y

    # La distance entre les abscisses de A et C
    # à partir de la variable X
    ACx = X[L[j]] - X[L[i]]


    # La distance entre les ordonnées de A et C
    # à partir de la variable Y
    ACy = Y[L[j]] - Y[L[i]]

    # La distance entre les abscisses de A et D
    # à partir de la variable X
    ADx = X[L[(j + 1)%n]] - X[L[i]]

    # La distance entre les ordonnées de A et D
    # à partir de la variable Y
    ADy = Y[L[(j + 1)%n]] - Y[L[i]]

    # La distance entre les abscisses de C et D
    # à partir de la variable X
    CDx = X[L[(j + 1)%n]] - X[L[j]]

    # La distance entre les ordonnées de C et D
    # à partir de la variable Y
    CDy = Y[L[(j + 1)%n]] - Y[L[j]]

    CAx = -ACx
    CAy = -ACy

    CBx = X[L[(i + 1)%n]] - X[L[j]]
    CBy = Y[L[(i + 1)%n]] - Y[L[j]]
#-----------------------------------

    # On calcule les déterminants
    det1 = ABx * ACy - ABy * ACx
    det2 = ABx * ADy - ABy * ADx
    det3 = CDx * CAy - CDy * CAx
    det4 = CDx * CBy - CDy * CBx

    #---------------------------

    return ((det1 * det2) < 0) and ((det3 * det4) < 0)

#-------------------------------------------------------------------

#EchangePositions : échange la position de deux éléments dans une liste
def EchangePositions(L, i, j):
    temp = L[i]
    L[i] = L[j]
    L[j] = temp
    return L

#-------------------------------------------------------------------
#ListeIntersections : calcule la liste des intersections d'un cycle L
#                     à partir des coordonnées X et Y
def ListeIntersections(L, X, Y):
    n = len(L) - 1
    Result = []
    #-----------------------------------
    for i in range(n):
        for j in range(i, n):
            if(intersection(L, i, j, X, Y)):
                 Result.append((i, j))
    return Result

#-------------------------------------------------------------------
# longueurCycle : calcule la longueur d'un cycle passé en paramètre à partir
#                 de la matrice des poids/distances
def longueurCycle(D, cycle):
    somme = 0
    for i in range(len(cycle) - 1):
        somme += D[cycle[i]][cycle[i+1]]
    return somme

#-------------------------------------------------------------------

def completeCycle(isEnd, L):
    temp = L.copy()
    if(isEnd):
        temp.insert(0, temp[len(temp) - 1])
    else:
        temp.append(temp[0])
    return temp

def auxOptimisePpvoisin(L, D, X, Y, isEnd):
    n = len(L) - 1
    intersec = []
    if(isEnd):
        del L[0]
    else:
        #On enleve la derniere valeur du cycle
        del L[n]
    #-----------------------------------
    #On calcule la liste des intersections restantes
    intersec = ListeIntersections(L, X, Y)
    #Tant qu'il reste des intersections dans la liste
    while(intersec != []):

        #Pour chaque couple d'arêtes dans la liste d'intersection
        for (i, j) in intersec:
            temp = L.copy()
            temp2 = L.copy()
            temp3 = L.copy()
            temp4 = L.copy()
            temp = EchangePositions(temp, (i+1)%n, j)
            temp2 = EchangePositions(temp2, i, j)
            temp3 = EchangePositions(temp3, (j+1)%n, i)
            temp4 = EchangePositions(temp4, (i+1)%n, (j+1)%n)
            if(longueurCycle(D, completeCycle(isEnd, temp)) <= longueurCycle(D, completeCycle(isEnd, L))):
                L = temp
                intersec = ListeIntersections(L, X, Y)
            if(longueurCycle(D, completeCycle(isEnd, temp2)) <= longueurCycle(D, completeCycle(isEnd, L))):
                L = temp2
                intersec = ListeIntersections(L, X, Y)
            if(longueurCycle(D, completeCycle(isEnd, temp3)) <= longueurCycle(D, completeCycle(isEnd, L))):
                L = temp3
                intersec = ListeIntersections(L, X, Y)
            if(longueurCycle(D, completeCycle(isEnd, temp4)) <= longueurCycle(D, completeCycle(isEnd, L))):
                L = temp4
                intersec = ListeIntersections(L, X, Y)
        I = ListeIntersections(L, X, Y)

        #Si on n'a pas trouvé de croisement avantageux
        # Donc que la liste d'intersections n'a pas changé
        if(intersec == I):
            break
        # Dans l'autre cas, on commence par les changements avantageux
        # On refait un tour de boucle
        else:
            intersec = I
    #-----------------------------------
    if(isEnd):
        L.insert(0, L[n - 1])
    else:
        #On ferme le cycle
        L.append(L[0])
    return L

#OptimisePpvoisin : A partir d'un cycle L renvoyé par Ppvoisin,
# et de la matrice des poids D avec les coordonnées X et Y
# décroise si le décroisement est avantageux tous les couples d'arêtes
# envisageables jusqu'à ce qu'il n'y ait plus aucun couple d'arêtes croisées.
def OptimisePpvoisin(L, D, X, Y):
    #On calcule notre cycle en décroisant
    L = auxOptimisePpvoisin(L, D, X, Y, False)
    #-----------------------------------
    L = auxOptimisePpvoisin(L, D, X, Y, True)
    return L
