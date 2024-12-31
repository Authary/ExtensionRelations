import PCA
from itertools import chain, combinations
import copy

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def context2Relation(context):
    Relation = {}
    Concepts = PCA.concepts(context)
    GroundSet = []
    Dimensions = []
    s = 0
    for i in range(1,len(context)):
        D = []
        for e in range(context[i]):
            GroundSet.append(e+s)
            D.append(e+s)
        s += context[i]
        Dimensions.append(D)
        
    Boites = []
    for C in Concepts:
        B = []
        for comp in range(len(C)):
            s = 0
            for i in range(1,comp+1):
                s += context[i]
            for elem in C[comp]:
                B.append(elem+s)
        Boites.append(B)

    PS = powerset(GroundSet) # Attention c'est grand
    for B in PS:
        ConclusionsB = []
        for C in Boites:
            if set(B).issubset(set(C)):
                ConclusionsB.append(C)
                
        if len(ConclusionsB) > 0:
            Relation[tuple(B)] = ConclusionsB
        else:
            Relation[tuple(B)] = [GroundSet]

    return (Relation,Dimensions)


def intersectExtensions(ens1,ens2):
    intersections = []
    for E1 in ens1:
        for E2 in ens2:
            intersections.append(list(set(E1).intersection(set(E2))))
    Result = []
    for E in intersections:
        add = True
        for E2 in intersections:
            if set(E).issubset(set(E2)) and not set(E2).issubset(set(E)):
                add = False
        if add and E not in Result:
            Result.append(E)
    return Result


def observation(relation,ens):
    if len(ens) == 0:
        return relation

    dimensionsObservatrices = []
    for dim in range(len(relation[1])):
        if len(set(ens).intersection(set(relation[1][dim]))) > 0:
            dimensionsObservatrices.append(dim)

    GroundSet = []
    for dim in relation[1]:
        GroundSet += dim

    Rel = copy.copy(relation[0])
    
    for dim in dimensionsObservatrices:
        newGroundSet = list(set(GroundSet).difference(set(relation[1][dim])))
        Observateurs = list(set(relation[1][dim]).intersection(set(ens)))
        PS = powerset(newGroundSet)
        newRelation = {}
        for B in list(PS):
            Conclusions = [newGroundSet]
            for obs in range(len(Observateurs)):
                box = list(B)+[Observateurs[obs]]
                box.sort()
                box = tuple(box)
                Conclusions = intersectExtensions(Conclusions,Rel[box])
            newRelation[tuple(B)] = Conclusions
        GroundSet = newGroundSet
        Rel = newRelation

        D = []
        for dim in range(len(relation[1])):
            if dim not in dimensionsObservatrices:
                D.append(relation[1][dim])

    return(newRelation,D)



'''
test
'''
'''
Context = ([[0,0],[0,1],[1,0]],2,2)
Relation = context2Relation(Context)
print(Relation)
Obs = observation(Relation,[0,1])
for P in Obs[0]:
    print(P," => ",Obs[0][P])
'''
