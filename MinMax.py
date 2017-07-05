class Node:
	def __init__(self, state = None, parent = None, children = None):
		self.state = state
		self.parent = parent
		self.children = children if children else []
		self.marks = None
	
	def add_child(self, child):
		self.children.append(child)

	def pchild(self):
		ch = ""
		for c in self.children:
			ch += " " + c.state
		return ch

	def __str__(self, level = 0):
		n = len(self.children)
		ret = "|\t"*max(0, level - 1) + "|-------"*(1 if level > 0 else 0) +repr(self)+"\n"
		for i, child in enumerate(self.children):
			ret += child.__str__(level + 1)
		return ret

	def __repr__(self):
		return str(self.state) + " " + str(self.marks)


def gen_game_tree(state = (1, 8), agent = False):
	curr = Node(state)
	curr.marks = -1 if agent else 1
	if state == (1, 2):
		return curr
	for num in state:
		if not num in (1, 2):
			for x in range(1, num // 2 + 1):
				if num - x == x:
					break
				child = gen_game_tree((x, num - x), not agent)
				child.parent = curr
				curr.add_child(child)
				curr.marks = child.marks if child.marks == (1 if agent else -1) else curr.marks
	return curr

def choose(root):
	for c in root.children:
		if c.marks == 1:
			return c
	return root.children[0]

def player_turn(root):
	print("Player:-")
	k=raw_input()
	st = tuple(list(map(int, k.rstrip().replace(" ", "").split(","))))
	for c in root.children:
		if c.state == st:
			return c
	print("Invalid Move.... Retry.... Dumbfuck ;)")
		
	return False


root = gen_game_tree(state = (1, 8))
print(root)

print("Game started")
r = root
i = 0
while(i >= 0):
	if i % 2 == 0:
		r = choose(r)
		print("PC:- " + str(r.state))
		i += 1
	else: 
		t = player_turn(r)
		if t:
			r = t
			i += 1
		else:
			continue
	if r.state == (1, 2):
		if i % 2 == 0:
			print "PC Wins"
		else:
			print "Player Wins"
		break
