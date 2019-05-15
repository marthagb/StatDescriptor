from permuta import Perm, PermSet, MeshPatt
from find_stats import *
from read_stats import *

def occs(perm, meshpatt):
	"""Return the number of occurrences of meshpatt in perm."""
	return len(list(meshpatt.occurrences_in(perm)))

def occsum(perm, meshpatts):
	"""Return sum of occurrences of mesh patterns in meshpatts in perm."""
	return sum([occs(perm,mp) for mp in meshpatts])

def smart_shade(perm, meshpatt, loccs=None):
	"""Return list of boxes that can be shaded to reduce the number
	   of occurrences of meshpatt in perm."""

	boxes = []
	if loccs == None:
		loccs = list(meshpatt.occurrences_in(perm))
	for candidate_indices in loccs:
		candidate = [perm[index] for index in candidate_indices]
		x = 0
		for element in perm:
			if element in candidate:
				x += 1
				continue
			y = sum(1 for candidate_element in candidate
					if candidate_element < element)
			if (x,y) not in boxes:
				boxes.append((x,y))
	return boxes

def smshcol(perm, meshpatt):
	"""Return list of columns that can be shaded to reduce the number
	   of occurrences of meshpatt in perm."""
	cols = []
	loccs = list(meshpatt.occurrences_in(perm))
	for candidate_indices in loccs:
		candidate = [perm[index] for index in candidate_indices]
		x = 0
		for element in perm:
			if element in candidate:
				x += 1
				continue
			if x not in cols:
				cols.append(x)
	return cols

def smshrow(perm, meshpatt, loccs=None):
	"""Return list of rows that can be shaded to reduce the number
	   of occurrences of meshpatt in perm."""

	rows = []
	if loccs == None:
		loccs = list(meshpatt.occurrences_in(perm))
	for candidate_indices in loccs:
		candidate = [perm[index] for index in candidate_indices]
		for element in perm:
			if element in candidate:
				continue
			y = sum(1 for candidate_element in candidate
					if candidate_element < element)
			if y not in rows:
				rows.append(y)
	return rows

def smshbiv(perm, meshpatt, loccs=None):
	"""Return list of columns and rows that can be shaded to reduce the
	   number of occurrences of meshpatt in perm."""

	cols,rows = [],[]
	if loccs == None:
		loccs = list(meshpatt.occurrences_in(perm))
	for candidate_indices in loccs:
		candidate = [perm[index] for index in candidate_indices]
		x = 0
		for element in perm:
			if element in candidate:
				x += 1
				continue
			y = sum(1 for candidate_element in candidate
					if candidate_element < element)
			if x not in cols:
				cols.append(x)
			if y not in rows:
				rows.append(y)
	crs = list(zip([0]*len(cols),cols)) + list(zip([1]*len(rows),rows))
	return crs

def smart_shade_list(perm, meshpatts):
	"""Return list of boxes that can be shaded to reduce the sum
	   of occurrences of mesh patterns in meshpatts in perm."""
	r = []
	for i in range(len(meshpatts)):
		s = smart_shade(perm, meshpatts[i])
		r.extend(zip([i]*len(s), s))
	return r

def smshcol_list(perm, meshpatts):
	"""Return list of columns that can be shaded to reduce the sum
	   of occurrences of mesh patterns in meshpatts in perm."""
	r = []
	for i in range(len(meshpatts)):
		s = smshcol(perm, meshpatts[i])
		r.extend(zip([i]*len(s), s))
	return r

def smshrow_list(perm, meshpatts):
	"""Return list of rows that can be shaded to reduce the sum
	   of occurrences of mesh patterns in meshpatts in perm."""
	r = []
	for i in range(len(meshpatts)):
		s = smshrow(perm, meshpatts[i])
		r.extend(zip([i]*len(s), s))
	return r

