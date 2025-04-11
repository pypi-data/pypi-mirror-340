class Node:
  def __init__(self, value, next = None, prev = None):
    self.value = value
    self.next = next
    self.prev = prev

# Allow the methods to handle double linked lists

class LinkedList:
  def __init__(self,double = False):
    self.head = None
    self.double = double

  # Inserting a node at the beginning of the list
  def InsertAtBeg(self, item):
    if self.head:
      new = Node(item)
      new.next = self.head
      if self.double:
        self.head.prev = new
      self.head = new
    else:
      self.head = Node(item)

  # Inserting a node at a particular position of the list
  def InsertAtPos(self, item, index):
    node = Node(item)
    if ((not self.head) and (index == 0)) or (index == 0):
      self.InsertAtBeg(item)
    else:
      i = 0
      temp = self.head

      while i < index and temp.next != None:
        i += 1
        prev = temp
        temp = temp.next

      if i == index:
        node.next = temp
        prev.next = node
        if self.double:
          temp.prev = node
          node.prev = prev

      elif index == i+1:
        self.InsertAtEnd(item)
      else:
        raise IndexError("This index is out of bounds")


  # Inserting a node at the end of the list
  def InsertAtEnd(self, item):
    last = Node(item)
    if self.head:
      temp = self.head
      while temp.next:
        prev = temp
        temp = temp.next
      temp.next = last
      if self.double:
        last.prev = temp
    else:
      self.head = last

  # Deleting a node with its index
  def deleteItem(self, index):
    i = 0
    tem = self.head
    if not self.head:
      raise IndexError("The list is empty")
      pass
    else:
      if index == 0:
        self.head = self.head.next
      while tem.next and i < index:
        prev = tem
        tem = tem.next
        i += 1
      if i == index and index != 0:
        if self.double:
          tem.next.prev = prev
        prev.next = tem.next
      elif not tem.next:
        raise IndexError(f'There is less than {index} elements in the linked list')

  # Get_length: count the number of nodes in the list

  def get_length(self):
    if not self.head:
      return 0
    else:
      i = 1
      temp = self.head
      while temp.next:
        i += 1
        temp = temp.next
      return i

  # Access: return the value of the node at the given position
  def access(self, index):
    if self.get_length() == 0 :
      print(f"The list is empty")
    elif self.get_length() <= index:
     raise IndexError("Index out of bound")
    else:
      temp = self.head
      for k in range(index):
        temp = temp.next
      return temp.value


  # Allow subscription

  def __getitem__(self, index):
      if isinstance(index, int):
      # Handle single index subscription
        if index >= 0:
          return self.access(index)
        else:
          if abs(index) <= self.get_length():
            return self.access(self.get_length() + index)
          else:
            raise IndexError("Index out of bound")
      else:
        raise TypeError("Invalid index type")

  # Search: look for a node with a specific value or property

  def search(self, key):
    '''Returns a list of indices of the nodes with value = key
    The list is empty if there is no node with value = key'''

    if self.get_length() == 0:
      raise IndexError(f"The list is empty")
    else:
      indices = []
      i = 0
      temp = self.head
      while temp is not None:
        if temp.value == key:
          indices.append(i)
        temp = temp.next
        i += 1
      return indices

  # Reverse the linked list

  def reverse_list(self):
    if self.IsEmpty():
      raise IndexError("The list is empty")
    else:
      new_list = LinkedList(self.double)
      temp = self.head

      while temp.next:
        new_list.InsertAtBeg(temp.value)
        temp = temp.next
      new_list.InsertAtBeg(temp.value)
      return new_list

  # Update a value at a particular position
  def update(self, new_val, pos):
    n = self.get_length()
    if n != 0:
      tem = self.head
      if pos <= n and pos >= 0 or (pos < 0 and pos >= -n):
        if pos < 0 :
          for i in range(n + pos):
            tem = tem.next
          tem.value = new_val
        else:
          for i in range(pos):
            tem = tem.next
          tem.value = new_val
      else:
        raise IndexError(f"Index {pos} out of range")
    else:
      raise IndexError(f"Cannot update element in an empty list")
  def IsEmpty(self):
    return  self.get_length() == 0

  def last_node(self):
    if self.head is None:
      raise IndexError("The linked list is empty")
    else:
      tem = self.head
      while(tem.next):
        tem = tem.next
      return tem

  def concatenate(self, L1, L2):
    pass

  def display(self):
      node = self.head

      a = "<-->" if self.double else "->"
      while node:
          print(node.value, end = a)
          node = node.next
      print('')



