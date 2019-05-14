from permuta import Perm, PermSet, MeshPatt


def find_stats(meshpatt, n):
	all_perms = []
	for i in range(n+1):
		all_perms += list(PermSet(i))

	stats = []
	for p in all_perms:
		stats.append((p, len(list(meshpatt.occurrences_in(p)))))
	return stats