def smshbiv_list(perm, meshpatts):
	"""Return list of columns and rows that can be shaded to reduce
	   the sum of occurrences of mesh patterns in meshpatts in perm."""
	r = []
	for i in range(len(meshpatts)):
		s = smshbiv(perm, meshpatts[i])
		r.extend(zip([i]*len(s), s))
	return r

def pick_shade(green, red):
	"""Return a list of boxes to shade that includes at least one element
	   from each list in red, but no elements from green"""
	greens = set(green)
	reds = []
	red.sort(key=len)
	for r in red:
		s = set(r) - greens
		if all(not s.issuperset(re) for re in reds):
			reds.append(list(s))
	picked = [[]]
	for r in reds:
		picked_new = []
		for p in picked:
			picked_new.extend(pick(p,r))
		picked = picked_new
	return picked

def pick(pp, red):
	"""Pick an element from red to add to pp, if there is no shared element.
	   Return all possible choices."""
	for r in red:
		if r in pp:
			return [pp]
	return [pp+[r] for r in red]

def shade_list(meshpatts, boxes):
	"""Shade given boxes in meshpatts."""
	r = []
	for i in range(len(meshpatts)):
		r.append(meshpatts[i].shade([box for n,box in boxes if n == i]))
	return r

def shcol_list(meshpatts, cols):
	"""Shade given columns in meshpatts."""
	r = []
	for i in range(len(meshpatts)):
		r.append(meshpatts[i].shade([(col,y) for y in range(len(meshpatts[i])+1) for n,col in cols if n == i]))
	return r

def shrow_list(meshpatts, rows):
	"""Shade given rows in meshpatts."""
	r = []
	for i in range(len(meshpatts)):
		r.append(meshpatts[i].shade([(x,row) for x in range(len(meshpatts[i])+1) for n,row in rows if n == i]))
	return r

def shbiv_list(meshpatts, crs):
	"""Shade given columns and rows in meshpatts."""
	r = []
	for i in range(len(meshpatts)):
		shd = [cr for n,cr in crs if n == i]
		sh = []
		for j,cr in shd:
			if j == 0:
				sh.extend([(cr,y) for y in range(len(meshpatts[i])+1)])
			if j == 1:
				sh.extend([(x,cr) for x in range(len(meshpatts[i])+1)])
		r.append(meshpatts[i].shade(sh))
	return r

def stat_descriptor_single(stats):
	"""Return all single mesh patterns that describe stats."""

	#Find first non-zero stat to determine underlying permutation
	for perm, stat in stats:
		if stat > 0:
			p = perm
			break
	meshpatts = [MeshPatt(p)]

	while not all(all(occs(p, m) == s for p,s in stats) for m in meshpatts):
		new_meshpatts = []
		for mp in meshpatts:
			unusable = False
			green = []
			red = []
			for perm, stat in stats:
				loccs = list(mp.occurrences_in(perm))
				s = len(loccs)
				if s < stat:
					unusable = True
					break
				if s == stat:
					green.extend(smart_shade(perm, mp, loccs))
				if s > stat:
					red.append(smart_shade(perm, mp, loccs))
			if not unusable:
				ps = pick_shade(green, red)
				new_meshpatts.extend([mp.shade(boxes) for boxes in ps])
		meshpatts = set(new_meshpatts)

	return meshpatts

