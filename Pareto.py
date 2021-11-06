class Solution:

    def __init__(self,solution,objective):
        """
            @params: solution: solucion actual del QAP formato vector
                     obj: objeto que contiene los dos objetivos a Evaluar
         """
        self.solution=solution
        self.obj=objective  #Se guarda el objeto que maneja la funciones de evaluacion
        
    def dominate(self,other_solution):
        """Determina si una funcion domina a otra aplicando la formula de dominancia de soluciones """
        
        # print(other_solution)
        # print('-'*65)
        if( self.obj.objective_fun1(self.solution)<=self.obj.objective_fun1(other_solution)
        and self.obj.objective_fun2(self.solution)<=self.obj.objective_fun2(other_solution)):
            if( self.obj.objective_fun1(self.solution) < self.obj.objective_fun1(other_solution)
                or self.obj.objective_fun2(self.solution) < self.obj.objective_fun2(other_solution)):
                return True
        return False

    def constraint_check(self,P):
        """Verifica las dos restricciones para una solucion """

        if(self.is_valid() and not self.is_in_P(P) ):
            return True
        return False

    def is_valid(self):
        """ Verfica que la solucion Generada no contenga edificios repetidos en diferentes lugares """

        if (len(set(self.solution))==len(self.solution)): return True
        return False

    def is_in_P(self,P):
        """Funcion que verifica si una solucion ya forma parte de la Poblacion """
        if(self.solution in [p.solution for p in P ]):
            return True
        
        return False
    
    def get_eval_solution(self):
        """ Retorna la evaluacion de la solucion """
        y1 = self.obj.objective_fun1(self.solution)
        y2 = self.obj.objective_fun2(self.solution)
        return [y1,y2]

class ParetoSet:

    def __init__(self,solutions=[],evaluation=None):
        """@params: listas de soluciones que formaran parte del conjunto Pareto """

        self.solutions=solutions
        self.evaluation=evaluation


    def update(self,candidate):
        """Determina si el candidato ya es dominado por una de las soluciones """

        solution_to_delete=[] #Lista que soluciones que van a ser eliminadas del CP por ser dominada por el candidato
        for solution in self.solutions:
            if(solution.dominate(candidate.solution)):   
                return 
            else:
                if(candidate.dominate(solution.solution)):
                    solution_to_delete.append(solution)

        self.remove_solutions_domidated(candidate,solution_to_delete)

    def remove_solutions_domidated(self,newSolution,solutions_to_remove):
        """Funcion que agrega una nueva colucion al conjunto pareto y elimina aquellas 
            soluciones que son dominadas por la  nueva solucion
         """
        for solution in solutions_to_remove:
            self.solutions.remove(solution) ##elimino las soluciones dominadas

        self.solutions.append(newSolution) #agrego la nueva solucion
                
    def merge(self,candidates):
        """Lista de soluciones para actualizar el frente Pareto """
        # print('candidatos',candidates)
        if not self.solutions:
            self.solutions = [candidates[0]]
            candidates = candidates[1:]
        for candidate in candidates:
            # print('candidato',candidate)
            self.update(candidate)

    def get_eval_solutions(self):
        """Retorna las evaluaciones de las soluciones """
        return [solution.get_eval_solution() for solution in self.solutions]

