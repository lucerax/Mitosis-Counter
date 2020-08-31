from cluster import *
import time
x =-1
import uuid
def gen_id():
    yield int(x+1)
    #yield uuid.uuid4()

#merge_cluster(ClusterPair().cluster1, ClusterPair().cluster2)
def merge_cluster(threshold, c1, c2, pair_heap, cluster_list):
    # O(n2) due to distance updating :((
    remove_pairs_with(c2, pair_heap, cluster_list, c1)
    #print("Removed pairs including {}".format(c2))
    c1.add_boxes(c2)
    update_pair_dists(c1, pair_heap, cluster_list)

    #print("Merged {} into {}".format(c2, c1))
    cluster_list.remove(c2)
    #print("Updated list of clusters.")

def update_pair_dists(c, pair_heap, cluster_list):

    for cluster in cluster_list:
        if c!=cluster:
            pair1 = str(c) +  "/" + str(cluster)
            try:
                idx = pair_heap.lookup(pair1)
            except KeyError as e:
                pair2 = str(cluster) +  "/" + str(c)
                idx = pair_heap.lookup(pair2)
            pair_heap.lst[idx].update_dist()

            tmp = pair_heap.remove(idx)
            pair_heap.insert(tmp)

            """
            before = [k for k in pair_heap.lst]


            for i, p in enumerate(pair_heap.lst):
                if before[i] != p:
                    print(before[i], "was moved, dist = ", before[i].dist)
                    print(before[i].dist > p.dist)


            #re-heapify with updated distances
"""

def remove_pairs_with(c, pair_heap, cluster_list, new_parent):
    #O(nlogn) where n is elements in cluster_list
    #before removing pair of c and cluster, update pair of new_parent and cluster distance
    for cluster in cluster_list:
        if c!=cluster and cluster!=new_parent:
            pair1 = str(c) +  "/" + str(cluster)
            try:
                idx = pair_heap.lookup(pair1)
            except KeyError as e:
                pair2 = str(cluster) +  "/" + str(c)
                idx = pair_heap.lookup(pair2)

            pair_heap.remove(idx)

def make_pairs():
    cluster_pairs.clear()
    def stage_pairs():
        seen = {}

        to_pair = []
        for c1 in list_of_clusters:
            #print("Pairing ", c1)
            for c2 in list_of_clusters:
                if c1.id < c2.id:
                    tmp = ClusterPair(c1, c2)
                    to_pair.append(tmp)
                    """
                    try:
                        if not seen[tmp.__str__()]:
                        #print("tmp: ", tmp.cluster1, tmp.cluster2)
                            to_pair.append(tmp)
                            #cluster_pairs.insert(tmp)
                            seen[tmp] = True
                    except KeyError as e:
                        seen[tmp.__str__()] = True
                        to_pair.append(tmp)
                    """
        return to_pair
    pairs = stage_pairs()
    for p in pairs:
        cluster_pairs.insert(p)
    print("Pairs all made")


###########################################################################
#LOAD PICKLE FILE
with open(os.path.join('extracted', '2ndstage_ODAEL_inference.p'), 'rb') as f:
    test = pickle.load(f)
count = 0
pos = 0
data_array = []
activation = 0.54 #For ODAEL as training set
threshold_dist = 3400 #radius of total scanning region in px?

#LOAD DATA FROM FILE
for row in test:
    print(row)

file = '8c9f9618fcaca747b7c3.svs'
#file = '8c9f9618fcaca747b7c3.svs'
results = {}
results['f3741e764d39ccc4d114.svs'] = [12000, 13]

"""
c91a842257ed2add5134.svs
add0a9bbc53d1d9bac4c.svs - 50 d=5000, complete
96274538c93980aad8d6.svs
f26e9fcef24609b988be.svs
8c9f9618fcaca747b7c3.svs - [11 with d=5000, complete], [19 with d=3400, centroid]
be10fa37ad6e88e1f406.svs- [3 with d=3000]
dd4246ab756f6479c841.svs
1018715d369dd0df2fc0.svs
552c51bfb88fd3e65ffe.svs- [8 with d = 3000]
c86cd41f96331adf3856.svs- [9 with d=3400, centroid]
f3741e764d39ccc4d114.svs - [8 with d=3400]
"""

for row in test[file]:
    count+=1
    if row[5].item() > activation:
        pos+=1
        #print(row)
        data_array.append(row)
print("Total number of boxes identified: ", count)
print("Using a threshold of {}, {} mitotic figures found".format(activation, pos))



#Initialize variables
boxes = [Box(i, row[0], row[1], row[2], row[3]) for i, row in enumerate(data_array)]
print("boxes done")
list_of_clusters = []
for i,box in enumerate(boxes):
    x = next(gen_id())
    list_of_clusters.append(Cluster(x, [box]))
cluster_pairs = BinHeap()

"""
print("=======Initial Data=======")
for b in boxes:
    print(b)
for c in list_of_clusters:
    print(c, "dist", c.dist)
"""
start_making = time.time()
make_pairs()
end_making = time.time()
p = cluster_pairs.peek_root()
print(p, "dist", p.dist)
print("Time to make: ", end_making-start_making)
print("=========================")


start_main = time.time()
while len(list_of_clusters) > 1 and cluster_pairs.peek_root().dist < threshold_dist:
    closest_pair = cluster_pairs.pop_root()
    merge_cluster(threshold_dist, closest_pair.cluster1, closest_pair.cluster2, cluster_pairs, list_of_clusters)
    #for p in cluster_pairs.lst:
        #print(p, "dist", p.dist)
    #print("==============")
end_main = time.time()

mx = 0
max_clus = ''
for l in list_of_clusters:
    if len(l.boxes) > mx:
        mx = len(l.boxes)
        max_clus = l.__str__()
print("{} has {} mitotic figures".format(max_clus, mx))
print("Total time taken was ", end_main - start_main)
results[file] = [threshold_dist, mx]
