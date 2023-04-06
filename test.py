# from input import getData


# dataPath = '/Users/YeungYathin/Desktop/创新实践/UFLP_Datasets/ORLIB/ORLIB-uncap/70/cap71.txt'
# m,n,f,c = getData(dataPath=dataPath)
# print(m,n,f,c)

# with open('/Users/YeungYathin/Desktop/创新实践/复现代码/PSO/DPSO_TEST/OUTPUT/test.txt', "w+") as f:
#     f.write("aa\naa")
# import time
    
# start = time.time()
# print(0)
# i = 0
# while i < 10000000:
#     i+=1
# t = time.time()
# print(t-start)

# a = open('/Users/YeungYathin/Desktop/创新实践/复现代码/PSO/M/O/MO1.opt', 'r')
# b = a.read()
# print(b)

# import copy
# import numpy as np

# class dog:
#     x = None
#     y = None
    
# a = dog()
# a.x = 1
# a.y = np.array([1,2,3])

# b = copy.deepcopy(a)
# b.x = 2
# b.y[1] = 4

# print(a.x, a.y)
# print(b.x, b.y)

# class dog:
#     def shout(self):
#         self.a = 1

# a = dog()
# a.shout()
# print(a.a)

# import heapq

# class MedianHeap:
#     def __init__(self):
#         self.small_heap = []
#         self.large_heap = []

#     def add_number(self, num):
#         if not self.small_heap or num < -self.small_heap[0]:
#             heapq.heappush(self.small_heap, -num)
#         else:
#             heapq.heappush(self.large_heap, num)

#         # Balance the heaps
#         if len(self.small_heap) > len(self.large_heap) + 1:
#             heapq.heappush(self.large_heap, -heapq.heappop(self.small_heap))
#         elif len(self.large_heap) > len(self.small_heap):
#             heapq.heappush(self.small_heap, -heapq.heappop(self.large_heap))

#     def get_median(self):
#         if len(self.small_heap) == len(self.large_heap):
#             return (-self.small_heap[0] + self.large_heap[0]) / 2.0
#         else:
#             return -self.small_heap[0]
        
#     def get_len(self):
#         return len(self.small_heap) + len(self.large_heap)

# numbers = [1.2, 3.4, 0.5, 0.1, 5.6, -0.3]
# median_heap = MedianHeap()
# for num in numbers:
#     median_heap.add_number(num)
# median_heap.add_number(5)
# print("所有浮点数的中位数是:", median_heap.get_median())
# print(median_heap.get_len())


# print(median_heap.get_median())

# print(1/6)

# def a(m):
#     print(m)
    
# def b(n):
#     print(n)
    
# c = []
# c.append(a)
# c.append(b)

# c[0](1)
# c[1](2)

# import copy
# class dog:
#     c = None
    
# class cat:
#     ls = [1,2,3]
    
# a = dog()
# a.c = cat()

# b = copy.deepcopy(a)
# b.c.ls[0] = 1000

# print(b.c.ls)
# print(a.c.ls)

# print(list(range(1,7)))


# my_list = [1, 7, 1, 1, 4, 6]

# min_value = min(my_list)
# min_index = my_list.index(min_value)

# print("最小值为:", min_value)
# print("最小值的索引为:", min_index)

# import random
# rand_nums = set()
# while len(rand_nums) < 4:
#     rand_num = random.randint(0, 100)
#     rand_nums.add(rand_num)
    
# print(rand_nums)

# big_array = [[] for _ in range(100)]
# print(big_array)
# import heapq
# from heapq import heappush, heapify, heappop
# class MedianHeap:
#     def __init__(self):
#         self.max_heap = []  # 存储较小的一半元素的大根堆
#         self.min_heap = []  # 存储较大的一半元素的小根堆
        
#     def add(self, x):
#         if not self.max_heap or x < -self.max_heap[0]:
#             heappush(self.max_heap, -x)
#         else:
#             heappush(self.min_heap, x)
#         self._rebalance()
        
#     def remove(self, x):
#         if x in self.max_heap:
#             i = self.max_heap.index(x)
#             self.max_heap[i] = -float('inf')
#             heapify(self.max_heap)
#         elif x in self.min_heap:
#             i = self.min_heap.index(x)
#             self.min_heap[i] = float('inf')
#             heapify(self.min_heap)
#         self._rebalance()
            
#     def median(self):
#         if len(self.max_heap) == len(self.min_heap):
#             return (-self.max_heap[0] + self.min_heap[0]) / 2.0
#         else:
#             return -self.max_heap[0]
        
#     def _rebalance(self):
#         if len(self.max_heap) > len(self.min_heap) + 1:
#             root = -heappop(self.max_heap)
#             heappush(self.min_heap, root)
#         elif len(self.min_heap) > len(self.max_heap) + 1:
#             root = heappop(self.min_heap)
#             heappush(self.max_heap, -root)
            
#     def get_len(self):
#         return len(self.max_heap) + len(self.min_heap)
            
# numbers = [1.2, 3.4, 0.5, 0.1, 5.6, -0.3]
# median_heap = MedianHeap()
# for num in numbers:
#     median_heap.add(num)
# median_heap.add(5)
# print("所有浮点数的中位数是:", median_heap.median())
# print(median_heap.get_len())
# median_heap.remove(5)
# print(median_heap.get_len())

a = [0,1]
a.remove(2)