#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Pareto import ParetoSet
from GaSolution import GaSolution, GeneticOperators
from Instance import Instance, QAP_INSTANCES
from random import randint,random
from Evaluation import Evaluation
from Metrics import Metrics
from cluster import Cluster

import random
import sys

class SPEA:
    def __init__(self, num_objectives, genetic_operators, max_pareto_points, cr=1.0, mr=0.1):
        pareto_set = ParetoSet([])
        self.num_objectives = num_objectives
        self.genetic_operators = genetic_operators
        self.crossover_rate = cr
        self.mutation_rate = mr
        self.max_pareto_points = max_pareto_points

    def run(self, P, num_generations,ev):
        """
        Ejecuta el algoritmo SPEA
        
        @param P: la poblacion inicial
        @param num_generations: el numero maximo de generaciones
        """
        ps = ParetoSet([])
        for i in range(num_generations):
            #print("Generation: ", i)
            # print(len(P),P[0])
            if type(P)==[GaSolution]:
                raise Exception("ParetoSet")
            ps.merge(P)
            #print('after merge')
            for s in ps.solutions:
                if s in P:
                    P.remove(s)

            #print('after remove')

            if len(ps.solutions) > self.max_pareto_points:
                self.reduce_pareto_set(ps)
                ps.solutions=self.reduce_pareto_set(ps)
                
            # print('ueoueoauaeouaeo')
            # print(len(P), P[0])
            self.fitness_assignment(ps, P)
            #print('after fitness')
            mating_pool = self.selection(P, ps)
            #print('after selection')
            P = self.next_generation(mating_pool, len(P),ev)
            #print('after next generation')
        
        if len(ps.solutions) > self.max_pareto_points:
                self.reduce_pareto_set(ps)

        return ps

    def fitness_assignment(self, pareto_set: ParetoSet, population: [GaSolution]):
        # print(len(pareto_set.solutions),len(population))
        for pareto_ind in pareto_set.solutions:
            count = 0
            for population_ind in population:
                if pareto_ind.dominate(population_ind.solution):
                    count += 1
            strength = count / (len(population) + 1)
            if strength != 0:
                pareto_ind.fitness = 1 / strength

        for population_ind in population:
            suma = 0
            for pareto_ind in pareto_set.solutions:
                if pareto_ind.dominate(population_ind.solution):
                    suma = suma + 1.0/pareto_ind.fitness
            suma = suma + 1.0
            population_ind.fitness = 1 / suma

    def selection(self, population, pareto_set):
        """
        Realiza la selecci??n y retorna el mating_pool
        """
        pool = []
        unido = []
        unido.extend(population)
        unido.extend(pareto_set.solutions)
        pool_size = len(unido) / 2
        while len(pool) < pool_size:
            c1 = random.choice(unido)
            c2 = random.choice(unido)
            while c1 == c2:
                c2 = random.choice(unido)
            if c1.fitness > c2.fitness:
                pool.append(c1)
            else:
                pool.append(c2)
        return pool

    def next_generation(self, mating_pool, pop_size,ev):
        """
        Crea la siguiente generacion a partir del mating_pool y los operadores 
        gen??ticos
        
        @param mating_pool: mating pool utilizada para construir la siguiente 
                            generaci??n de individuos
        """
        Q = []
        
        #cruzamiento
        while len(Q) < pop_size:
            parents = []
            parents.append(random.choice(mating_pool))
            other = random.choice(mating_pool)
            parents.append(other)
            if random.random() < 1:
                children = self.genetic_operators.crossover(parents[0], parents[1],ev)
                Q.extend(children)
            else:
                Q.extend(parents)
        
        for ind in Q:
            if random.random() < self.mutation_rate:
                self.genetic_operators.mutation(ind)
                ind.evaluation = ind.get_eval_solution()

        # print(Q)
        return Q


    def reduce_pareto_set(self, par_set):
        """
        Realiza el clustering
        """
        lista_cluster=[]
        for solucion in par_set.solutions:
            cluster = Cluster()
            cluster.agregar_solucion(solucion)
            lista_cluster.append(cluster)
  
        while len(lista_cluster) > self.max_pareto_points:
            min_distancia = float('inf')
            for i in range (0,len(lista_cluster)-1):
                for j in range(i+1, len(lista_cluster)-1): 
                    c = lista_cluster[i]
                    distancia = c.calcular_distancia(lista_cluster[j])
                    if distancia < min_distancia:
                        min_distancia = distancia
                        c1 = i
                        c2 = j
               
            cluster = lista_cluster[c1].unir(lista_cluster[c2]) #retorna un nuevo cluster 
            del lista_cluster[c1]
            del lista_cluster[c2]

            lista_cluster.append(cluster)
        
        par_set=[]
        
        for cluster in lista_cluster:
            solucion = cluster.centroide()
            par_set.append(solucion)
            
        
        return par_set 
def test_qap(n = 5, ins_nro = 0):
    total_ind = 10
    total_generations = 100
    max_pareto_size = 20
    op = GeneticOperators()

    pareto_set = ParetoSet([])

    instancia = QAP_INSTANCES[ins_nro]

    instancias = Instance(instancia)  # creo  la Instancia
    instancias.reading_data()  # Leo los datos del archivo
    flux1, flux2 = instancias.flux1, instancias.flux2
    flux_mats = [flux1, flux2]
    # print(flux_mats)
    dist_mat = instancias.distance
    # print('dist_mat', dist_mat)
    objs = []

    ev=Evaluation(instancias) #Genero mis funciones objetivos para esa instancia
    spea = SPEA(len( dist_mat ), op, max_pareto_size)
    num_loc = len(dist_mat)
    
    
    for i in range(n):
        pop = []
        for _ in range(total_ind):
            sol = [j for j in range(num_loc)]
            random.shuffle(sol)
            pop.append(GaSolution(sol, ev))
        print("GA - Iteracion: ", i+1,'para', instancia)
        result = spea.run(pop, total_generations,ev)
        #print('after run', result, result.solutions)
        soluciones = [r for r in result.solutions]

        #print(soluciones)
        pareto_set.merge(soluciones)
        

    return pareto_set

if __name__ == '__main__':
    print()
    result = test_qap(n=2, ins_nro=0)
    print('-'*50)
    print(result.solutions )