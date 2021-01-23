import collections
import json

def flattenDict(data, sep="."):
	obj = collections.OrderedDict()

	def recurse(t,parent_key=""):
		if isinstance(t,list):
			for i in range(len(t)):
				recurse(t[i],parent_key + sep + str(i) if parent_key else str(i))
		elif isinstance(t,dict):
			for k,v in t.items():
				recurse(v,parent_key + sep + k if parent_key else k)
		else:
			obj[parent_key] = t

	recurse(data)
	print(obj)
	return obj


with open("./data/sample/root[27]-sub-page[1].json", "r") as read_file:
    data = json.load(read_file)

flattenDict(data)