class Evaluation():
    """Clase que aplica la funcion de evaluacion para los dos objetivo """
    def __init__(self,instance):
        self.instance=instance #instancia donde estan las  matriz de flujo y distancias

    def objective_fun1(self,solution):
        """ Calcula el valor para la funcion objetivo 1
         solucion en formato [2,3,1]--> edificio 2 en localidad 1, edificio 3 en localidad 2 """
        sumObjective1=0
        
        for i in range(0,self.instance.N):
            for j in range(i,self.instance.N):
                sumObjective1+=self.instance.flux1[solution[i]][solution[j]]*self.instance.distance[i][j]   #flujo * distancia

        return sumObjective1
    
    def objective_fun2(self,solution):
        """ Calcula el valor para la funcion objetivo 2
         solucion en formato [2,3,1]--> edificio 2 en localidad 1, edificio 3 en localidad 2 """
        sumObjective2=0
        for i in range(0,self.instance.N):
            for j in range(i,self.instance.N):
                sumObjective2+=self.instance.flux2[solution[i]][solution[j]]*self.instance.distance[i][j]
    
        return sumObjective2
    
    def setInstance(self,instance):
        """Cambiar la instacia actual que se esta leyendo """
        self.instance=instance