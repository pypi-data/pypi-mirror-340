from collections import defaultdict

class Graph:
   """
   A directed graph implementation using an adjacency list.
   
   This class provides methods for building and analyzing a directed graph,
   including cycle detection functionality.
   """
   
   def __init__(self):
       """
       Initialize an empty graph with an adjacency list.
       """
       self.adj_list = defaultdict(list)

   def add_node(self, node):
       """
       Add a node to the graph if it doesn't already exist.
       
       Args:
           node: The node to be added to the graph.
       """
       if node not in self.adj_list:
           self.adj_list[node] = []

   def add_edge(self, src, dest):
       """
       Add a directed edge from source to destination node.
       
       Args:
           src: The source node of the edge.
           dest: The destination node of the edge.
       """
       self.adj_list[src].append(dest)

   def print_graph(self):
       """
       Print the graph's adjacency list representation.
       
       Displays each node along with its list of adjacent nodes.
       """
       for node in self.adj_list:
           print(f"{node} -> {self.adj_list[node]}")

   def has_cycle_util(self, node, visited, rec_stack):
       """
       Utility function used by has_cycle to detect cycles using DFS.
       
       Args:
           node: The current node being visited.
           visited (set): Set of nodes that have been visited.
           rec_stack (set): Set of nodes in the current recursion stack.
           
       Returns:
           bool: True if a cycle is detected, False otherwise.
       """
       visited.add(node)
       rec_stack.add(node)

       for neighbor in self.adj_list[node]:
           if neighbor not in visited:
               if self.has_cycle_util(neighbor, visited, rec_stack):
                   return True
           elif neighbor in rec_stack:
               return True

       rec_stack.remove(node)
       return False

   def has_cycle(self):
       """
       Detect if the directed graph contains any cycles.
       
       Uses depth-first search to identify cycles in the graph.
       
       Returns:
           bool: True if the graph has at least one cycle, False otherwise.
       """
       visited = set()
       rec_stack = set()
       for node in self.adj_list:
           if node not in visited:
               if self.has_cycle_util(node, visited, rec_stack):
                   return True
       return False