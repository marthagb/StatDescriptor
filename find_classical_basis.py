from classical_basis import *

av21 = PermSet([Perm(),Perm((0,)),Perm((0,1)),Perm((0,1,2)),Perm((0,1,2,3))])
print(find_classical_basis(av21))

av132_231 = PermSet([Perm(),Perm((0,)),Perm((0,1)),Perm((1,0)),Perm((0,1,2)),Perm((1,0,2)),Perm((2,0,1)),Perm((2,1,0)),Perm((0,1,2,3)),
	Perm((1,0,2,3)),Perm((2,0,1,3)),Perm((2,1,0,3)),Perm((3,0,1,2)),Perm((3,1,0,2)),Perm((3,2,0,1)),Perm((3,2,1,0))])
print(find_classical_basis(av132_231))

all_perms = PermSet([Perm(),Perm((0,)),Perm((0,1)),Perm((1,0)),
	Perm((0,1,2)),Perm((0,2,1)),Perm((1,0,2)),Perm((1,2,0)),Perm((2,0,1)),Perm((2,1,0)),
	Perm((0,1,2,3)),Perm((0,1,3,2)),Perm((0,2,1,3)),Perm((0,2,3,1)),Perm((0,3,1,2)),Perm((0,3,2,1)),
	Perm((1,0,2,3)),Perm((1,0,3,2)),Perm((1,2,0,3)),Perm((1,2,3,0)),Perm((1,3,0,2)),Perm((1,3,2,0)),
	Perm((2,0,1,3)),Perm((2,0,3,1)),Perm((2,1,0,3)),Perm((2,1,3,0)),Perm((2,3,0,1)),Perm((2,3,1,0)),
	Perm((3,0,1,2)),Perm((3,0,2,1)),Perm((3,1,0,2)),Perm((3,1,2,0)),Perm((3,2,0,1)),Perm((3,2,1,0))])
print(find_classical_basis(all_perms))
