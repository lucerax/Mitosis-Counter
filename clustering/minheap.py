class BinHeap:
    def __init__(self):
        self.lst = []
        self.table = {} #stores indices of data
    def __str__(self):
        out = "\n".join([str(l) for l in self.lst])
        return out

    def lookup(self, id):
        return self.table[id]
        
    def heapify(self):
        self.heapify_up()
        self.heapify_down()

    def insert(self, data):
        self.lst.append(data)
        self.table[str(data.cluster1)+  "/" + str(data.cluster2)] = len(self.lst)-1
        self.heapify_up(len(self.lst) - 1, True)

    def clear(self):
        self.lst = []
        self.table = {}

    def remove(self, index, update_table=True):
        if len(self.lst) == 0:
            raise IOError("Heap is empty")

        to_del = self.lst[index]
        last = self.lst.pop()


        if len(self.lst) > index:
            self.lst[index] = last
            self.table[str(last.cluster1) + "/" + str(last.cluster2)] = index
            if index == 0:
                self.heapify_down(0)

            elif last < self.lst[index//2]:
                self.heapify_up(index)
            else:
                self.heapify_down(index)

        #print("Needa delete: ", str(to_del))
        if update_table:
            try:
                self.table.pop(str(to_del.cluster1) + "/" + str(to_del.cluster2))
            except Exception as e:
                print("CAN'T UPDATE TABLE")

        return to_del

    def pop_root(self):
        return self.remove(0, False)

    def peek_root(self):
        if len(self.lst) == 0:
            raise IOError("Heap is empty")
        return self.lst[0]

    def heapify_down(self, parent_idx, update_table=True):
        assert parent_idx >= 0
        child_idx = parent_idx * 2 + 1
        if child_idx >= len(self.lst):
            return

        if child_idx + 1 < len(self.lst) and self.lst[child_idx] > self.lst[child_idx + 1]:
            child_idx = child_idx + 1
        parent_greater_bool = self.lst[parent_idx] > self.lst[child_idx]

        if parent_greater_bool:
            #swap parent and child entries
            self.lst[parent_idx], self.lst[child_idx] = self.lst[child_idx], self.lst[parent_idx]
            if update_table:
                #Updates lookup table with index of swapped positions
                try:
                    id = str(self.lst[parent_idx].cluster1) +  "/" + str(self.lst[parent_idx].cluster2)
                    self.table[id] = parent_idx
                    id = str(self.lst[child_idx].cluster1) +  "/" + str(self.lst[child_idx].cluster2)
                    self.table[id] = child_idx
                except Exception as e:
                    print("Table should only be updated for cluster pairs.")

            self.heapify_down(child_idx, True)

    def heapify_up(self, child_idx, update_table=True):
        assert child_idx < len(self.lst)
        parent_idx = (child_idx - 1) // 2

        if parent_idx < 0:
            return

        if self.lst[parent_idx] > self.lst[child_idx]:
            self.lst[parent_idx], self.lst[child_idx] = self.lst[child_idx], self.lst[parent_idx]
            if update_table:
                #Updates lookup table with index of swapped positions
                try:
                    id = str(self.lst[parent_idx].cluster1) +  "/" + str(self.lst[parent_idx].cluster2)
                    self.table[id] = parent_idx
                    id = str(self.lst[child_idx].cluster1) +  "/" + str(self.lst[child_idx].cluster2)
                    self.table[id] = child_idx
                except Exception as e:
                    print("Table should only be updated for cluster pairs.")
            self.heapify_up(parent_idx, True)
