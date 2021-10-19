
QAP_INSTANCES=["files/qapUni.75.0.1.qap.txt","files/qapUni.75.p75.1.qap.txt"]

class Instance:
	def __init__(self,file):
		self.flux1=[]  #objetivo1
		self.flux2=[] #objetivo2
		self.distance=[] #distancia
		self.file=file  #archivo de la instancia que se va a leer
		self.N=0 #Numero de ciudades
	
	def reading_data(self):
		f=open(self.file,'r')
		n = int(f.readline()) # nro localidades
		self.N=n
		for i in range(3):
			for j in range(n):
				if(i==0):
					self.flux1.append([float(e) for e in f.readline().split()])
				elif(i==1):		
					self.flux2.append([float(e) for e in f.readline().split()])
				else:
					self.distance.append([float(e) for e in f.readline().split()])
			f.readline()
		f.close()




ins1=Instance(QAP_INSTANCES[0])##que instancia leer index:0-> instancia 1, index:1->intancia 2
ins1.reading_data() #leemos del archivo
ins2=Instance(QAP_INSTANCES[1])