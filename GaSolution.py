from Pareto import Solution
import sys

class GaSolution(Solution):
    """
    Class for representing a solution in a genetic algorithm.
    """
    def __init__(self, solution, objectives):
        """
        Initialize a solution.
        :param chromosome: The chromosome of the solution.
        """
        Solution.__init__(self, solution, objectives)
        self.fitness = 999999999
        self.evaluation = self.get_eval_solution()



class GeneticOperators:

    def crossover(self, sol_a, sol_b):
        """
        Crossover de las soluciones dadas como parametros.
        Se toma el primer elemento de sol_a y se copia en el hijo. Luego se 
        consulta el valor del primer elemento de sol_b y se averigua su 
        posicion en sol_a, luego se copia el elemento de sol_a en el hijo
        manteniendo la posicion, asi hasta querer insertar un elemento ya
        presente en el hijo.
        
        Luego se copian los elementos restantes de sol_b en el hijo.
        
        @param sol_a: Primera solucion
        @param sol_b: Segunda solucion
        @return: lista de hijos
        """    
        child = [-1 for n in xrange(len(sol_a.solution))]
        k = 0
        
        #fijar elementos de la primera solucion
        while True:
            child[k] = sol_a.solution[k]
            k = sol_a.solution.index(sol_b.solution[k])
            if child[k] >= 0:
                break
        
        #fijar elementos de la segunda solucion
        for i, s in enumerate(sol_b.solution):
            if child[i] < 0:
                child[i] = s
        
        return [GaSolution(child, sol_a.objectives)]
    
    def mutation(self, sol):
        """
        Realiza la operación de mutación sobre la solución.
        Elige dos posiciones aleatorias y realiza un intercambio de elementos
        
        @param sol: la solución a mutar
        """
        n = len(sol.solution) - 1
        i = random.randint(0, n)
        j = random.randint(0, n)
        while i == j:
            import time
            random.seed(time.time())
            j = random.randint(0, n)
        sol.solution[i], sol.solution[j] = sol.solution[j], sol.solution[i]
