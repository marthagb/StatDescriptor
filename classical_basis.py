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

p = PermSet([Perm(),Perm((0)),Perm((0,1)),Perm((0,1,2)),Perm((0,1,2,3))])
print(find_classical_basis(p))

p = PermSet([Perm(),Perm((0)),Perm((0,1)),Perm((1,0)),Perm((0,1,2)),Perm((1,0,2)),Perm((2,0,1)),Perm((2,1,0)),Perm((0,1,2,3)),
	Perm((1,0,2,3)),Perm((2,0,1,3)),Perm((2,1,0,3)),Perm((3,0,1,2)),Perm((3,1,0,2)),Perm((3,2,0,1)),Perm((3,2,1,0))])
print(find_classical_basis(p))

p = PermSet([Perm(),Perm((0)),Perm((0,1)),Perm((1,0)),
	Perm((0,1,2)),Perm((0,2,1)),Perm((1,0,2)),Perm((1,2,0)),Perm((2,0,1)),Perm((2,1,0)),
	Perm((0,1,2,3)),Perm((0,1,3,2)),Perm((0,2,1,3)),Perm((0,2,3,1)),Perm((0,3,1,2)),Perm((0,3,2,1)),
	Perm((1,0,2,3)),Perm((1,0,3,2)),Perm((1,2,0,3)),Perm((1,2,3,0)),Perm((1,3,0,2)),Perm((1,3,2,0)),
	Perm((2,0,1,3)),Perm((2,0,3,1)),Perm((2,1,0,3)),Perm((2,1,3,0)),Perm((2,3,0,1)),Perm((2,3,1,0)),
	Perm((3,0,1,2)),Perm((3,0,2,1)),Perm((3,1,0,2)),Perm((3,1,2,0)),Perm((3,2,0,1)),Perm((3,2,1,0))])
print(find_classical_basis(p))
