import sys

mydic = {}

fnm = str((sys.argv)[1])
mode = str((sys.argv)[2])
f = open("./TR2T0.log", 'r')
for line in f:
  index = line.split()

  if mode == "TR2T0":
    mydic[index[0]] = index[1]
  else:
    mydic[index[1]] = index[0]

f.close()

f = open(fnm, 'r')
fw = open(fnm+mode, 'w')
for line in f:
  words = line.split()
  fw.write('%3d   %3d   %d  %7.6f   %7.6f   %7.6f\n' % (int(mydic[words[0]]), int(mydic[words[1]]), int(words[2]), float(words[3]), float(words[4]), float(words[5])))

f.close()
fw.close()
