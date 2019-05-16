from permuta import Perm, PermSet, MeshPatt


def find_stats(meshpatt, n):
	"""Find the number of occurrences of meshpatt in all permutations of length up to n.
	
	Returns a list of tuples (p,s) where p is a permutation and s is the number of 
	occurrences of meshpatt in p.
	"""
	all_perms = []
	for i in range(n+1):
		all_perms += list(PermSet(i))

	stats = []
	for p in all_perms:
		stats.append((p, len(list(meshpatt.occurrences_in(p)))))
	return stats