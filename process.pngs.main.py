import sys
import numpy as np
import matplotlib.pyplot as plt
import imp

load_module = imp.load_source('load_module', 'process.pngs.minimizer.py')
minimizer = load_module.minimizer

f = open(sys.argv[1], 'r')

dataInfo = {'NAT': 0, 'MDL': 0, 'PEAK': [], 'WIDTH': [], 'DATA': [[],[]]}
for line in f:
  if line[0] == '#':
    key = line.split()[1]
    continue

  if key == 'PEAK' or key == 'WIDTH':
    dataInfo[key].append(int(line))
  elif key == 'DATA':
    xy = line.split()
    dataInfo[key][0].append(float(xy[0]))
    dataInfo[key][1].append(float(xy[1]) * -1)
  else:
    dataInfo[key] = float(line)

peakIndex = dataInfo['PEAK']
peakNumber = len(peakIndex)
data = dataInfo['DATA']

binSize = data[0][1] - data[0][0]
width = map(lambda x: (x * binSize / 2)**2 * 2, dataInfo['WIDTH'])
  
mini = minimizer(data, peakIndex, width)
res = 0
for i in range(0, 10):
  newres = mini.start()
  if res == 0 or newres['res'] < res['res'] :
    res = newres
  if res['res'] <= 2.5:
    break
if res['res'] >= 3:
  print "WARNING: NOT GOOD FITTING"
print "MINIMIZE RESULT: "+str(res['res'])

# gen fit curve
x = np.arange(min(data[0]), max(data[0]), (max(data[0]) - min(data[0]))/200) 
y = 0
resultFile = open("Result", "a")
for i in range(0, peakNumber):
    y += res['sol'][i] * np.exp(- (x - data[0][peakIndex[i]])**2 / res['sol'][i + peakNumber])
    resultFile.write('%-6s   %7.6f   %7.6f   %7.6f\n' % (sys.argv[1][3:], data[0][peakIndex[i]], np.sqrt(0.5 * res['sol'][i + peakNumber]), -res['sol'][i]))
plt.plot(x,y)
resultFile.close()

# gen original data
plt.scatter(data[0], data[1], s=50, c='b', marker='o')

# gen model data
halfBinSize = binSize / 2
xMin = data[0][0] - halfBinSize
xMax = data[0][-1] + halfBinSize
if dataInfo['MDL'] >= xMin and dataInfo['MDL'] <= xMax:
  plt.axvline(x=dataInfo['MDL'], color='r')
      
# gen native data
if dataInfo['NAT'] >= xMin and dataInfo['MDL'] <= xMax:
  plt.axvline(x=dataInfo['NAT'], color='k')

xlength = max(data[0]) - min(data[0])
plt.xlim(min(data[0]) - xlength / 50, max(data[0]) + xlength / 50)
plt.ylim(min(min(data[1]), min(y)) - 1 , 1)
plt.savefig(sys.argv[1][3:], ext='png', close=True, verbose=False)
