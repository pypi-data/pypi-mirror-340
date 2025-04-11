from data_structures.linked_lists import LinkedList
from data_structures.array import Array_new
# Add features to handle linked lists

# Add features to handle linked lists

class Stack:
    def __init__(self, para):
      self.stack = para    
      self.size = self.size_stack()
    
    def __str__(self):
      if type(self.stack) == Array_new:
        return f"{self.stack}"

    def push(self,newElement):
      """This insert an element at a specific position. The default position is 0"""
      if type(self.stack) == Array_new:
        a = [0] + [s for s in self.stack]
        a[0] = newElement
        
        self.stack = Array_new(a)
        self.size += 1 
        
      if type(self.stack) == LinkedList:
        self.stack.InsertAtBeg(newElement)
        self.size += 1 


    def peek(self):
      """Return the last element of the stack"""
      if not self.isEmpty():
        return self.stack[-1]  
      else: 
        raise IndexError("Empty stack")

    def pop_stack(self, index = -1):
      """Delete and return the last element (default value) of the stack"""
      if type(self.stack) == Array_new:
        a = self.stack.pop_array()
        self.size -= 1
        return a

      if type(self.stack) == LinkedList:
        self.stack.deleteItem(index)
        self.size -= 1
        return self.stack.access(index)
    def top(self):
      if not self.isEmpty():
        return self.stack[-1]  
      else: 
        raise IndexError("Empty stack")
    # Checks if the stack is empty
    def isEmpty(self):
      return self.size_stack() == 0


    # Size of the stack
    def size_stack(self):
      if type(self.stack) == LinkedList:
        return self.stack.get_length()

      if type(self.stack) == Array_new:
        return len(self.stack)

    # Stack display
    def display_stack(self):
      if type(self.stack) == LinkedList:
        self.stack.display()

      if type(self.stack) == Array_new:
        self.stack.show_array()
