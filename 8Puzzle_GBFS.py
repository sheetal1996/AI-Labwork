### Data Structures
#
# The state of the board is stored in a list. The list stores values for the
# board in the following positions:
#
# -------------
# | 0 | 3 | 6 |
# -------------
# | 1 | 4 | 7 |
# -------------
# | 2 | 5 | 8 |
# -------------
#
# The goal is defined as:
#
# -------------
# | 1 | 2 | 3 |
# -------------
# | 8 | 0 | 4 |
# -------------
# | 7 | 6 | 5 |
# -------------
#
# Where 0 denotes the blank tile or space.
goal_state = [1, 4, 7, 2, 5, 8, 3, 6, 0]
#
# as above but space seperated. i.e. the content for the goal state would be
# 1 8 7 2 0 6 3 4 5

### Code begins.
import sys
import random as r
def display_board( state ):
	print "-------------"
	print "| %i | %i | %i |" % (state[0], state[3], state[6])
	print "-------------"
	print "| %i | %i | %i |" % (state[1], state[4], state[7])
	print "-------------"
	print "| %i | %i | %i |" % (state[2], state[5], state[8])
	print "-------------"
	
def move_up( state ):
	"""Moves the blank tile up on the board. Returns a new state as a list."""
	# Perform an object copy
	new_state = state[:]
	index = new_state.index( 0 )
	# Sanity check
	if index not in [0, 3, 6]:
		# Swap the values.
		temp = new_state[index - 1]
		new_state[index - 1] = new_state[index]
		new_state[index] = temp
		return new_state
	else:
		# Can't move, return None (Pythons NULL)
		return None

def move_down( state ):
	"""Moves the blank tile down on the board. Returns a new state as a list."""
	# Perform object copy
	new_state = state[:]
	index = new_state.index( 0 )
	# Sanity check
	if index not in [2, 5, 8]:
		# Swap the values.
		temp = new_state[index + 1]
		new_state[index + 1] = new_state[index]
		new_state[index] = temp
		return new_state
	else:
		# Can't move, return None.
		return None

def move_left( state ):
	"""Moves the blank tile left on the board. Returns a new state as a list."""
	new_state = state[:]
	index = new_state.index( 0 )
	# Sanity check
	if index not in [0, 1, 2]:
		# Swap the values.
		temp = new_state[index - 3]
		new_state[index - 3] = new_state[index]
		new_state[index] = temp
		return new_state
	else:
		# Can't move it, return None
		return None

def move_right( state ):
	"""Moves the blank tile right on the board. Returns a new state as a list."""
	# Performs an object copy. Python passes by reference.
	new_state = state[:]
	index = new_state.index( 0 )
	# Sanity check
	if index not in [6, 7, 8]:
		# Swap the values.
		temp = new_state[index + 3]
		new_state[index + 3] = new_state[index]
		new_state[index] = temp
		return new_state
	else:
		# Can't move, return None
		return None

def create_node( state, parent, operator, depth, cost ):
	return Node( state, parent, operator, depth, cost )

def expand_node( node):
	"""Returns a list of expanded nodes"""
	expanded_nodes = []
	expanded_nodes.append( create_node( move_up( node.state ), node, "u", node.depth + 1, h( move_up(node.state)) ) )
	expanded_nodes.append( create_node( move_down( node.state ), node, "d", node.depth + 1, h( move_down(node.state)) ) )
	expanded_nodes.append( create_node( move_left( node.state ), node, "l", node.depth + 1, h( move_left(node.state)) ) )
	expanded_nodes.append( create_node( move_right( node.state), node, "r", node.depth + 1, h( move_right(node.state)) ) )
	# Filter the list and remove the nodes that are impossible (move function returned None)
	expanded_nodes = [node for node in expanded_nodes if node.state != None] #list comprehension!
	return expanded_nodes

def gbfs( start, goal ):
	"""Perfoms an A* heuristic search"""
	nodes = []
	nodes.append( create_node( start, None, None, 0,h( start) ) )
	while True:
		# We've run out of states - no solution.
		if len( nodes ) == 0: return None
		# Sort the nodes.
		sort(nodes)
		node = nodes.pop(0)
		print "Expanding node (Heuristic value: ",node.cost,"): "
		display_board(node.state)
		if node.state == goal:
			moves = []
			sol=[]
			temp = node
			while True:
				moves.insert( 0, temp.operator )
				sol.insert(0,temp.state)
				if temp.depth <=1: break
				temp = temp.parent
			return moves, sol
		#Expand the node and add all expansions to the end of the queue.
		nodes.extend( expand_node( node) )
		
def sort(nodes):
	for j in range(len(nodes)):
			for i in range(len(nodes)-1):
				if (nodes[i].cost) > (nodes[i+1].cost):
					temp=nodes[i]
					nodes[i]=nodes[i+1]
					nodes[i+1]=temp
					
def h( state, goal = goal_state):
	score = 0
	if state!=None:
		for i in range( len(state)):
			if state[i] != goal[i]:
				score = score + 1
	return score

# Node data structure
class Node:
	def __init__( self, state, parent, operator, depth, cost ):
		# Contains the state of the node
		self.state = state
		# Contains the node that generated this node
		self.parent = parent
		# Contains the operation that generated this node from the parent
		self.operator = operator
		# Contains the depth of this node (parent.depth +1)
		self.depth = depth
		# Contains the path cost of this node from depth 0. Not used for depth/breadth first.
		self.cost = cost

# Main method
def main():
	#starting_state = readfile( "state.txt" )
	starting_state=[2,1, 7, 0, 4, 5, 3, 6, 8]
	#r.shuffle(starting_state)
	print starting_state
	moves, result = gbfs( starting_state, goal_state )
	print "Initial state: "
	display_board(starting_state)
	print "Goal state: "
	display_board(goal_state)
	if result == None:
		print "No solution found"
	elif result == [None]:
		print "Start node was the goal!"
	else:
		print "Solution: "
		for i in result:
			display_board(i)
		print moves
		print len(result), " moves"

# A python-isim. Basically if the file is being run execute the main() function.
if __name__ == "__main__":
	main()
