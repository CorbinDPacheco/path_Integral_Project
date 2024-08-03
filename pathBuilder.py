import pickle
from project import Particle

particle = Particle(5, [0,400])

file = open("./paths.pckl","wb")
out = []
numOfPaths = 500
for i in range(numOfPaths):
    out.append(particle.createPath_verticalGauss(100,800,400,0.00001))
for i in range(numOfPaths):
    out.append(particle.createPath_verticalGauss(100,800,400,.005))
for i in range(numOfPaths):
    out.append(particle.createPath_verticalGauss(100,800,400,1))

pickle.dump(out,file)
file.close()

