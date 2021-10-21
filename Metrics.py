
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

class Metrics:
    def m1(self, paretoOptimo,pareto):
        optimoSolutions = paretoOptimo.get_eval_solutions()
        solutions = pareto.get_eval_solutions()
    # def m1(self, solution):
        # optimoSolutions = [[0,1],[1,0],[1,1],[0,0]]
        # solutions = [[2,3],[3,2],[3,3],[2,2]]

        sumatorio = 0
        for solution in solutions:
            sumatorio = min_dist(solution,optimoSolutions)
        return sumatorio/len(solutions)


ins1=Instance(QAP_INSTANCES[0]) ##creo  la Instancia
ins1.reading_data() #Leo los datos del archivo
ev=Evaluation(ins1) #Genero mis funciones objetivos para esa instancia
PS=ParetoSet() #creo mi conjunto pareto

#alternative= [[1,3,4,2],[1,3,4,2],[1,3,4,2]]

P=[] #Poblacion
N=3 #Tamaño de la poblacion

for i in range(N):
    solution=Solution(rd.sample(range(ins1.N), ins1.N),ev)
    if(solution.constraint_check(P)):
        P.append(solution)
    else:
        print('Solucion No valida')

print('----------------------')
PS.update(P)
for i in range(len(P)):
    # print(f'X{i}, su F1 es {ev.objective_fun1(P[i].solution)}, su F2 es {ev.objective_fun2(P[i].solution)}')
    [y1,y2]=P[i].get_eval_solution()
    print(f'X{i}, su F1 es {y1}, su F2 es {y2}')

print('Lista de soluciones')
for ps in PS.solutions:
    # print(f'X{i}, su F1 es {ev.objective_fun1(ps.solution)}, su F2 es {ev.objective_fun2(ps.solution)}')
    [y1,y2]=ps.get_eval_solution()
    print(f'X{i}, su F1 es {y1}, su F2 es {y2}')

m = Metrics()
print(m.m1(PS,PS))
# m.m1(PS)