memo = {}
def stat_descriptor_multiple(stats, priors=[], maxpatts=2, maxlen=3):
	"""Find one or more lists of mesh patterns that describe stats, if possible.
	Args:
		stats:
			The statistic for which to find a description.
			List of tuples (p,s) where p is a permutation and s is an integer.
		priors:
			List of mesh patterns previously selected for the description.
		maxpatts:
			The maximum number of patterns allowed in a description.
		maxlen:
			The maximum length of patterns allowed in a description.

	Returns list of lists of mesh patterns that describe the given statistic.
	"""

	tsp = tuple(sorted(priors))
	if tsp in memo:
		return []
	if len(priors) > maxpatts:
		memo[tsp] = []
		return []
	if priors == []:
		for perm, stat in stats:
			if stat > 0:
				p = perm
				break
		if len(p) > maxlen:
			memo[tsp] = priors
			return []
		meshpatts = [[MeshPatt(p)]]
	else:
		meshpatts = [priors]
	if len(priors) == maxpatts and any(occsum(p,priors) < s for p,s in stats):
		memo[tsp] = []
		return []
	i = 0
	while i < 10 and not all(all(occsum(p,m) <= s for p,s in stats) for m in meshpatts):
		new_meshpatts = []
		for mp in meshpatts:
			green = []
			red = []
			for perm, stat in stats:
				st = occsum(perm, mp)
				if st > stat:
					red.append(smart_shade_list(perm, mp))
			ps = pick_shade(green, red)
			new_meshpatts.extend([shade_list(mp, boxes) for boxes in ps])

		meshpatts = new_meshpatts
		i += 1

	f = []
	for mp in meshpatts:
		new_stats = [(p,s-occsum(p,mp)) for p,s in stats]
		if all(s == 0 for _,s in new_stats):
			f.append(mp)
		elif all(s >= 0 for _,s in new_stats):
			for perm, stat in new_stats:
				if stat > 0:
					p = perm
					break
			if len(p) <= maxlen:
				f.extend(stat_descriptor_multiple(stats, mp+[MeshPatt(p)], maxpatts, maxlen))

	if len(f) == 0:
		memo[tsp] = []
		return []
	minlen = min([len(l) for l in f])
	ff = set([tuple(sorted(l)) for l in f if len(l) == minlen])
	memo[tsp] = ff
	return ff

memo_v = {}
def sdm_vincular(stats, priors=[], maxpatts=4, maxlen=3):
	"""Find one or more lists of mesh patterns (vincular patterns) that describe stats, if possible.
	Args:
		stats:
			The statistic for which to find a description.
			List of tuples (p,s) where p is a permutation and s is an integer.
		priors:
			List of mesh patterns previously selected for the description.
		maxpatts:
			The maximum number of patterns allowed in a description.
		maxlen:
			The maximum length of patterns allowed in a description.

	Returns list of lists of mesh patterns (vincular patterns) that describe the given statistic.
	"""

	tsp = tuple(sorted(priors))
	if tsp in memo_v:
		return []
	if len(priors) > maxpatts:
		memo_v[tsp] = []
		return []
	if priors == []:
		for perm, stat in stats:
			if stat > 0:
				p = perm
				break
		if len(p) > maxlen:
			memo_v[tsp] = priors
			return []
		meshpatts = [[MeshPatt(p)]]
	else:
		meshpatts = [priors]
	if len(priors) == maxpatts and any(occsum(p,priors) < s for p,s in stats):
		memo_v[tsp] = []
		return []
	i = 0
	while i < 10 and not all(all(occsum(p,m) <= s for p,s in stats) for m in meshpatts):
		new_meshpatts = []
		for mp in meshpatts:
			green = []
			red = []
			for perm, stat in stats:
				st = occsum(perm, mp)
				if st > stat:
					red.append(smshcol_list(perm, mp))
			ps = pick_shade(green, red)
			new_meshpatts.extend([shcol_list(mp, boxes) for boxes in ps])

		meshpatts = new_meshpatts
		i += 1

	f = []
	for mp in meshpatts:
		new_stats = [(p,s-occsum(p,mp)) for p,s in stats]
		if all(s == 0 for _,s in new_stats):
			f.append(mp)
		elif all(s >= 0 for _,s in new_stats):
			for perm, stat in new_stats:
				if stat > 0:
					p = perm
					break
			if len(p) <= maxlen:
				f.extend(sdm_vincular(stats, mp+[MeshPatt(p)], maxpatts, maxlen))

	if len(f) == 0:
		memo_v[tsp] = []
		return []
	minlen = min([len(l) for l in f])
	ff = set([tuple(sorted(l)) for l in f if len(l) == minlen])
	memo_v[tsp] = ff
	return ff

