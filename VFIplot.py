import numpy as np
import matplotlib.pyplot as plt
data=np.load('resfile.npz')
capval=data['capval']
labval=data['labval']
hpol=data['hpol']
kpol=data['kpol']
v=data['v']

# f, axarr=plt.subplots(2,sharex=True)
# axarr[0]=plot(capval, kpol)
# axarr[1]=plot(capval,V)
# 
# plt.show()

# Simple data to display in various forms
# x = np.linspace(0, 2 * np.pi, 400)
# y = np.sin(x ** 2)

print v.shape

plt.subplot(3,1,1)
plt.plot(capval, kpol[:,0],capval, kpol[:,1],capval, kpol[:,2])
plt.title('Policy function for capital')

plt.subplot(3,1,3)
plt.plot(capval, v[:,0],capval, v[:,1],capval, v[:,2])
plt.title('Value function')

plt.subplot(3,1,2)
plt.plot(labval, hpol[:,0],labval, hpol[:,1],labval, hpol[:,2])
plt.title('Policy function for labour')

plt.show()
