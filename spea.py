#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Pareto import Solution,ParetoSet
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

    def run(self, P, num_generations):
        """
        Ejecuta el algoritmo SPEA
        
        @param P: la poblacion inicial
        @param num_generations: el numero maximo de generaciones
        """
        ps = ParetoSet()
        for i in xrange(num_generations):
            ps.merge(P)
            for s in ps.solutions:
                if s in P:
                    P.remove(s)

            #if len(ps.solutions) > self.max_pareto_points:
            #    self.reduce_pareto_set(ps)
            self.fitness_assignment(ps, P)
            mating_pool = self.selection(P, ps)
            #P = self.next_generation(mating_pool, len(P))

    def fitness_assignment(self, pareto_set, population):
        for pareto_ind in pareto_set.solutions:
            count = 0
            for population_ind in population:
                if pareto_ind.dominates(population_ind):
                    count = count + 1
            strength = count / (len(population) + 1)
            if strength != 0:
                pareto_ind.fitness = 1 / strength

        for population_ind in population:
            suma = 0
            for pareto_ind in pareto_set.solutions:
                if pareto_ind.dominates(population_ind):
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
