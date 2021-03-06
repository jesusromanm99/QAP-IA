# from Instance import Instance,QAP_INSTANCES
# from Evaluation import Evaluation
# from Pareto import Solution,ParetoSet
# import random as rd
from M3AS import testQap as m3as_test
from spea import test_qap as spea_test
from Pareto import ParetoSet
import sys
from Metrics import Metrics


# ins1=Instance(QAP_INSTANCES[0]) ##creo  la Instancia
# ins1.reading_data() #Leo los datos del archivo
# ev=Evaluation(ins1) #Genero mis funciones objetivos para esa instancia
# PS=ParetoSet() #creo mi conjunto pareto

# #alternative= [[1,3,4,2],[1,3,4,2],[1,3,4,2]]

# P=[] #Poblacion
# N=3 #Tamaño de la poblacion

# for i in range(N):
#     solution=Solution(rd.sample(range(ins1.N), ins1.N),ev)
#     if(solution.constraint_check(P)):
#         P.append(solution)
#     else:
#         print('Solucion No valida')

# print('----------------------')
# PS.merge(P)
# for i in range(len(P)):
#     # print(f'X{i}, su F1 es {ev.objective_fun1(P[i].solution)}, su F2 es {ev.objective_fun2(P[i].solution)}')
#     [y1,y2]=P[i].get_eval_solution()
#     print(f'X{i}, su F1 es {y1}, su F2 es {y2}')

# print('Lista de soluciones')
# for ps in PS.solutions:
#     # print(f'X{i}, su F1 es {ev.objective_fun1(ps.solution)}, su F2 es {ev.objective_fun2(ps.solution)}')
#     [y1,y2]=ps.get_eval_solution()
#     print(f'X{i}, su F1 es {y1}, su F2 es {y2}')


instance = int(sys.argv[1])
pareto_true = ParetoSet([])

pareto_m3as = m3as_test(n=5, ins_nro=instance)
pareto_true.merge( [i for i in pareto_m3as.solutions] )

pareto_spea = spea_test(n=5, ins_nro=instance)

pareto_true.merge( [i for i in pareto_spea.solutions] )

 
sm1 = 0
sm2 = 0
sm3 = 0
sm4 = 0
mm1 = 0
mm2 = 0
mm3 = 0
mm4 = 0
for i in range(5):

    pareto_m3as = m3as_test(n=1, ins_nro=instance)
    # pareto_true.merge( [i for i in pareto_m3as.solutions])

    pareto_spea = spea_test(n=1, ins_nro=instance)
    # pareto_true.merge([i for i in pareto_spea.solutions])

    

    sm1 += Metrics.m1(pareto_true, pareto_spea)
    sm2 += Metrics.m2(pareto_spea, 1000)
    sm3 += Metrics.m3(pareto_spea)
    sm4 += Metrics.m4(pareto_true, pareto_spea)
    mm1 += Metrics.m1(pareto_true, pareto_m3as)
    mm2 += Metrics.m2(pareto_m3as, 1000)
    mm3 += Metrics.m3(pareto_m3as)
    mm4 += Metrics.m4(pareto_true, pareto_m3as)

print('>>>>>>>>>>SPEA')
print('Metrica m1:', sm1/5)
print('Metrica m2:', sm2/5)
print('Metrica m3:', sm3/5)
print('Metrica m4:', sm4/5)

print('>>>>>>>>>M3AS')
print('Metrica m1:', mm1/5)
print('Metrica m2:', mm2/5)
print('Metrica m3:', mm3/5)
print('Metrica m4:', mm4/5)
