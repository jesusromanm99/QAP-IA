
from Instance import Instance,QAP_INSTANCES
from Evaluation import Evaluation
from Pareto import Solution,ParetoSet
import random as rd
import math

def distance(p1,p2):
    """
    Calculates the distance between two points.
    """
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def min_dist(point, points):
    """
    Calculates the minimum distance between a point and a set of points.
    """
    min_dist = float('inf')
    for p in points:
        dist = distance(p, point)
        if dist < min_dist:
            min_dist = dist
    return min_dist

def outRadius(list_points, point, radius):
    """
    Count the points in out of the radius of a point.
    """
    count = 0
    for p in list_points:
        dis = distance(p, point)
        if dis > radius:
            count += 1
    return count

def max_dist(point, points):
    """
    Calculates the maximum distance between a point and a set of points.
    """
    max_dist = 0
    for p in points:
        dist = distance(p, point)
        if dist > max_dist:
            max_dist = dist
    return max_dist

def included(list_points, point):
    """
    Checks if a point is included in a list of points. if so, returns True else False.
    """
    # print("list_points", list_points)
    # print("point", point)
    for p in list_points:
        if p[0] == point[0] and p[1] == point[1]:
            return True
    return False

def interset(list_points1, list_points2):
    """
    Calculates the intersection between two sets of points.
    """
    interset = []
    for p in list_points1:
        if included(list_points2, p):
            interset.append(p)
    return interset


class Metrics:
    def m1(paretoOptimo,pareto):
        optimoSolutions = paretoOptimo.get_eval_solutions()
        solutions = pareto.get_eval_solutions()
    #     optimoSolutions = [[1,4],[2,2],[4,1],[6,0]]
    #     solutions = [[2,6],[3,4],[5,3],[6,2]]

        sumatorio = 0
        for solution in solutions:
            sumatorio += min_dist(solution,optimoSolutions)
        return sumatorio/len(solutions)

    def m2(pareto, sigma):
    #     solutions = [[8,0],[7,1],[6,2],[5,3],[4,4],[3,5],[2,6],[1,7],[0,8]] # mejor distribucion
    #     solutions = [[8,0],[7,1],[6,2],[5,3],[1,7],[0,8]]
        try:
            solutions = pareto.get_eval_solutions()
            sumatorio = 0
            for solution in solutions:
                sumatorio += outRadius(solutions,solution,sigma)
            res = sumatorio/(len(solutions)-1)
            return res
        except:
            print("Error: Pareto set have a only solution, can't calculate m2")
            exit()

    def m3(pareto):
        # solutions = [[8,0],[7,1],[6,2],[5,3],[4,4],[3,5],[2,6],[1,7],[0,8]] # mejor distribucion
        # solutions = [[8,0],[7,1],[6,2],[5,3]] # peor distribucion
        solutions = pareto.get_eval_solutions()
        sumatorio = 0
        for solution in solutions:
            sumatorio += max_dist(solution,solutions)
        return math.sqrt(sumatorio)

    def m4(paretoOptimo, pareto):

        # optimoSolutions = [[8,0],[7,1],[4,4],[1,7],[0,8]] 
        # solutions = [[8,0],[7,1],[1,1]]
        optimoSolutions = paretoOptimo.get_eval_solutions()
        solutions = pareto.get_eval_solutions()
        fnf = interset(optimoSolutions,solutions)
        return 1 - (len(fnf)/len(solutions))

# ins1=Instance(QAP_INSTANCES[0]) ##creo  la Instancia
# ins1.reading_data() #Leo los datos del archivo
# ev=Evaluation(ins1) #Genero mis funciones objetivos para esa instancia
# PS=ParetoSet() #creo mi conjunto pareto

# P=[] #Poblacion
# N=3 #Tamaño de la poblacion

# for i in range(N):
#     solution=Solution(rd.sample(range(ins1.N), ins1.N),ev)
#     if(solution.constraint_check(P)):
#         P.append(solution)
#     else:
#         print('Solucion No valida')

# print('----------------------')
# PS.update(P)

# print("Metrica m1: ", Metrics.m1(PS,PS))
# print("Metrica m2: ", Metrics.m2(PS,3))
# print("Metrica m3: ", Metrics.m3(PS))
# print("Metrica m4: ", Metrics.m4(PS,PS))