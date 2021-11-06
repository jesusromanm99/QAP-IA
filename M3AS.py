from Instance import Instance, QAP_INSTANCES
from Pareto import ParetoSet
from Pareto import Solution
from random import randint,random
from Evaluation import Evaluation
from Metrics import Metrics


class Ant():
    def __init__(self, beta, ant_number, total_ants, ferom_mat, visib_mats, objectives, ev):
        self.beta = beta
        self.ant_number = ant_number
        self.total_ants = total_ants
        self.ferom_mat = ferom_mat
        self.objectives = objectives
        self.visib_mats = visib_mats
        self.ev = ev
        
    def probability(self, city_number, feasible_nodes):
        """
        @param city_number: ciudad actual.

        @feasible_nodes: lista de posibles ciudades a ser visitadas en el siguiente movimiento.
        """
        lamda = self.ant_number / self.total_ants #lambda es una palabra reservada
        total = 0
        prob_list = list() #cada elemento tiene el numero de ciudad y su probabilidad asociada
        for j in feasible_nodes:
            total = total + self.ferom_mat[city_number][j] * self.visib_mats[0][city_number][j] ** \
                (lamda * self.beta) * self.visib_mats[1][city_number][j] ** ((1 - lamda) * self.beta)
            
        for j in feasible_nodes:
            prob = (self.ferom_mat[city_number][j] * self.visib_mats[0][city_number][j] ** (lamda * self.beta) \
                * self.visib_mats[1][city_number][j] ** ((1 - lamda) * self.beta)) / total
            prob_list.append([j, prob])

        return prob_list

    def build_solution(self):
        sol_len = len(self.ferom_mat)
        sol = [randint(0, sol_len - 1)]
        while(len(sol) < sol_len):
            probs = self.probability(sol[-1], [i for i in range(sol_len) if i not in sol])
            aux = [p[1] for p in probs]
            limits = [sum(aux[:i+1]) for i in range(len(aux))]
            aux = random()
            for i in range(len(limits)):
                if aux <= limits[i]:
                    sol.append(probs[i][0])
                    break
        # print('sol', sol)
        return Solution(sol, self.ev)

 


class M3as():
    def __init__(self, taumax, taumin, beta, rho, cost_mats, dist_mat, total_ants, total_generations, ev):
        self.taumax = taumax
        self.taumin = taumin
        self.beta = beta
        self.rho = rho
        self.total_ants = total_ants
        self.total_generations = total_generations
        self.pareto_set = ParetoSet()
        self.visib_mats = []
        self.objectives = []
        self.max_values = []
        self.ev = ev

        self.init_max_min(cost_mats, dist_mat)
        self.init_feromone_matrix(cost_mats, taumax)
        self.init_visibility_matrix(cost_mats)

    def init_visibility_matrix(self, cost_mats):
        for cost_mat in cost_mats:
            visib_mat = []
            for row in cost_mat:
                visib_mat.append([1.0/e if e != 0.0 else e for e in row])
            self.visib_mats.append(visib_mat)

    def init_feromone_matrix(self, cost_mats, taumax):
        n = len(cost_mats[0])
        self.ferom_mat = []
        for i in range(n):
            self.ferom_mat.append([taumax for j in range(n)])

    def init_max_min(self, cost_mats, dist_mat):
        #flux_mats == cost_mats: en esta variable se recibe las matrices de flujo
        n = len(cost_mats[0])
        max_dist = 0
        for dist_row in dist_mat:
            if max(dist_row) > max_dist:
                max_dist = max(dist_row)
        for cost_mat in cost_mats:
            max_val = 0
            for i in range(n):
                if max(cost_mat[i]) > max_val:
                    max_val = max(cost_mat[i])
            self.max_values.append(max_val*max_dist)
            # ev = Evaluation()
            # self.objectives.append(ev)

    def run(self):
        for i in range(self.total_generations):
            # print("Generation: ", i)
            for ant_number in range(self.total_ants):
                ant = Ant(self.beta, ant_number, self.total_ants,
                          self.ferom_mat, self.visib_mats, self.objectives,self.ev)

                sol = ant.build_solution()
            # print(">>>>>>sol", sol)
            self.pareto_set.update(sol)
        return self.pareto_set
            # self.update_feromone_matrix(sol)


def testQap(n=5, ins_nro=0):
    taumax = 0.0000053
    taumin = 0.000000053
    beta = 1
    rho = 0.02
    total_ants = 10
    total_generations = 100
    # instancias = parse_qap()

    pareto_set = ParetoSet()

    instancia = QAP_INSTANCES[ins_nro]
    instancias = Instance(instancia)  # creo  la Instancia
    instancias.reading_data()  # Leo los datos del archivo
    flux1, flux2 = instancias.flux1, instancias.flux2
    flux_mats = [flux1, flux2]
    # print(flux_mats)
    dist_mat = instancias.distance
    # print('dist_mat', dist_mat)

    ev=Evaluation(instancias) #Genero mis funciones objetivos para esa instancia

    m3as = M3as(taumax, taumin, beta, rho, flux_mats,
                dist_mat, total_ants, total_generations, ev)
    for i in range(n):
        print("Iteracion: ", i+1,'para', instancia)
        result = m3as.run()
        soluciones = [r for r in result.solutions]
        pareto_set.merge(soluciones)
    return pareto_set

if __name__ == '__main__':
    pareto_set = testQap(n=2, ins_nro=0)