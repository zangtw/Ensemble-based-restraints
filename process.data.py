import sys
import copy
import Queue

def do(filenm):
  with open(filenm) as f:
    nat = float(f.readline().split()[1])
    mdl = float(f.readline().split()[1])

    # pre-process
    for line in f:
      if line[0] != '#':
        break
    
    # values to be determined
    peakIndexList = []
    bottomIndexList = []
    natIndex = -1
    mdlIndex = -1
    xList = []
    yList = []
    
    # initialize
    initialized = False
    temp = line.split()
    count = int(temp[4][:-2])
    currIndex = 0
    xList.append(0.5 * (float(temp[0]) + float(temp[2])))
    yList.append(count)

    # do iteration
    for line in f:
      currIndex = currIndex + 1

      temp = line.split()
      
      countOld = count
      count = int(temp[4][:-2])
      
      xList.append(0.5 * (float(temp[0]) + float(temp[2])))
      yList.append(count)
      
      if natIndex == -1:
        if float(temp[2]) > nat:
          natIndex = currIndex

      if mdlIndex == -1:
        if float(temp[2]) > mdl:
          mdlIndex = currIndex

      if not initialized:
        climbing = (count > countOld)
        if not climbing: 
          peakIndexList.append(currIndex - 1)
        initialized = True
        continue

      if count == countOld:
        continue
      if climbing ^ (count < countOld):
        continue

      if climbing:
        peakIndexList.append(currIndex - 1)
      else:
        bottomIndexList.append(currIndex - 1)

      climbing = not climbing

    return {'natIndex': natIndex, 'mdlIndex': mdlIndex, \
             'peaks': peakIndexList, 'bottoms': bottomIndexList, \
             'x': xList, 'y': yList, 'nat': nat, 'mdl': mdl}

res = do(sys.argv[1])

# Now, answer the first question: 
# How many peaks are between nat the mdl?
bottoms = res['bottoms']
peaks = res['peaks']
peakStatus = [0] * len(peaks)
for i in range(0, len(peaks)):
  if peaks[i] > 0:
    if res['y'][peaks[i]] - res['y'][bottoms[i - 1]] != 1:
      continue
  
  if peaks[i] < len(res['y']) and peaks[i] < len(bottoms):
    if res['y'][peaks[i]] - res['y'][bottoms[i]] == 1:
      peakStatus[i] = 1

sign = 1 if res['natIndex'] > res['mdlIndex'] else -1
minIndex = res['mdlIndex'] if sign == 1 else res['natIndex']
maxIndex = res['natIndex'] if sign == 1 else res['mdlIndex']
peakCount = 0
for i in range(0, len(peaks)):
  if peaks[i] > maxIndex:
    break
  if peakStatus[i] == 1:
    continue
  if peaks[i] > minIndex:
    peakCount = peakCount + sign

with open("Info", "a") as myfile:
  myfile.write('%-6s  %d' % (sys.argv[1][3:], peakCount))
  myfile.write('\n')
  
# The second question is:
# How to generate a list of peaks around mdl?
peakList = []
nLeftPeaks = 0
nRightPeaks = 0
q = Queue.Queue()
for i in range(0 , len(peaks)):
  if peakStatus[i] == 1:
    continue
  
  if peaks[i] > res['mdlIndex']:
    if nRightPeaks == 3:
      break
    nRightPeaks = nRightPeaks + 1
  elif peaks[i] < res['mdlIndex']:
    if nLeftPeaks == 3:
      q.get()
    nLeftPeaks = nLeftPeaks + 1
    
  q.put(i)
    
while not q.empty():
  peakList.append(q.get())

# Last, estimate the width of each peak?
widthList = []
for i in range(0, len(peakList)):
  if peakList[i] > 0:
    widthLeft = peaks[peakList[i]] - bottoms[peakList[i] - 1] 
  else:
    widthLeft = -1

  if peakList[i] < len(bottoms):
    widthRight = bottoms[peakList[i]] - peaks[peakList[i]]
  else:
    widthRight = -1

  widthList.append(max(widthLeft, widthRight))

print "# NAT"
print res['nat']
print "# MDL"
print res['mdl']
print "# PEAK"
for i in peakList:
  print peaks[i]
print "# WIDTH"
for i in widthList:
  if i == 1:
    print 2
  else:
    print i
print "# DATA"
for i in range(0, len(res['x'])):
  if peakList[-1] < len(bottoms) and i > bottoms[peakList[-1]]:
    break
  print "%7.5f    %d" % (res['x'][i], res['y'][i])
