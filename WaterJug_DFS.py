#!/usr/bin/python

import sys
import random as r

def display_state(state):
	print "[",state[0],", ",state[1],"]"
	
def fill_first( state ):
	new_state=state[:]
	new_state[0]=n1
	return new_state

def fill_second(state):
		new_state=state[:]
		new_state[1]=n2
		return new_state

def empty_first(state):
	new_state=state[:]
	new_state[0]=0
	return new_state
	
def empty_second(state):
		new_state=state[:]
		new_state[1]=0
		return new_state

def first_2_second(state):
	new_state=state[:]
	while new_state[1]!=n2:
		if new_state[0]>'0':
			new_state[0]=str(int(new_state[0])-1)
			new_state[1]=str(int(new_state[1])+1)
		else:
			break
	return new_state
	
def second_2_first(state):
	new_state=state[:]
	while new_state[0]!=n1:
		if new_state[1]>'0':
			new_state[1]=str(int(new_state[1])-1)
			new_state[0]=str(int(new_state[0])+1)
		else:
			break
	return new_state

def allfirst_2_second(state):
	new_state=state[:]
	new_state[0]='0'
	new_state[1]=str(int(state[0])+int(state[1]))
	if new_state[1]>n2:
		new_state[1]=n2
	return new_state

def allsecond_2_first(state):
	new_state=state[:]
	new_state[1]='0'
	new_state[0]=str(int(state[0])+int(state[1]))
	if new_state[0]>n1:
		new_state[0]=n1
	return new_state
	
def create_node( state, parent, operator, depth, cost ):
	return Node( state, parent, operator, depth, cost )

def expand_node( node, openlist, closedlist):
	"""Returns a list of expanded nodes"""
	val=[]
	expanded_nodes = []
	if node.operator=="Initial":
		expanded_nodes.append( create_node( fill_first( node.state ), node, "Fill first jug until full", node.depth + 1, 0 ) )
		expanded_nodes.append( create_node( fill_second( node.state ), node, "Fill second jug until full", node.depth + 1, 0 ) )
	else:
		expanded_nodes.append( create_node( fill_first( node.state ), node, "Fill first jug until full", node.depth + 1, 0 ) )
		expanded_nodes.append( create_node( fill_second( node.state ), node, "Fill second jug until full", node.depth + 1, 0 ) )
		expanded_nodes.append( create_node( empty_first( node.state ), node, "Empty first jug", node.depth + 1, 0 ) )
		expanded_nodes.append( create_node( empty_second( node.state ), node, "Empty second jug", node.depth + 1, 0 ) )
		expanded_nodes.append( create_node( first_2_second( node.state ), node, "Pour water from first jug to second jug", node.depth + 1, 0 ) )
		expanded_nodes.append( create_node( second_2_first( node.state ), node, "Pour water from second jug to first jug", node.depth + 1, 0 ) )
		expanded_nodes.append( create_node( allfirst_2_second( node.state ), node, "Pour all water from first jug to second jug", node.depth + 1, 0 ) )
		expanded_nodes.append( create_node( allsecond_2_first( node.state ), node, "Pour all water from second jug to first jug ", node.depth + 1, 0 ) )
	for i in openlist:
			val.append(i.state)
	for j in closedlist:
			val.append(j.state)
	expanded_nodes = [node for node in expanded_nodes if node.state not in val] #list comprehension!
	return expanded_nodes

def dfs( start, goal, depth=10): #NOTE --> The value of depth is set to 10 for depth limit search, remove it for normal DFS.
	"""Performs a depth first search from the start state to the goal. Depth param is optional."""
	depth_limit = depth
	flag=0
	closedlist=[]
	# A list (can act as a stack too) for the nodes.
	nodes = []
	# Create the queue with the root node in it.
	nodes.append( create_node( start, None,"Initial", 0, 0 ) )
	#display_board(start)
	print "Traversal: "
	while True:
		# We've run out of states, no solution.
		if len( nodes ) == 0: return None
		# take the node from the end of the queue
		#NOTE --> change the below function to pop(0) for BFS
		node = nodes.pop(0)
		closedlist.append(node)
		display_state(node.state)
		# if this node is the goal, return the moves it took to get here.
		if node.depth < depth_limit:
			for k in expand_node( node, nodes, closedlist ):
				# if this node is the goal, return the moves it took to get here.
				if k.state==goal:
					flag=1
					node=k
					break
				elif goal[0]=='*' and k.state[1]==goal[1]:
					flag=1
					node=k
					break
				elif goal[1]=='*' and k.state[0]==goal[0]:
					flag=1
					node=k
					break
				else:
				# Add all the expansions to the beginning of the stack if we are under the depth limit
					nodes.append( k )
		if flag==1:
			display_state(node.state)
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
			nodes.extend( expand_node( node, nodes, closedlist) )

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

starting_state=[0,0]
n1=raw_input('Enter the capacity of first jug: ')
n2=raw_input('Enter the capacity of second jug: ')
print "-----Enter Goal value------"
o1=raw_input('First jug (Enter * for any value):  ')
o2=raw_input('Second jug (Enter * for any value) :  ')
goal_state=[o1,o2]
moves, result = dfs( starting_state, goal_state )
if result == None:
	print "No solution found"
elif result == [None]:
	print "Start node was the goal!"
else:
	#print result
	print "Initial state: "
	display_state(starting_state)
	print "Goal state: "
	display_state(goal_state)
	print "Solution: "
	for i in result:
		display_state(i)
	for i in moves:
		print i,"-->",
	print "\n",len(result), " moves"


