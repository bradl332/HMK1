import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(3, 100000, 3, 75, True)
# Setup the parameters these are all taken from the literature
beta=0.95
psi=1.88
delta=0.05
gamman=0.02
gammaz=0.03
theta=0.3

parameters=[beta, psi, delta, gamman, gammaz, theta]

# Create a linspace for all the possible values of capital and labour
nk=50
nl=50
nz=3
capval=np.linspace(0.05,2,nk)
capprimeval=np.linspace(0.05,2,nk)
labval=np.linspace(0,1,nl)
zval=np.linspace(0.5,1.5,nz)

#Create a final paramter rho to give probability of next state each period to begin with will gie all of them the same. For more advanced stuff can use Tauchen method
rho=1.0/nz
#Need to create a grid of all the possible values of consumption

c=np.zeros((nk,nl,nk,nz))
for i in range(nk):
    for l in range(nl):
        for q in range(nk):
            for y in range(nz):
                c[i,l,q,y]=((capval[q]**theta)*(zval[y]*labval[l])**(1-theta))-((1+gamman)*(1+gammaz))*capprimeval[i]+capval[q]*(1-delta)

# Now calculate all possible values of utility

uti=np.zeros((nk,nl,nk,nz))
for i in range(nk):
    for l in range(nl):
        for q in range(nk):
            for y in range(nz):
                if c[i,l,q,y]>0 and labval[l]<1:
                    uti[i,l,q,y]=np.log(c[i,l,q,y])+psi*np.log(1-labval[l])
                else:
                    uti[i,l,q,y]=-10000


# First need to create an intitial v so that can perform a first iteration of the value function
v=np.zeros((nk,nz))
for q in range(nk):
    for y in range(nz):
        v[q,y]=np.amax(np.amax(uti[:,:,q,y]))


# This new v matrix is nk by nz so its saying for each state z given what level of capital i picked last period this is what the utility will be next period

#These next lines set up the while loop for the VFI
dist=np.ones((nk,nz))
tol=0.00001

V=np.zeros((nk,nl,nk,nz))
vp=np.zeros((nk,nz))
kpol=np.zeros((nk,nz))
hpol=np.zeros((nk,nz))
iter=0

while np.all(np.absolute(dist))>tol:
	for y in range(nz):
		for q in range(nk):
			V[:,:,q,y]=uti[:,:,q,y]+beta*(1+gamman)*(rho*(v[:,0].reshape((nk,1)))*(np.ones((1,nl)))+rho*(v[:,1].reshape((nk,1)))*(np.ones((1,nl)))+rho*(v[:,2].reshape((nk,1)))*(np.ones((1,nl))))
			# The reshape part has to be there otherwise python just makes it into a list, now we have all the possible values of the value function need to find which values of capital prime maximise it
			indk=np.argmax(V[:,:,q,y],0)
			vk=np.amax(V[:,:,q,y],0)
			# indk gives the where the capital is located and vk gives the actual value of k dependent on kprime
			# Have now restricted the set of possible values to a specific k prime now need to see which value of labour maximises that
			indh=np.argmax(vk)
			vh=np.amax(vk)
			vp[q,y]=vh
			kpol[q,y]=capprimeval[indk[indh]]
			hpol[q,y]=labval[indh]
	dist=vp-v
	v=np.copy(vp)
	iter+=1
# Unlike Matlab have to use np.copy rather than v=vp otherwise the code only goes for two iterations as to why I have no idea I'm guessing its some strange oddity of python
print iter

np.savez('resfile.npz',capval=capval, labval=labval,kpol=kpol,hpol=hpol,v=v)

