from hashlib import md5
from Bio import PDB as pdb

directory = '../public/data/'

  # saves pdb to a file with a name equal to its md5 hash
  # returns this hash as a result
def save_to_file(text):
    hasher = md5()
    hasher.update(text.encode())
    name = hasher.hexdigest()
    path = directory + name + '.pdb'
    try:
        with open(path, mode='r') as f:
            pass
            #file already exists
    except IOError:
        f = open(path, mode='w')
        f.write(text)
        f.flush()
        f.close()
    return name

#useless
def load_from_file(file_name):
    path = directory + file_name
    if path[-4:] != '.pdb':
        path += '.pdb'
    f = open(path, mode='r')
    return f.read()

def __to_broken_line_struct(struct):
    ans = []
    for residue in struct.get_chains():
        for atom in residue.get_atoms():
            if atom.name == 'CA':
                coords = atom.get_coord()
                ans.append((coords[0], coords[1], coords[2]))
    return ans

def to_broken_line(text):
    struct = pdb.Structure(text)

    return __to_broken_line_struct(struct)

if __name__ == '__main__':
    parser = pdb.PDBParser()
    structure = parser.get_structure('test_id', 'ala_phe_ala.pdb')
    print(__to_broken_line_struct(structure))
