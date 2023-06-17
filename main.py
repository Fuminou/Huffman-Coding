import heapq # Hint: use Python's priority queue class, heapq.
import sys

file = sys.argv[1]

class Node:
    def __init__(self, count, leftChild, rightChild):
        self.count    = count
        self.leftChild = leftChild
        self.rightChild = rightChild
        
    def is_leaf(self):
        return False
        
    def __lt__(self, other):
        return self.count < other.count

    def __eq__(self, other):
        return self.count == other.count
    
        
class LeafNode(Node):
    def __init__(self, symbol, count, leftChild, rightChild):
        super().__init__(count, leftChild, rightChild)
        self.symbol = symbol
        
    def is_leaf(self):
        return True

class HuffmanCode:
    def __init__(self, F):
        self.C = dict()
        self.T = huffmanTree(F)
        self.cost = 0
        self.average_cost = 0
        # TODO: Construct the Huffman Code and set C, T, cost, and average_cost properly!

        str = ""
        str = dfsTraversal(self.T, self.C, str)

        sum = 0
        cost = 0
        for x in F:
            sum += F[x]
            self.cost += F[x] * len(self.encode(x))

        self.average_cost = self.cost/sum

        

    def encode(self, m):
        """
        Uses self.C to encode a binary message.
.    
        Parameters:
            m: A plaintext message.
        
        Returns:
            The binary encoding of the plaintext message obtained using self.C.
        """
        
        # TODO: Implement this method!

        str = ""
        for i in range(0, len(m)):
            str += self.C[m[i]]

        return str
        
    def decode(self, c):
        """
        Uses self.T to decode a binary message c = encode(m).
.    
        Parameters:
            c: A message encoded in binary using self.encode.
        
        Returns:
            The original plaintext message m decoded using self.T.
        """
        
        # TODO: Implement this method!

        t = self.T
        str = ""
        i = 0

        while(i < len(c)):
            # binary for left = 0
            if c[i] == "0":
                i += 1
                t = t.leftChild
            # binary for right = 1
            else:
                i += 1
                t = t.rightChild
            
            if t.is_leaf():
                str += "".join(t.symbol)
                t = self.T

        return str
        
    def get_cost(self):
        """
        Returns the cost of the Huffman code as defined in CLRS Equation 16.4.
        
        Returns:
            Returns the cost of the Huffman code.
        """ 
                
        return self.cost
        
    def get_average_cost(self):
        """
        Returns the average cost of the Huffman code.
        
        Returns:
            Returns the average cost of the Huffman code.
        """ 
                
        return self.average_cost
    

def get_frequencies(s):
    """
    Computes a frequency table for the input string "s".
    
    Parameters:
        s: A string.
        
    Returns:
        A frequency table F such that F[c] = (# of occurrences of c in s).
    """

    F = dict()
    
    for char in s:
        if not(char in F):
            F[char] = 1
        else:
            F[char] += 1
            
    return F
    
def get_frequencies_from_file(file_name):
    """
    Computes a frequency table from the text in file_name.
    
    Parameters:
        file_name: The name of a text file.
        
    Returns:
        A frequency table F such that F[c] = (# of occurrences of c in the contents of <file_name>).
    """
    f = open(file_name, "r")
    s = f.read()
    f.close()

    return get_frequencies(s)

def huffmanTree(dic):
    sum = 0
    li = []
    for x in dic:
        n = LeafNode(x, dic[x], None, None)
        sum += dic[x]
        heapq.heappush(li, n)

    while li:
        n1 = heapq.heappop(li)
        if n1.count == sum:
            heapq.heappush(li, n1)
            break

        n2 = heapq.heappop(li)
        newNode = Node(0, n1, n2)
        newNode.count = n1.count + n2.count
        heapq.heappush(li, newNode)

    return heapq.heappop(li)

def dfsTraversal(rootNode, dic, str):
        
    if rootNode.leftChild is not None:
        str = str + "0"
        str = dfsTraversal(rootNode.leftChild, dic, str)

    if rootNode.is_leaf():
        dic[rootNode.symbol] = str
        
    if rootNode.rightChild is not None:
        str = str + "1"
        str = dfsTraversal(rootNode.rightChild, dic, str)

    if(len(str) > 0):
        str = str[:len(str) - 1]
        
    return str

dic = get_frequencies_from_file("cs325-w23-homework3-gettysburg-address.txt")
h = HuffmanCode(dic)
print(h.get_cost())
print(h.get_average_cost())
str = "go beavers"
print(h.encode(str))
str = "oregon state rules"
print(h.encode(str))
print(h.decode("11001010010010101110111011101010011010010001"))
print(len(h.encode(str)))
