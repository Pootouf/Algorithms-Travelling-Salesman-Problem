import numpy as np
import numpy.random as rd
import math
#------------------------------------------------------
#SuccesseursM : renvoie la liste des successeurs de s pour un graphe G dont la matrice d'adjacence est M
def SuccesseursM(M, s):
    n = np.shape(M)[0] #nombre de ligne de G = nombre sommets de G
    L =[]
    for j in range(n):
        if M[(s),j] > 0 :
            L.append(j)
    return(L)

#------------------------------------------------------
#minList : renvoie le minimum d'une liste passée en paramètre
def minList(L):
    min = math.inf
    indice = -1
    for i in range(len(L)):
        if L[i][1] < min:
            min = L[i][1]
            indice = i
    return indice, min

#Esdemisomme : calcule le cycle hamiltonien le plus optimal en
# énumérant toutes les solutions possibles et en choisissant les plus
# intéressantes.
# Prend un sommet s à partir duquel calculer le cycle, et la matrice des poids/
# distance D.
def Esdemisomme(D, s):
    #on définit une liste contenant comme premier élément un couple
    # tel que le premier élément du couple est une liste contenant le sommet de
    # départ (cette liste représentera le parcours courant dans l'arbre), et
    # le second élément représente le résultat de la demi somme pour l'arête
    # calculée selon le chemin défini dans la liste en premier élément.
    L = [([s], aux(D, s, []))]

    #une fois la demi-somme et sa racine définies, on appelle la fonction
    # récursive pour calculer le chemin selon l'arbre des possibilités.
    # L représente donc la liste des cas et s la racine
    return Esdemisommerec(D, L, s)


#------------------------------------------------------
# Esdemisommerec : calcule la plus petite demi-somme pour l'arbre
#                  avec son cycle associé à partir
#                  de l la liste des cas et du graphe D des distances/poids
def Esdemisommerec(D, l, r):
    n = np.shape(D)[0]
    #----------------------------------------------------
    #On réalise une copie de la liste des cas pour la modifer
    result = l.copy()

    while (result != []):
        #Et on initialise une liste pour le minimum
        listMin = []

        #Ainsi qu'une somme minimale, initialisée à l'infini
        sommeMin = math.inf
        #----------------------------------------------------
        #Puis on parcourt la liste des cas pour trouver la plus petite demi-somme
        #Ainsi que son chemin dans l'arbre
        for (list, somme) in result:
            if(somme < sommeMin):
                sommeMin = somme
                listMin = list

        if (listMin == []):
            return result

        # si notre liste a la même taille que le nombre de sommets
        if(len(listMin) ==  np.shape(D)[0]):
            #On cherche à fermer notre cycle actuel

            # on appelle temp le dernier sommet de notre liste
            temp = listMin[len(listMin) - 1]

            #on calcule la demi-somme du cycle en cours

            resultList = listMin.copy()
            resultSomme = aux(D, r, resultList)
            resultList.append(r)
            result.remove((listMin, sommeMin))

            result.append((resultList, resultSomme))
            continue
        #on regarde si le cycle a la demisomme la plus petite de tous les autres
        # éléments de la liste des cas (autrement dit si de tous les cycles
        # possibles, le notre est le plus petit), si oui c'est notre résultat
        if(len(listMin) == n +1):
            return listMin

        #----------------------------------------------------
        #On récupère le dernier sommet du cycle calculé actuellement
        s = listMin[len(listMin) - 1]
        # et on enlève le cas que l'on traite de la liste des cas
        result.remove((listMin, sommeMin))

        #Pour chaque successeur de s
        for i in SuccesseursM(D, s):
            # si le successeur est déjà dans la liste du cycle, on passe au suivant
            if i in listMin:
                continue

            #On calcule la demi-somme pour le successeur de s à partir de notre cycle
            somme = aux(D, i, listMin)

            #On ajoute le successeur au cycle
            ls = listMin.copy()
            ls.append(i)
            #puis dans la liste de cas avec le résultat de sa demi-somme
            result.append((ls, somme))
    return result

#------------------------------------------------------
# aux : calcule la demi-somme des arêtes sortantes et incidentes
# minimum pour chaque sommet à partir d'une liste non vide, ou de la matrice
# uniquement sinon
def aux(D, s, L):
    #--------------------
    #Nombre de lignes/colonnes
    n = np.shape(D)[0]

    #Initialisation de la somme
    somme = 0

    #dans le cas de la racine (et donc la liste contenant le cycle est vide)
    if L == []:
        #Pour chaque ligne
        for i in range(n):

            #On initialise les minimums incidents et sortants
            min1 = math.inf
            min2 = math.inf

            #Pour chaque colonne
            for j in range(n):

                #Si on ne se trouve pas sur la diagonale
                if i != j:
                    #Et que la valeur trouvée est inférieure au premier min
                    if D[i][j] < min1:
                        #On donne la valeur trouvée au premier min et l'ancien min
                        # au 2nd
                        min2 = min1
                        min1 = D[i][j]
                        continue

                    # Si la valeur trouvée est inférieure au 2nd min uniquement
                    # On lui donne la valeur trouvée
                    if D[i][j] < min2:
                        min2 = D[i][j]
        #dans le cas où l'on explore une possibilité et donc que la liste n'est
        # pas vide
            #On ajoute les deux min à la somme
            somme += (min1 + min2)
    else:
        list = L.copy()

        min = np.zeros((n, 2))
        list.append(s)
        temp = list[0]

        for i in range (1, len(list)):
            temp2 = list[i]
            min[temp][1] = D[temp][temp2]
            min[temp2][0] = D[temp2][temp]
            temp = temp2

        sommetPrec = L[len(L)-1]
        PoidsAretePrec = D[sommetPrec][s]
        #Pour chaque ligne
        for i in range(n):

            #On initialise les minimums incidents et sortants
            min1 = math.inf
            min2 = math.inf
            initmin1= False
            initmin2 = False

            if min[i][0] != 0:
                min1 = min[i][0]
                initmin1 = True
            if min[i][1] != 0:
                min2 = min[i][1]
                initmin2 = True
            #Pour chaque colonne
            for j in range(n):

                if i != j :
                    if initmin2 and initmin1:
                        break
                    if initmin2:
                        if D[i][j] < min1 and min2 != D[i][j]:
                            min1 = D[i][j]
                        continue
                    if initmin1:
                        if D[i][j] < min2 and min1 != D[i][j]:
                            min2 = D[i][j]
                        continue
                    if D[i][j] < min1:
                            min2 = min1
                            min1 = D[i][j]
                            continue
                    if D[i][j] < min2:
                        min2 = D[i][j]

            #On ajoute les deux min à la somme
            somme += (min1 + min2)
    #Et on retourne la demi-somme
    return somme/2