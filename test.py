import os.path
import numpy as np
import matplotlib.pyplot as plt
import scipy

import refnx
from refnx.dataset import ReflectDataset, Data1D
from refnx.analysis import Transform, CurveFitter, Objective, Model, Parameter
from refnx.reflect import SLD, Slab, ReflectModel


DATASET_NAME = 'rawdataDay2.dat'
#file_path = os.path.join(pth, 'analysis', 'test', DATASET_NAME)


data = ReflectDataset(DATASET_NAME)
'''
fronting = SLD(name="fronting",rho=1.3196e-11)
poly = SLD(name = "poly", rho = 1.35354)
poly2 = SLD(name = " poly2", rho = 2.95368)
SiOx = SLD(name = "SoOx", rho = 3.48249)
backing = SLD (name = " backing" , rho = 2.07)

sample =(
fronting(0, 0)
    | poly(79.4147, 53.9112)
    | poly2(327.551, 24.9953)
    | SiOx(24.1576, 6.01569)
    | backing(0, 3)
)

# === Fit parameters ===
fronting.rho.range(1e-11, 1e-10)
sample[1].thickness.range(1, 100)
sample[1].interface.range(1, 110)
poly.rho.range(1, 1.5)
sample[2].thickness.range(1, 50)
sample[2].interface.range(1, 100)
poly2.rho.range(1, 3.16)
sample[3].thickness.range(15, 30)
sample[3].interface.range(6.01,6.036)
SiOx.rho.range(3.48, 5.5)
'''

#fronting = SLD(1.3196e-11, name="fronting") 
poly = SLD(1.35354, name = "poly")
poly2 = SLD(2.95368, name = "poly2")
SiOx = SLD(3.48249, name = "SiOx")
film = SLD(2.0, name='film')
film2 = SLD(2.0, name='film')
#backing = SLD(2.07, name = "backing")


poly_layer = poly(79.4147, 53.9112)
poly2_layer = poly2(327.551, 53.9112)
film_layer = film(250, 3)
film2_layer = film(100, 3)
siox_layer = SiOx(24.1576, 6.01569)

poly_layer.thick.setp(bounds=(50,100), vary=True)
poly_layer.rough.setp(bounds=(20,70), vary=True)

poly2_layer.thick.setp(bounds=(300,400), vary=True)
poly2_layer.rough.setp(bounds=(20,70), vary=True)

film_layer.thick.setp(bounds=(200, 300), vary=True)
film_layer.sld.real.setp(bounds=(0.1, 3), vary=True)
film_layer.rough.setp(bounds=(1, 15), vary=True)

film2_layer.thick.setp(bounds=(50, 150), vary=True)
film2_layer.sld.real.setp(bounds=(0.1, 3), vary=True)
film2_layer.rough.setp(bounds=(1, 15), vary=True)

siox_layer.thick.setp(bounds=(10,50), vary=True)
siox_layer.rough.setp(bounds=(1,10), vary=True)
structure = poly | poly2 | film_layer | film2_layer | SiOx


model = ReflectModel(structure, bkg=3e-6, dq=5.0)
model.scale.setp(bounds=(0.6, 1.2), vary=True)
model.bkg.setp(bounds=(1e-9, 9e-6), vary=True)

q = np.linspace(0.005, 0.3, 1001)
plt.xlabel('Q')
plt.ylabel('Reflectivity')
plt.yscale('log')
plt.plot(q, model(q))
#plt.show()


objective = Objective(model, data, transform=Transform('logY'))
fitter = CurveFitter(objective)
fitter.fit('differential_evolution');
objective.plot()
plt.legend()
plt.xlabel('Q')
plt.ylabel('logR')
plt.legend()
plt.show()
