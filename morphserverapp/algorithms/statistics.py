from .basic_operations import *


def min_residue_distance(struct):
    prev = None
    min_dist = -1
    for res in struct:
        if prev is None:
            prev = res
        else:
            tmp = dist(res, prev)
            if min_dist == -1:
                min_dist = tmp
            min_dist = min(tmp, min_dist)
            prev = res
    return min_dist

def max_residue_distance(struct):
    prev = None
    max_dist = -1
    for res in struct:
        if prev is None:
            prev = res
        else:
            tmp = dist(res, prev)
            max_dist = max(tmp, max_dist)
            prev = res
    return max_dist

def rmsd(s, f):
    return rms(minus_lines(s, f))

def analyze(struct1, struct2):
    stats = {}
    if len(struct1) == len(struct2):
        stats["rmsd"] = rmsd(struct1, struct2)
    else:
        stats["rmsd"] = "Since the proteins have different number of residues, the alignment was not performed"
    stats["first protein"] = analyze_struct(struct1)
    stats["second protein"] = analyze_struct(struct2)
    return stats

def __analyze_struct(struct):
      st = {}
      st['minimum distance between consecutive residues'] = min_residue_distance(struct)
      st['maximum distance between consecutive residues'] = max_residue_distance(struct)
      st['number of residues'] = len(struct)
      return st
