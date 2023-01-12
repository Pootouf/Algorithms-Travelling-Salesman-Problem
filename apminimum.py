import numpy as np
import numpy.random as rd
import math
import pvcprim

#------------------------------------------------------
#ListeAretesDispo : prend une liste d'arêtes à ne pas traiter et une matrice M pour calculer toutes les arêtes disponibles
def ListeAretesDispo(AretesTraitees, M):
    #-----------------------------------
    # Longueur colonnes/lignes
    n = np.shape(M)[0]

    # Initialisation du résultat
    L = []
    #-----------------------------------
    #Compte le degré des sommets et les met dans une liste
    Sommets = [0 for i in range(n)]
    for (x,y) in AretesTraitees:
        Sommets[x] = Sommets[x] + 1
        Sommets[y] = Sommets[y] + 1

    # On ajoute les arêtes à partir de M

    # On récupère la liste des arêtes indisponibles
    # par transitivité
    AretesIndispo = Transitivite(AretesTraitees)
    for i in range(n):
        for j in range(n):
            if(Sommets[i] >= 2 or Sommets[j] >= 2):
                continue
            # Si on n'est pas sur la diagonale
            if(M[i][j] > 0):
                # Et que l'arête n'est pas indisponible
                if(i, j) not in AretesIndispo:
                    # On ajoute l'arête au résultat
                    L.append((i, j))
    #-----------------------------------
    return L

#-----------------------------------------
# Transitivite : à partir de la liste des arêtes traitées, calcule les arêtes indisponibles par transitivité
def Transitivite(AretesTraitees):
    #On initialise une liste résultat avec la liste des
    # arêtes traitées
    AretesIndispo = AretesTraitees.copy()

    # Pour chaque couple dans la liste résultat,
    # On ajoute son symétrique

    for (x, y) in AretesTraitees:
        AretesIndispo.add((y, x))

    result = AretesIndispo.copy()
    #Pour chaque couple d'arêtes traitées
    for (x, y) in AretesIndispo:
        # Et pour chaque (x, y), pour chaque couple
        # d'arêtes traitées
        for (i, j) in AretesIndispo:

            #On calcule la transitivité, et on ajoute
            # l'arête correspondante à la liste résultat
            if(y == i):
                result.add((j, x))
                result.add((x, j))
    if(AretesTraitees == result):
        return result
    return Transitivite(result)
#-----------------------------------------
#FermeCycle : ajoute l'arête manquante à une liste pour fermer son cycle
def FermeCycle(L):
    #Compte le degré des sommets et les met dans une liste
    Sommets = [0 for i in range(len(L) + 1)]
    for (x,y) in L:
        Sommets[x] = Sommets[x] + 1
        Sommets[y] = Sommets[y] + 1
    #On crée une variable temporaire pour stocker les extrémités
    # du cycle
    temp  = []
    for i in range(len(Sommets)):
        if(Sommets[i] != 2):
            temp.append(i)

    #Puis on ajoute l'arête à la liste pour fermer le cycle
    # temp ne contient que les deux valeurs aux extrémités
    L.append((temp[0], temp[1]))
    return L
#-----------------------------------------
#areteVersCycle : transforme une liste d'arêtes en un cycle hamiltonien
def areteVersCycle(L):
    aretes = Symetrique(L.copy())
    result = []
    x,y = aretes[0]
    result.append(y)
    result.append(x)
    aretes.remove((x,y))
    aretes.remove((y, x))
    while aretes != []:
        #dernier indice de notre cycle actuellement
        end = result[len(result) - 1]
        for(x,y) in aretes:
            if x == end:
                result.append(y)
                aretes.remove((x,y))
                aretes.remove((y, x))
                break
            if y == end:
                result.append(x)
                aretes.remove((x,y))
                aretes.remove((y, x))
                break
    return result
#-----------------------------------------
#Apminimum : renvoie le cycle de poids minimum selon l'algo
# de l'arête de poids minimum
def Apminimum(D):
    #-----------------------------------
    #Initialisation de la variable résultat
    Result = []

    #Initialisation de la liste des arêtes disponibles
    AretesDispo = ListeAretesDispo({}, D)

    #-----------------------------------
    # Longueur colonnes/lignes
    n = np.shape(D)[0]
    #-----------------------------------
    while(AretesDispo != []):

        #On initialise à la valeur la plus grande possible
        poidsMin = math.inf

        #Et à la première valeur possible
        aretePoidsMin = AretesDispo[0]

        #Pour toutes les arêtes disponibles
        for (x, y) in AretesDispo:
            #Si le poids de l'arête est plus petit que le min
            if(D[x][y] < poidsMin):

                #On donne sa valeur au min
                poidsMin = D[x][y]
                aretePoidsMin = (x, y)
        #Et on ajoute l'arête de poids min au résultat
        Result.append(aretePoidsMin)


        #Si la liste contient tous les sommets
        if (len(Result) >= n):
            #On sort de la boucle
            break
        #Sinon on recalcule la liste des arêtes disponibles
        AretesDispo = ListeAretesDispo(set(Result), D)

    #On ajoute l'arête manquante pour fermer le cycle
    Result = FermeCycle(Result)
    #-----------------------------------
    return areteVersCycle(Result)

