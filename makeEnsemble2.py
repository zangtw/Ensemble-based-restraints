from Bio import PDB
from Bio.PDB.PDBParser import PDBParser
import re
import sys

parser = PDB.PDBParser()

pdbfnm = str((sys.argv)[1])
indexL = int((sys.argv)[2])
indexH = int((sys.argv)[3])
pdbList = re.split('TS', pdbfnm)
pdbID = pdbList[1]

myFileIndex = int((sys.argv)[4])
totFileNum = int((sys.argv)[5])
percent = str(float(myFileIndex) / float(totFileNum) * 100)[:4]

structure = parser.get_structure(pdbID, pdbfnm)
for model in structure:
  for chain in model:
    for residue in list(chain):
      id = residue.get_id()
      if id[1] < indexL or id[1] > indexH:
        chain.detach_child(id)
      else:
        for atom in list(residue):
          id = atom.get_id()
          if id != 'N' and id != 'C' and id != 'O' and id != 'CA':
            residue.detach_child(id)

    if len(chain) > indexH - indexL:
      io = PDB.PDBIO()
      io.set_structure(structure)
      io.save(pdbID + ".pdb")
      sys.stdout.write("\r" + percent +"%:   Finishing " + pdbID)
    else:
      sys.stdout.write("\r" + percent +"%:   Skipping " + pdbID)
