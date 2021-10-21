from Instance import Instance,QAP_INSTANCES
from Evaluation import Evaluation
from Pareto import Solution,ParetoSet
import random as rd

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
PS.merge(P)
for i in range(len(P)):
    # print(f'X{i}, su F1 es {ev.objective_fun1(P[i].solution)}, su F2 es {ev.objective_fun2(P[i].solution)}')
    [y1,y2]=P[i].get_eval_solution()
    print(f'X{i}, su F1 es {y1}, su F2 es {y2}')

print('Lista de soluciones')
for ps in PS.solutions:
    # print(f'X{i}, su F1 es {ev.objective_fun1(ps.solution)}, su F2 es {ev.objective_fun2(ps.solution)}')
    [y1,y2]=ps.get_eval_solution()
    print(f'X{i}, su F1 es {y1}, su F2 es {y2}')
