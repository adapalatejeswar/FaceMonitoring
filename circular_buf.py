from numpy import ndarray
import numpy as np
from collections import deque
import timeit
import cv2

class RingBuffer():

    def __init__(self, shape, dtype='uint8'):
        self.shape = shape
        self.size = self.shape[0]
        self.top = 0
        self.bottom = 0
        self.data = np.empty(shape=self.shape, dtype=dtype)
        self.length = 0

    #@profile
    def append(self, element):
        """ Write new element on top """
        self.data[self.top] = element

        """ Increment the size """
        self.length = min(self.length + 1, self.size)
        
        """ Update the top n bottom indexes. shift bottom by 1 in case of it's overwrite """
        self.top = (self.top + 1) % self.size
        if self.top == self.bottom:
            self.bottom = (self.top + 1) % (self.size - 1)

        #print (self.data, self.bottom, self.top, self.length)

    #@profile
    def pop(self):
        """ Decrement the size """
        if self.length:
            self.length = min(self.length - 1, self.size)
        else:
            raise AssertionError("Nothing to pop!")

        """ Returns the topmost element """
        top = self.data[self.top-1]
        
        """ Reduce the top index """
        self.top = (self.top -1) % self.size

        #print (self.data, self.bottom, self.top, self.length)
        return top
 
   
    #@profile
    def read_bottom(self,index):
        """ Decrement the size """
        return self.data[(index-1) % self.size]

#def get_item():
#    return 1#np.ones(shape=(10000, 1))
#
#def ring_buffer_test():
#    size = 1000
#    buffer = RingBuffer(shape=(size, 1))
#    item = get_item()
#    
#    for i in range(1000):
#        buffer.append(item)
#
##@profile
#def dequeue_test():
#    size = 1000
#    """ Some performance tests. Compared with python queue """
#    buffer = deque(np.zeros(size, dtype=np.int), maxlen=size)
#    item = get_item()
#
#    for i in range(1000):
#        buffer.append(item)
#        np.array(list(buffer))
#
#print ("Dequeue: %f" % timeit.timeit(dequeue_test, number=100))
#print ("Ring buffer: %f" % timeit.timeit(ring_buffer_test, number=100))