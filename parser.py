

import os

bp = "instancias" + os.sep

tsp_instances = [bp + "KROAB100.TSP.TXT", bp + "kroac100.tsp.txt"]
qap_instances = [bp + "qapUni.75.0.1.qap.txt", bp + "qapUni.75.p75.1.qap.txt"]
y1 = ob1*dist
y2 = ob2*dist
def parse_qap():
				  # [        instancia uno        ] [        instancia dos 	     ]
	mat_objs = [] # [ [ [obj 1], [ obj 2], [dist] ],[ [obj 1] , [obj 2] , [dist] ] ]
	for s, ins in enumerate(qap_instances):
		f = open(ins, "r")
		n = int(f.readline()) # nro localidades
		mat_objs.append([])
		for i in range(3):
			mat_objs[s].append([])
			for j in range(n):
				mat_objs[s][i].append([float(e) for e in f.readline().split()])
			f.readline()
		f.close()
	return mat_objs

if __name__ == "__main__":
    print(len(parse_qap()[0][-1]))
    print(len(parse_qap()))