memo_c = {}
def sdm_covincular(stats, priors=[], maxpatts=4, maxlen=3):
	"""Find one or more lists of mesh patterns (covincular patterns) that describe stats, if possible.
	Args:
		stats:
			The statistic for which to find a description.
			List of tuples (p,s) where p is a permutation and s is an integer.
		priors:
			List of mesh patterns previously selected for the description.
		maxpatts:
			The maximum number of patterns allowed in a description.
		maxlen:
			The maximum length of patterns allowed in a description.

	Returns list of lists of mesh patterns (covincular patterns) that describe the given statistic.
	"""

	tsp = tuple(sorted(priors))
	if tsp in memo_c:
		return []
	if len(priors) > maxpatts:
		memo_c[tsp] = []
		return []
	if priors == []:
		for perm, stat in stats:
			if stat > 0:
				p = perm
				break
		if len(p) > maxlen:
			memo_c[tsp] = priors
			return []
		meshpatts = [[MeshPatt(p)]]
	else:
		meshpatts = [priors]
	if len(priors) == maxpatts and any(occsum(p,priors) < s for p,s in stats):
		memo_c[tsp] = []
		return []
	i = 0
	while i < 10 and not all(all(occsum(p,m) <= s for p,s in stats) for m in meshpatts):
		new_meshpatts = []
		for mp in meshpatts:
			green = []
			red = []
			for perm, stat in stats:
				st = occsum(perm, mp)
				if st > stat:
					red.append(smshrow_list(perm, mp))
			ps = pick_shade(green, red)
			new_meshpatts.extend([shrow_list(mp, boxes) for boxes in ps])

		meshpatts = new_meshpatts
		i += 1

	f = []
	for mp in meshpatts:
		new_stats = [(p,s-occsum(p,mp)) for p,s in stats]
		if all(s == 0 for _,s in new_stats):
			f.append(mp)
		elif all(s >= 0 for _,s in new_stats):
			for perm, stat in new_stats:
				if stat > 0:
					p = perm
					break
			if len(p) <= maxlen:
				f.extend(sdm_covincular(stats, mp+[MeshPatt(p)], maxpatts, maxlen))

	if len(f) == 0:
		memo_c[tsp] = []
		return []
	minlen = min([len(l) for l in f])
	ff = set([tuple(sorted(l)) for l in f if len(l) == minlen])
	memo_c[tsp] = ff
	return ff

memo_b = {}
def sdm_bivincular(stats, priors=[], maxpatts=4, maxlen=3):
	"""Find one or more lists of mesh patterns (bivincular patterns) that describe stats, if possible.
	Args:
		stats:
			The statistic for which to find a description.
			List of tuples (p,s) where p is a permutation and s is an integer.
		priors:
			List of mesh patterns previously selected for the description.
		maxpatts:
			The maximum number of patterns allowed in a description.
		maxlen:
			The maximum length of patterns allowed in a description.

	Returns list of lists of mesh patterns (bivincular patterns) that describe the given statistic.
	"""

	tsp = tuple(sorted(priors))
	if tsp in memo_b:
		return []
	if len(priors) > maxpatts:
		memo_b[tsp] = []
		return []
	if priors == []:
		for perm, stat in stats:
			if stat > 0:
				p = perm
				break
		if len(p) > maxlen:
			memo_b[tsp] = priors
			return []
		meshpatts = [[MeshPatt(p)]]
	else:
		meshpatts = [priors]
	if len(priors) == maxpatts and any(occsum(p,priors) < s for p,s in stats):
		memo_b[tsp] = []
		return []
	i = 0
	while i < 10 and not all(all(occsum(p,m) <= s for p,s in stats) for m in meshpatts):
		new_meshpatts = []
		for mp in meshpatts:
			green = []
			red = []
			for perm, stat in stats:
				st = occsum(perm, mp)
				if st > stat:
					red.append(smshbiv_list(perm,mp))
			ps = pick_shade(green, red)
			new_meshpatts.extend([shbiv_list(mp, boxes) for boxes in ps])

		meshpatts = new_meshpatts
		i += 1

	f = []
	for mp in meshpatts:
		new_stats = [(p,s-occsum(p,mp)) for p,s in stats]
		if all(s == 0 for _,s in new_stats):
			f.append(mp)
		elif all(s >= 0 for _,s in new_stats):
			for perm, stat in new_stats:
				if stat > 0:
					p = perm
					break
			if len(p) <= maxlen:
				f.extend(sdm_bivincular(stats, mp+[MeshPatt(p)], maxpatts, maxlen))

	if len(f) == 0:
		memo_b[tsp] = []
		return []
	minlen = min([len(l) for l in f])
	ff = set([tuple(sorted(l)) for l in f if len(l) == minlen])
	memo_b[tsp] = ff
	return ff


