import sys

refFnm = str((sys.argv)[1])
indexL = 0
indexL_Init = 0
indexR = 0

for line in open(refFnm):
  l = line.split()
  if l[0] != "ATOM":
    continue

  newIndex = int(l[4])

  if (not indexL_Init) or newIndex < indexL:
    indexL_Init = 1
    indexL = newIndex

  if newIndex > indexR:
    indexR = newIndex

print str(indexL)+"   "+str(indexR)
