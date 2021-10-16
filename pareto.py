

class Pareto:
    # constructor
    def __init__(self, y1, y2):
        self.y1 = y1
        self.y2 = y2

	# Metodo que verifica si u domina a v
    def covers(u, v):
        if u.y1 <= v.y1 and u.y2 <= v.y2:
            if u.y1 < v.y1 or u.y2 < v.y2:
                return True
        return False
    # to string 
    def __str__(self):
        return "(" + str(self.y1) + "," + str(self.y2) + ")"

class ParetoSet:
    # constructor
    def __init__(self, paretoArray=[]):
        self.paretos = paretoArray

    # Metodo que retorna todas las soluciones no dominadas de una poblacion dada
    def collect_non_dominated_solutions(population):
        no_dominated_solutions = []
        for u in population:
            contador = 0
            for v in population:
                if Pareto.covers(u, v):
                    contador += 1
            if contador == 0:
                no_dominated_solutions.append(u)
        return no_dominated_solutions

    # Metodo que combina dos paretos set en uno
    def combine_pareto_sets(pareto_set1, pareto_set2):
        combined_pareto_set = pareto_set1+pareto_set2

        return ParetoSet.collect_non_dominated_solutions(combined_pareto_set)

    def __repr__(self):
        return str([str(p) for p in self.paretos])


if __name__ == "__main__":
    a = Pareto(1, 3)
    b = Pareto(2, 2)
    c = Pareto(3,1)
    d = Pareto(1,5)
    population = [a, b, c]
    population2 = [d]
    x=ParetoSet.combine_pareto_sets(population, population2)
    print('combined', ParetoSet(x))
    print('population1', ParetoSet(population))
    print('population2', ParetoSet(population2))
    # print(a.covers(b))
    # print(a.covers(a))
    # print(b.covers(c))


