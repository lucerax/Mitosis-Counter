from minheap import *
from math import *
import numpy as np
import pickle
import os
import torch
import statistics as stat

class Cluster:
    def __init__(self, id, boxes):
        self.boxes = boxes
        self.centroid = self.get_centroid()
        self.dist = find_distance(self, linkage='centroid')
        self.id = id

    def get_num_boxes(self):
        return len(self.boxes)

    def get_centroid(self):
        cx = stat.mean([b.get_centre()[0] for b in self.boxes])
        cy = stat.mean([b.get_centre()[1] for b in self.boxes])
        return [cx, cy]

    def get_max_dist(self, linkage, metric):
        #max euclidean distance between any two points
        """
        if type == 'centroid':
            mx = 0
            return max([])
        elif linkage == 'complete':
            #theta(ij) where i, j are number of points in each cluster
            #O(N^2)
            mx = 0
            for b1 in self.boxes:
                dists = [sqrt((b1.get_centre()[0] - b2.get_centre()[0])**2 + (b1.get_centre()[1] - b2.get_centre()[1])**2) for b2 in self.boxes]
                mx = max(mx, max(dists))
            return mx
            """

    def add_boxes(self, clus):
        self.boxes += clus.boxes
        self.centroid = self.get_centroid()
        self.dist = find_distance(self, linkage='centroid')

    def __eq__(self, other):
        self.boxes.sort()
        other.boxes.sort()
        #print(self.boxes == other.boxes)
        return self.boxes == other.boxes and self.id == other.id
    def __lt__(self, other):
        return self.id < other.id
    def __gt__(self, other):
        return self.id > other.id

    def __str__(self):
        return "cluster " + str(self.id)


class Box:
    def __init__(self, id, x1, y1, x2, y2, cls=1, score=1):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.cls = cls
        self.score = score
        self.id = id

    def get_centre(self):
        return [(self.x1 + self.x2)/2, (self.y1 + self.y2)/2]


    def in_range(self, x_cen, y_cen, dist):
        return (self.get_centre()[0] <= x_cen + dist) and (self.get_centre()[1] <= y_cen + dist)
    def __eq__(self, other):
        return self.id == other.id
    def __lt__(self, other):
        return self.id < other.id
    def __gt__(self, other):
        return self.id > other.id
    def __str__(self):
        return "box " + str(self.id)




linkages = ['complete', 'single', 'centroid']
metrics = ['euclidean', 'manhattan', 'max']

def find_distance(cluster1, cluster2=None, linkage = 'complete', metric = 'euclidean'):
    if linkage not in linkages:
        raise ValueError('Linkage type should be one of: ', linkages)
    if metric not in metrics:
        raise ValueError('Metric type should be one of: ', metrics)
    if linkage == 'complete':
        return complete_linkage(cluster1, cluster2, metric)
    elif linkage == 'centroid':
        return centroid_linkage(cluster1, cluster2, metric)
    #TODO: update other methods
    else:
        print('Linkage method not implemented yet.')


def centroid_linkage(cluster1, cluster2=None, metric='euclidean'):
    if metric == 'euclidean':
        if cluster2:
            #EXTERNAL DISTANCE
            temp = cluster1.boxes + cluster2.boxes
            cx = stat.mean([b.get_centre()[0] for b in temp])
            cy = stat.mean([b.get_centre()[1] for b in temp])
            cen = [cx, cy]
            dists = [sqrt((b.get_centre()[0] - cen[0])**2 + (b.get_centre()[1] - cen[1])**2) for b in temp]
            return max(0, max(dists))
        else:
            #INTERNAL DISTANCE
            cen = cluster1.centroid
            dists = [sqrt((b1.get_centre()[0] - cen[0])**2 + (b1.get_centre()[1] - cen[1])**2) for b1 in cluster1.boxes]
            return max(0, max(dists))
    #TODO: update other methods
    else:
        print('Metric method not implemented yet.')


def complete_linkage(cluster1, cluster2=None, metric='euclidean'):
    #theta(ij) where i, j are number of points in each cluster
    #O(N^2)
    if metric == 'euclidean':
        if cluster2:
            #EXTERNAL DISTANCE
            for b1 in cluster1.boxes:
                dists = [sqrt((b1.get_centre()[0] - b2.get_centre()[0])**2 + (b1.get_centre()[1] - b2.get_centre()[1])**2) for b2 in cluster2.boxes]

            return max(0, max(dists))
        else:
            #INTERNAL DISTANCE
            for b1 in cluster1.boxes:
                dists = [sqrt((b1.get_centre()[0] - b2.get_centre()[0])**2 + (b1.get_centre()[1] - b2.get_centre()[1])**2) for b2 in cluster1.boxes]

            return max(0, max(dists))

    #TODO: update other methods
    else:
        print('Metric method not implemented yet.')

#Makes it a bit more convenient to place the objects into a priority queue
class ClusterPair:
    def __init__(self, cluster1, cluster2):
        self.cluster1 = cluster1
        self.cluster2 = cluster2
        self.dist = find_distance(cluster1, cluster2, 'centroid')
    def update_dist(self):
        self.dist = find_distance(self.cluster1, self.cluster2, 'centroid')
    def __eq__(self, other):
        a = [self.cluster1, self.cluster2]
        a.sort()
        b = [other.cluster1, other.cluster2]
        b.sort()
        return self.dist == other.dist and a == b
    def __lt__(self, other):
        return self.dist < other.dist
    def __gt__(self, other):
        return self.dist > other.dist
    def __str__(self):
        return "Cluster-Pair " + str(self.cluster1.id) + "/" + str(self.cluster2.id)









"""
each mitotic figure is represented as a box of coords
cluster is a circular region that contains a list of boxes, a centroid location,
funcs: add_box (updates centroid too)
merge_cluster - checks if distance(def = complete_linkage) is less than threshold, then adds all
"""
