import sys
import random
import numpy as np
from scipy.optimize import minimize

class minimizer(object):
  def __init__(self, data, peakIndex, width):
    self.data = np.array(data)
    self.peakIndex = np.array(peakIndex)
    self.peakNumber = self.peakIndex.size
    self.width = np.array(width)
    np.seterr(all='ignore')

  def start(self):
    def func(x):
      f = 0
      for i in range(0, self.peakNumber):
        f += x[i] * np.exp(-1 * (self.data[0,:] - self.data[0][self.peakIndex[i]])**2 / x[i + self.peakNumber])
      f -= self.data[1,:]
      f = np.sum(f**2)
      return f / self.data[0].size

    bnds = np.zeros((2 * self.peakNumber, 2))
    for i in range(0, self.peakNumber):
      bnds[i][0] = 1.5 * self.data[1][self.peakIndex[i]]
      bnds[i][1] = 0.5 * self.data[1][self.peakIndex[i]]
      bnds[i + self.peakNumber][0] = 0
      bnds[i + self.peakNumber][1] = self.width[i]

    oldres = 0
    newres = 0
    sys.stdout.write("\r" + "0.0%")
    sys.stdout.flush()
    for j in range(1, 201):
      if j % 5 == 0:
        sys.stdout.write("\r" + str(0.5 * j)+"%")
        sys.stdout.flush()
      startPoint = np.zeros(2 * self.peakNumber)
      rand = random.random()
      for i in range(0, startPoint.size):
        startPoint[i] = bnds[i][0] * rand + bnds[i][1] * (1.0 - rand)

      oldres = newres
      newres = minimize(func, startPoint,                                      \
                        bounds=bnds, method='SLSQP',                           \
                        options={'disp': False, 'maxiter': 1000})            
      
      if oldres == 0 or newres.fun < oldres.fun:
        res = newres

    sys.stdout.write("\n")
    sys.stdout.flush()
    return {'sol': res.x, 'res': np.sqrt((res.fun))}
