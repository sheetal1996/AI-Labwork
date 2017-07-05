#!/usr/bin/python

# The state of the board is stored in a list. The list stores values for the
# board in the following positions:
#
# -------------
# | 1 | 2 | 3 |
# -------------
# | 4 | 0 | 6 |
# -------------
# | 7 | 5 | 8 |
# -------------
#
# The goal is defined as:
#
# -------------
# | 1 | 2 | 3 |
# -------------
# | 4 | 5 | 6 |
# -------------
# | 7 | 8 | 0 |
# -------------
#
# Where 0 denotes the blank tile or space.
goal_state = [1, 4, 7, 2, 5, 8, 3, 6, 0]
#

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
	print "\n"
	
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

def expand_node( node ):
	"""Returns a list of expanded nodes"""
	expanded_nodes = []
	if node.operator == "r":
		expanded_nodes.append( create_node( move_up( node.state ), node, "u", node.depth + 1, 0 ) )
		expanded_nodes.append( create_node( move_down( node.state ), node, "d", node.depth + 1, 0 ) )
		expanded_nodes.append( create_node( move_right( node.state ), node, "r", node.depth + 1, 0 ) )
	elif node.operator == "l":
		expanded_nodes.append( create_node( move_up( node.state ), node, "u", node.depth + 1, 0 ) )
		expanded_nodes.append( create_node( move_down( node.state ), node, "d", node.depth + 1, 0 ) )
		expanded_nodes.append( create_node( move_left( node.state ), node, "l", node.depth + 1, 0 ) )
	elif node.operator == "d":
		expanded_nodes.append( create_node( move_down( node.state ), node, "d", node.depth + 1, 0 ) )
		expanded_nodes.append( create_node( move_left( node.state ), node, "l", node.depth + 1, 0 ) )
		expanded_nodes.append( create_node( move_right( node.state ), node, "r", node.depth + 1, 0 ) )
	elif node.operator == "u":
		expanded_nodes.append( create_node( move_up( node.state ), node, "u", node.depth + 1, 0 ) )
		expanded_nodes.append( create_node( move_left( node.state ), node, "l", node.depth + 1, 0 ) )
		expanded_nodes.append( create_node( move_right( node.state ), node, "r", node.depth + 1, 0 ) )		
	# Filter the list and remove the nodes that are impossible (move function returned None)
	else:
		expanded_nodes.append( create_node( move_up( node.state ), node, "u", node.depth + 1, 0 ) )
		expanded_nodes.append( create_node( move_down( node.state ), node, "d", node.depth + 1, 0 ) )
		expanded_nodes.append( create_node( move_left( node.state ), node, "l", node.depth + 1, 0 ) )
		expanded_nodes.append( create_node( move_right( node.state ), node, "r", node.depth + 1, 0 ) )		
	expanded_nodes = [node for node in expanded_nodes if node.state != None] #list comprehension!
	return expanded_nodes

def dfs( start, goal, depth=10): #NOTE --> The value of depth is set to 10 for depth limit search, remove it for normal DFS.
	"""Performs a depth first search from the start state to the goal. Depth param is optional."""
	depth_limit = depth
	# A list (can act as a stack too) for the nodes.
	nodes = []
	# Create the queue with the root node in it.
	nodes.append( create_node( start, None, None, 0, 0 ) )
	#display_board(start)
	while True:
		# We've run out of states, no solution.
		if len( nodes ) == 0: return None
		# take the node from the end of the queue
		#NOTE --> change the below function to pop(0) for BFS
		node = nodes.pop()
		display_board(node.state)
		# if this node is the goal, return the moves it took to get here.
		if node.state == goal:
			moves = []
			sol=[]
			temp = node
			while True:
				moves.insert(0, temp.operator)
				sol.insert(0,temp.state)
				if temp.depth <= 1: break
				temp = temp.parent
			return moves, sol			
		# Add all the expansions to the beginning of the stack if we are under the depth limit
		if node.depth < depth_limit:
			nodes.extend( expand_node( node) )

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
	starting_state=[2, 1, 7, 0, 4, 5, 3, 6, 8]
	#r.shuffle(starting_state)
	moves, result = dfs( starting_state, goal_state )
	if result == None:
		print "No solution found"
	elif result == [None]:
		print "Start node was the goal!"
	else:
		#print result
		print "Initial state: "
		display_board(starting_state)
		print "Goal state: "
		display_board(goal_state)
		print "Solution: "
		for i in result:
			display_board(i)
		print moves
		print len(result), " moves"

if __name__ == "__main__":
	main()
