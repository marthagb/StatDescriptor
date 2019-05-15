from permuta import Perm, PermSet

def find_classical_basis(permset):
	"""Find the classical basis of permset.
	Args:
		permset:
			The set of permutations whose classical basis is to be found.
	Returns list of permutations that the set avoids, if possible.
	"""
	try:
		# Find maximum length in the given set
		L = max([len(perm) for perm in permset])
	except ValueError:
		L = 0
	# Build list of all candidates for basis
	all_perms = []
	for i in range(L+1):
		all_perms += list(PermSet(i))
	basis = []
	for p in all_perms:
		if p not in permset:
			if not any(p.contains(a) for a in basis):
				basis.append(p)
		elif not p.avoids_set(basis):
			return []
	return basis
