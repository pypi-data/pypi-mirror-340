class Stack:
    def __init__(self, para=[]):
      self.stack = para

    def push(self,newElement):
      return self.stack.append(newElement)

    def pop(self):
      if not self.is_Empty():
        return self.stack.pop(-1)
      else:
        print("It is empty my friend, do not insist")

    def is_Empty(self):
      return len(self.stack) == 0

    def peek(self):
        if not self.is_Empty():
            return self.stack[-1]
        return None

    def display_stack(self):
      print(self.stack)