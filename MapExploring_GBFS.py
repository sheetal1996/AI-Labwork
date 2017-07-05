RomaniaMap={	'Arad': {'Sibiu': 140, 'Zerind': 75,'Timisoara': 118}, 
				'Zerind': {'Arad': 75, 'Oradea': 71}, 
				'Timisoara': {'Arad':118,'Lugoj': 111}, 
				'Lugoj': {'Timisoara': 111, 'Mehadia': 70}, 
				'Mehadia': {'Lugoj': 70, 'Drobeta':75},
				'Oradea':{'Zerind':71, 'Sibiu':151},
				'Sibiu':{'Oradea':151, 'Arad':140, 'Rimnicu Vilcea':80, 'Fagaras':99},
				'Rimnicu Vilcea':{'Pitesti':97, 'Sibiu':80, 'Craiova':146},
				'Pitesti':{'Rimnicu Vilcea':97, 'Craiova':138, 'Bucharest':101},
				'Craiova':{'Pitesti':138, 'Rimnicu Vilcea':146,  'Drobeta':120},
				'Bucharest':{'Pitesti':4, 'Fagaras':211},
				'Drobeta':{'Mehadia':75, 'Craiova':120},
				'Fagaras':{'Sibiu':99, 'Bucharest':211}
	}

h={	'Arad': 366, 
	'Zerind': 374, 
	'Timisoara': 329, 
	'Lugoj': 244, 
	'Mehadia': 241,
	'Oradea': 380,
	'Sibiu': 253,
	'Rimnicu Vilcea': 193,
	'Pitesti': 100,
	'Craiova': 160,
	'Bucharest': 0,
	'Drobeta': 242,
	'Fagaras': 176

	}
def display_map(map):
	print 'To\t\tFrom\t\tCost'
	print '_____________________________________________________'
	for k1 in map.keys():
		for k2 in map[k1].keys():
			print "{:<15} {:<15} {:<15}".format(k1,k2, map[k1][k2])
			
def create_node( value, parent, depth, cost ):
	return Node( value, parent, depth, cost )

def expand_node( node, openlist, closedlist):
	"""Returns a list of expanded nodes"""
	neighbours=RomaniaMap[node.value]
	expanded_nodes = []
	val=[]
	for k,v in neighbours.iteritems():
		expanded_nodes.append( create_node(k, node, node.depth + 1, node.cost+v) )
	return expanded_nodes
	
def gbfs( start, goal, depth=10):
	"""Performs a depth first search from the start state to the goal. Depth param is optional."""
	depth_limit = depth
	# A list (can act as a stack too) for the nodes.
	nodes = []
	# Create the queue with the root node in it.
	nodes.append( create_node( start, None, 0,0) )
	closedlist=[]
	print 'Traversal: [ ',
	while True:
		# We've run out of states, no solution.
		if len( nodes ) == 0: return None
		# take the node from the end of the queue
		sort(nodes)
		node = nodes.pop(0)
		closedlist.append(node)
		print '( ',node.value, ', ',h[node.value],'); ',
		# if this node is the goal, return the moves it took to get here.
		if node.value == goal:
			print ' ]'
			sol=[]
			cost=node.cost
			temp = node
			while True:
				sol.insert(0,temp.value)
				if temp.depth < 1: break
				temp = temp.parent
			#return moves
			return cost,sol				
		# Add all the expansions to the beginning of the stack if we are under the depth limit
		if node.depth < depth_limit:
			nodes.extend( expand_node( node, nodes, closedlist ) )

def sort(nodes):
	for j in range(len(nodes)):
			for i in range(len(nodes)-1):
				if (h[nodes[i].value]) > (h[nodes[i+1].value]):
					temp=nodes[i]
					nodes[i]=nodes[i+1]
					nodes[i+1]=temp
					
class Node:
	def __init__( self, value, parent, depth, cost ):
		# Contains the state of the node
		self.value = value
		# Contains the node that generated this node
		self.parent = parent
		# Contains the operation that generated this node from the parent
		#self.operator = operator
		# Contains the depth of this node (parent.depth +1)
		self.depth = depth
		# Contains the path cost of this node from depth 0. Not used for depth/breadth first.
		self.cost = cost
		
def main():
	print "Map: "
	display_map(RomaniaMap)
	#print "Enter start state:  "
	#starting_state=raw_input()
	#print "Enter goal state:  "
	#goal_state=raw_input()
	starting_state='Arad'
	goal_state='Bucharest'
	if starting_state not in RomaniaMap.keys() or starting_state not in RomaniaMap.keys():
		print "Invalid state error, start or goal state doesn't exist in the map!"
	if starting_state==goal_state:
		print "Start state is the goal"
	else:
		cost,result = gbfs( starting_state, goal_state )
		if result == None:
			print "No solution found"
		else:
			print "Start: ", starting_state
			print "Goal: ", goal_state
			print "Solution: ",result
			print "Cost: ",cost
			print "Length of Path: ", (len(result)-1)
			
if __name__ == "__main__":
	main()
	