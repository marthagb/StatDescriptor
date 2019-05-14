import pytest

from permuta import Perm, PermSet
from permuta.permutils.classical_basis import *

def test_classical_basis():
	p1 = PermSet([Perm(()),Perm((0)),Perm((0,1)),Perm((1,0)),Perm((0,1,2)),Perm((0,2,1)),
		Perm((1,0,2)),Perm((2,0,1)),Perm((2,1,0)),Perm((0,1,2,3)),Perm((0,1,3,2)),
		Perm((0,2,1,3)),Perm((0,3,1,2)),Perm((0,3,2,1)),Perm((1,0,2,3)),
		Perm((1,0,3,2)),Perm((2,0,1,3)),Perm((2,1,0,3)),Perm((3,0,1,2)),
		Perm((3,0,2,1)),Perm((3,1,0,2)),Perm((3,2,1,0))])
	b1 = find_classical_basis(p1)
	assert b1 == [Perm((1,2,0)), Perm((3,2,0,1))]
	p2 = PermSet([])
	b2 = find_classical_basis(p2)
	assert b2 == [Perm(())]
	p3 = PermSet([Perm(())])
	b3 = find_classical_basis(p3)
	assert b3 == []
	p4 = PermSet([Perm(()),Perm((0))])
	b4 = find_classical_basis(p4)
	assert b4 == []
	p5 = PermSet([Perm(()),Perm((0)),Perm((0,1)),Perm((0,1,2,)),Perm((0,1,2,3))])
	b5 = find_classical_basis(p5)
	assert b5 == [Perm((1,0))]