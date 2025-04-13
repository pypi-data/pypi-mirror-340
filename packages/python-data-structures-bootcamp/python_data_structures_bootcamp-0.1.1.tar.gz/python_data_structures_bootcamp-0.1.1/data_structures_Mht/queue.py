class Queue:
    def __init__(self, lists=None):
        if lists is None:
            lists = []
        self.queue = lists

    def enqueue(self, element):
        self.queue.append(element)

    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop(0)
        return None

    def dequeue_asc(self): 
        if not self.is_empty():
            smallest = min(self.queue)
            self.queue.remove(smallest)
            return smallest
        return None

    def display_queue(self):
        print(self.queue)

    def is_empty(self):
        return len(self.queue) == 0

    def peek(self):
        if not self.is_empty():
            return self.queue[0]
        return None

    def rear(self):
        if not self.is_empty():
            return self.queue[-1]
        return None
