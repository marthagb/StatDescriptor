from permuta import Perm
import json
import sys

def read_stats_json(file, n):
	f = open(file, 'r')
	data = json.load(f)
	f.close()

	stats = []
	try:
		for perm, value in data['Data'].items():
		    perm = Perm.to_standard(eval(perm))
		    if len(perm) <= n:
		    	stats.append((perm, value))
	except KeyError:
		for perm, value in data['StatisticData'].items():
		    perm = Perm.to_standard(eval(perm))
		    if len(perm) <= n:
		    	stats.append((perm, value))
	stats.sort()

	return stats