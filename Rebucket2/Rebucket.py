import json
import numpy as np
import math
import heapq


class pair():
	p1 = None
	p2 = None
	similar = False
	sim = 0

	def __init__(self, p1, p2):
		self.p1 = p1
		self.p2 = p2

	def change(self, t):
		self.similar = t

	def set_sim(self, s):
		self.sim = s


############function to get buckets with training pairs############
def get_buckets_pair(D):
	all_bucket = {}
	for i in D:
		if i.similar:
			if i.p1 in all_bucket:
				all_bucket[i.p1].add(i.p2)
			else:
				all_bucket[i.p1] = {i.p2}
	return all_bucket

############function to get f-measures############
def get_F_measure(L,C,train_size):

	f_measure = 0
	###find the maxj{F(Li,Cj)}
	for key,i in L:
		maxj = get_f(i,C[key])
		f_measure+=len(i)/train_size*maxj
	return f_measure
def get_f(l,c):
	precision = len(l&c)/len(c)
	recall = len(l&c)/len(l)
	return 2*precision*recall/(precision+recall)


############function to Train the parameters############
# D --> pair() (a,b) a -> duplicated_stack b -> stack_id in bucket
# C --> selected buckets
# 选择出一些buckets，并用(key,random(items)）的格式来制作pair
def Trainning(alltraces,allbuckets, c0, o0, d0, s1, s2, s3, dm, om, cm):
	train_size = 1000
	D = []
	C = {}
	###Generate pairs
	for key,i in allbuckets.items():
		if len(i)>1:
			for t in i :
				D.append(pair(key,t))
			C[key] = i
			if len(D)>train_size:
				break
	c = c0
	max_heap = []
	while (c < cm):
		o = o0
		while (o < om):
			for i in D:
				sim = calculate_sim(alltraces[i.p1], alltraces[i.p2])
				i.set_sim(sim)
			d = d0
			while (d <= dm):
				for i in D:
					if i.sim > 1 - d:
						i.change(True)
				L = get_buckets_pair(D) ### get the buckets information according to the pairs
				f = get_F_measure(L, C,train_size) ### get F measurement
				heapq.heappush(max_heap, (1 - f, o, (c, d)))
				d = d + s1
			o += s2
		c += s3
	ff, oo, (cc, dd) = heapq.heappop(max_heap)
	return oo, cc, dd


############function to read the file############
def read_json_file(filepath):
	alltrace = {}
	with open(filepath, 'r') as eclipse:
		all_trace = json.load(eclipse)
	for i in all_trace:
		alltrace[i['stack_id']] = i
	return alltrace


############function to calculate the similarity############
def calculate_sim(trace1, trace2, c, o):
	M = np.zeros(len(trace1) + 1, len(trace2) + 1).tolist()
	for i in range(1, len(trace1) + 1):
		for j in range(1, len(trace2) + 1):
			cost = 0
			if trace1[i - 1] == trace2[j - 1]:
				cost = math.pow(math.e, -c * min(i, j) - o * abs(i - j))
			M[i][j] = max(M[i - 1][j - 1] + cost, M[i - 1][j], M[i][j - 1])
	divider = sum(math.pow(math.e, -c * j) for j in range(min(len(trace1), len(trace2)) + 1))
	return M[len(trace1)][len(trace2)] / divider


############function to get clusters############
def cluster(d, alltrace):
	clusters = [[i] for i in range(alltrace)]
	while (True):
		min_length = math.inf
		choosed = (0, 0)
		for i in range(len(clusters)):
			for j in range(i + 1, len(clusters)):
				cluster1 = clusters[i]
				cluster2 = clusters[j]
				real_length = 0
				for i1 in cluster1:
					for i2 in cluster2:
						length = 1 - calculate_sim(clusters[i1], clusters[i2])
						if length > real_length:
							real_length = length
				if real_length < min_length:
					choosed = (i, j)
		if min_length > d:
			break
		i1, i2 = choosed
		q = clusters[i1] + clusters[i2]
		clusters.pop(i1)
		clusters.pop(i2 - 1)
		clusters.append(q)


############function to get the buckets information############
def get_buckets(alltrace):
	allbuckets = {}
	for key,i in alltrace.items():
		if i['duplicated_stack'] == '':
			allbuckets[i['stack_id']] = {i} ###use set to store the bucket information
		else:
			if i['duplicated_stack'] in allbuckets:
				allbuckets[i['duplicated_stack']].add(i['stack_id'])
			else:
				allbuckets[i['duplicated_stack']] = {i['stack_id']}
	return allbuckets



def main():
	filepath = "./eclipse_old.json"
	alltraces = read_json_file(filepath)
	allbuckets = get_buckets(alltraces)
	o,c,d = Trainning(alltraces,allbuckets,0,0,0,0.01,0.1,0.1,1,2,2)




if __name__ == "__main__":
	main()
