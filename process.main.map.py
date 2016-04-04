import sys

SBMfile = str((sys.argv)[1])
sampleFile = str((sys.argv)[2])
optFile = "TR2T0.log"

SBMfp = open(SBMfile, "r")
optfp = open(optFile, "w")

for line in open(sampleFile):
  if line == "TER\n":
    break
  line_SBM = SBMfp.readline()

  l = line.split()
  l_SBM = line_SBM.split()

  optfp.write('%6s   %6s\n' % (l_SBM[1], l[1]))

optfp.close()

line_SBM = SBMfp.readline()
print line_SBM.split()[1]