examples = {"2":("0002",4),"4":("0004",4),"7":("0007",4),"18":("0018",4),"21":("0021",4),"22":("0022",4),"23":("0023",4),"30":("0030",4),
	"35":("0035",4),"54":("0054",5),"55":("0055",4),"56":("0056",4),"92":("0092",4),"99":("0099",4),"119":("0119",4),"123":("0123",5),
	"154":("0154",4),"213":("0213",4),"214":("0214",4),"215":("0215",4),"217":("0217",4),"218":("0218",4),"219":("0219",4),"220":("0220",4),
	"221":("0221",3),"234":("0234",4),"245":("0245",4),"246":("0246",4),"304":("0304",4),"305":("0305",4),"308":("0308",4),"314":("0314",4),
	"316":("0316",4),"325":("0325",4),"341":("0341",4),"353":("0353",4),"354":("0354",4),"355":("0355",5),"356":("0356",5),"357":("0357",5),
	"358":("0358",5),"359":("0359",5),"360":("0360",5),"365":("0365",5),"366":("0366",5),"371":("0371",5),"372":("0372",5),"374":("0374",4),
	"423":("0423",4),"424":("0424",4),"425":("0425",4),"426":("0426",4),"427":("0427",4),"428":("0428",4),"429":("0429",4),"430":("0430",4),
	"431":("0431",4),"432":("0432",4),"433":("0433",4),"434":("0434",4),"435":("0435",4),"436":("0436",4),"437":("0437",4),"441":("0441",4),
	"446":("0446",4),"457":("0457",4),"470":("0470",4),"472":("0472",4),"483":("0483",4),"495":("0495",4),"534":("0534",5),"541":("0541",4),
	"542":("0542",3),"546":("0546",4),"619":("0619",5),"740":("0740",5),"756":("0756",4),"799":("0799",5),"834":("0834",4),"836":("0836",4),
	"1082":("1082",5),"1087":("1087",5),"1130":("1130",5)}


def stat_descriptor(n):
	"""Find one or more descriptions of stats, if possible.
	Args:
		n: Number of statistic from findstat.org

	Returns list of lists of mesh patterns that describe the given statistic.
	"""

	try:
		ex,l = examples[n]
	except:
		ex,l = "0"*(4-len(n))+n, 4
	print(n + ".\n")
	stats = read_stats_json("stats/St00"+ex+".json", l)

	sds = stat_descriptor_single(stats)
	if len(sds) > 0:
		return [[m] for m in sds]

	sdmv = sdm_vincular(stats)
	if len(sdmv) > 0:
		return sdmv

	sdmc = sdm_covincular(stats)
	if len(sdmc) > 0:
		return sdmc

	sd = stat_descriptor_multiple(stats)
	return sd

def print_results(meshpatts):
	for mps in meshpatts:
		print("------------------------------------------\n")
		for mp in mps:
			print(mp, "\n")
	print("------------------------------------------\n")

ex = sys.argv[1:]
for example in ex:
	meshps = stat_descriptor(example)
	print_results(meshps)
	memo, memo_v, memo_c, memo_b = {}, {}, {}, {}
