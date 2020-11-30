



class Node:
    def __init__(self, value = None, next = None):
        self.item = value
        self.next = next


class LinkedQ:
	def __init__(self):
		self.__first = None

	def enqueue(self, newdata):
		if self.__first == None:
			newnode = Node(newdata)
			self.__first = newnode
			self.__bot = newnode
			return
		newnode = Node()
		newnode.item = newdata
		self.__bot.next = newnode
		self.__bot = newnode

	def dequeue(self):
		if self.__first == None: return None
		theitem = self.__first.item
		self.__first = self.__first.next
		return theitem

	def isEmpty(self):
		return self.__first == None

	def peek(self):
		if self.__first == None: return None
		return self.__first.item



class Ruta:
    def __init__(self, atom="( )", num=1):
        self.atom = atom
        self.num = num
        self.next = None
        self.down = None