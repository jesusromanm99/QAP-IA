#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Pareto import Solution,ParetoSet
from GaSolution import GaSolution, GeneticOperators
from Instance import Instance, QAP_INSTANCES
from Pareto import ParetoSet
from Pareto import Solution
from random import randint,random
from Evaluation import Evaluation
from Metrics import Metrics
import random
import sys

class SPEA:
    def __init__(self, num_objectives, genetic_operators, max_pareto_points, cr=1.0, mr=0.1):
        pareto_set = ParetoSet(None)
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
        ps = ParetoSet()
        for i in range(num_generations):
            # print(len(P),P[0])
            ps.merge(P)
            for s in ps.solutions:
                if s in P:
                    P.remove(s)

            #if len(ps.solutions) > self.max_pareto_points:
            #    self.reduce_pareto_set(ps)
            # print('ueoueoauaeouaeo')
            # print(len(P), P[0])
            self.fitness_assignment(ps, P)
            mating_pool = self.selection(P, ps)
            P = self.next_generation(mating_pool, len(P),ev)
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
        Realiza la selección y retorna el mating_pool
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
        genéticos
        
        @param mating_pool: mating pool utilizada para construir la siguiente 
                            generación de individuos
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

        return Q

def test_qap(n = 5, inst_nro = 0):
    total_ind = 10
    total_generations = 10
    max_pareto_size = 20
    op = GeneticOperators()

    pareto_set = ParetoSet()

    instancia = QAP_INSTANCES[inst_nro]

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
        print("Iteracion: ", i+1,'para', instancia)
        result = spea.run(pop, total_generations,ev)
        soluciones = [r for r in result.solutions]

        pareto_set.merge(soluciones)

    return pareto_set

if __name__ == '__main__':
    print(test_qap(n=5, inst_nro=0))