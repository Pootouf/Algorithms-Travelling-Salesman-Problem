import numpy as np
import numpy.random as rd
import math
#------------------------------------------------------
#Cocycle : Calcule le cocycle à partir d'un ensemble d'entiers de l'arbre
# et de la matrice des poids
def Cocycle(T, D):
    #Longueur colonnes/lignes
    n = np.shape(D)[0]

    #Initialisation d'un ensemble résultat
    Result = set()

    #Pour tous les sommets dans T
    for x in T:
        #Pour tous les sommets du graphe
        for y in range(n):
            # qui ne sont pas dans T
            if(y not in T):
                #On ajoute l'arête et le poids au résultat
                Result.add(((x, y), D[x][y]))
    return Result

#-----------------------------------------
# Symetrique : à partir d'une liste d'aretes, calcule les arêtes symétriques
def Symetrique(liste):
    #On initialise une liste résultat avec la liste
    result = liste.copy()

    # Pour chaque couple dans la liste résultat,
    # On ajoute son symétrique

    for (x, y) in liste:
        result.append((y, x))
    return result



#------------------------------------------------------
#Prim : Calcule l'ACM d'un graphe G représenté par sa matrice des poids D
# avec pour racine le sommet s
def Prim(D, s):
    # Initialisation d'un ensemble d'arêtes pour l'ACM
    #ACM = set()
    ACM = []
    #Initialisation d'un ensemble d'entiers
    T = {s}

    #-----------------------------------
    # Longueur colonnes/lignes
    n = np.shape(D)[0]
    #-----------------------------------
    #Fait la liste des sommets
    Sommets = {i for i in range(n)}
    #--------------------------------------------------
    # Tant que tous les sommets n'ont pas été traités
    while(T != Sommets):

        # On récupère le cocycle de T
        cocycle = Cocycle(T, D)

        # On initialise le poids min et l'arête de poids min
        # tout en sauvegardant sa valeur
        temp = cocycle.pop()
        min = temp[1]
        areteMin = temp[0]

        # Pour tous les couples du cocycle
        for ((x, y), d) in cocycle:

            # Si le poids du couple est inférieur au min
            if(d < min):
                # On change la valeur du min et de l'arête
                min = d
                areteMin = (x, y)
        T.add(areteMin[1])
        ACM.append(areteMin)
    return ACM

#-----------------------------------------
def rangeList(D, ACM, X, Y):
    #-----------------------------------
    # Longueur colonnes/lignes
    n = np.shape(D)[0]

    #Une liste contenant les sommets
    Sommets = [i for i in range(n)]

    #Pour chaque sommet de la liste
    for s in Sommets:
        #on prend ses successeurs
        temp = []
        for(x, y) in ACM:
            if(x == s):
                temp.append(y)
        #S'il n'a pas de successeurs
        #On passe au sommet suivant
        if(temp == []):
            continue
        #On sauvegarde l'indice de la première
        #arête du successeur du sommet
        ind = ACM.index((s, temp[0]))
        #Tant qu'on a encore des successeurs
        while(temp != []):
            #on regarde d'un point de vue
            # des coordonnées le plus petit
            min = math.inf
            indMin = -1
            for i in range(len(temp)):
                if(X[temp[i]] <= min):
                    indMin = i
                    min = X[temp[i]]
            #On supprime l'arête la plus petite
            del ACM[ACM.index((s, temp[indMin]))]
            #Et on la déplace avant les autres
            # arêtes successeurs
            ACM.insert(ind, ((s, temp[indMin])))
            #Puis on supprime de la liste
            # des successeurs
            del temp[indMin]

#-----------------------------------------
def ParcoursPrefixe(ACM, s):
    #On fait une copie de l'ACM
    ACM = ACM.copy()
    #On initialise le résultat avec la valeur
    # du sommet
    Result = [s]
    #Et la temporaire aussi
    temp = [s]
    #Tant qu'il reste des sommets à traiter
    while(temp != []):
        #On récupère le premier sommet à traiter
        lasty = temp[0]
        #Pour chaque arête de l'ACM
        for(x, y) in ACM:
            #On regarde si x correspond au
            # sommet à traiter
            if(x == lasty):
                #Si oui on ajoute y à l'indice suivant le sommet à traiter
                Result.insert(Result.index(lasty) + 1 ,y)
                #Et on ajoute y aux sommets à traiter
                temp.append(y)
        #On enlève le sommet traité
        del temp[0]

    return Result
#------------------------------------------------------
# Pvcprim : Renvoie à partir d'un graphe G représenté par
# sa matrice D des poids, les coordonnées X et Y et d'un sommet s,
# un cycle hamiltonien qui visite les sommets de l'ACM construit par l'algo de
# Prim dans l'ordre préfixe
def Pvcprim(D, s, X, Y):
    ACM = Prim(D, s)
    #-----------------------------------
    # Longueur colonnes/lignes
    n = np.shape(D)[0]
    #-----------------------------------
    rangeList(D, ACM, X, Y)
    Result = ParcoursPrefixe(ACM, s)

    while(Result[0] != s):
        temp = Result[0]
        del Result[0]
        Result.append(temp)
    Result.append(s)

    return Result

