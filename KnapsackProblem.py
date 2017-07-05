import random
import math
import collections
w = [] # Stores weights of the items
b=[] # Stores profit gained by each item
population=collections.OrderedDict() # To store set of solutions after each iteration 
sol=[] # Stores individual solution
valid=collections.OrderedDict() # From the set of solutions, it stores the valid ones (Total<=M)
selected=collections.OrderedDict() # Stores the solutions chosen for cross breed
n = raw_input('Enter the total number of elements: ') 
m = raw_input('Enter the capacity of Knapsack: ')

def displaySolution(solution):
	print "__________________________________________________________________________________"
	print "{:<15} {:<15} {:<15} {:<15}".format('Solution','Total weight','Profit','Validity')
	print "__________________________________________________________________________________\n"
	for k, v in solution.iteritems():
		soltn, wt, prft, val = v
		print "{:<15} {:<15} {:<15} {:15}".format( soltn, wt, prft, val)
	
# Checks for valid solution set		
def validCheck(toCheck):
	total=0
	for i in range(len(toCheck)):
		if int(toCheck[i])==1:
			total=total+int(w[i])
	if total > int(m):
		return 'invalid',total
	else:
		return 'valid',total 
		
# Calculates profit for each solution set
def calculateProfit(toCheck):
	total=0
	for i in range(len(toCheck)):
		if int(toCheck[i])==1:
			total=total+int(b[i])
	return total

# Generates random population initially depending upon the value of N and size of population given by the user (maximum size=2^N)
def initPopulation(rangep,size):
	p = random.sample(xrange(rangep), size) 
	for i in range(len(p)):
		individual=[]
		p[i]=str(bin(int(p[i]))[2:].zfill(int(n)))
	return p
	
# Selects solutions from the valid ones for cross breed depending upon the profit gained by each solution (decreasing order of profit)
def select(pop):
	for i in pop.keys():
		if pop[i][3]=='valid':
			valid.update({i:pop[i]})
	for key, value in sorted(valid.items(), key=lambda e: e[1][2], reverse=True):
		selected.update({key:value})
		k=key
	if len(selected)%2 != 0:
		selected.pop(k)
	print '\n--------SELECTED POPULATION--------\n'
	displaySolution(selected)
	return selected		
	
# Generates new solutions from the selectetd solutions. The selection point is obtained by N/2
def crossover(selectedPop):
	print '\n--------AFTER CROSSOVER--------\n'
	indexlist=selectedPop.keys()
	children=[]
	for i in xrange(0,len(selectedPop)-1,2):
		parent1= selectedPop.values()[i]
		parent2= selectedPop.values()[i+1]
		print 'Parent1: ',parent1[0]
		print 'Parent2: ',parent2[0]
		crosspoint=int(math.ceil(len(parent1[0])/2))
		child=parent1[0][0:crosspoint]+parent2[0][crosspoint:]
		print 'Child1: ',child
		child=mutation(child)
		print 'Child1 (After mutation): ',child
		children.append(child)
		child=parent2[0][0:crosspoint]+parent1[0][crosspoint:]
		print 'Child2: ',child
		child=mutation(child)
		print 'Child2 (After mutation): ',child
		children.append(child)
		print '________________________'
	return children,indexlist
	
# Introduces new feature in the child by inverting any random bit	
def mutation(child):
	r=random.randint(0,len(child)-1)
	if child[r] == '1':
		child=child[0:r]+'0'+child[r+1:]
	else:
		child=child[0:r]+'1'+child[r+1:]
	return child
	
	
# Checks whether the child is better than parent or not. If yes, then the parent is replaced by child	
def replace(nl,id):
	for i in xrange(0,len(nl)-1,2):
		parentkey=id[i]
		newv,wgt=validCheck(nl[i])
		newp=calculateProfit(nl[i])
		if newv== 'valid' and newp>population[parentkey][2]:
			population.update({parentkey:[nl[i],wgt,newp,newv]})
		parentkey=id[i+1]
		if newv== 'valid' and newp>population[parentkey][2]:
			population.update({parentkey:[nl[i],wgt,newp,newv]})
		parentkey=id[i]
		newv,wgt=validCheck(nl[i+1])
		newp=calculateProfit(nl[i+1])
		if newv== 'valid' and newp>population[parentkey][2]:
			population.update({parentkey:[nl[i],wgt,newp,newv]})
		parentkey=id[i+1]
		if newv== 'valid' and newp>population[parentkey][2]:
			population.update({parentkey:[nl[i+1],wgt,newp,newv]})
	
# Selects the optimal solution depending upon profit gained from the population after 2 iterations	
def findOptimal():
	max=0
	for v in population.values():
		if v[3] == 'valid' and int(v[2])>int(max):
			max=v[2]
			opt=v
	if opt==None:
		print '\n--------NO SOLUTION FOUND--------\n'
	else:
		print '\n--------SOLUTION--------\n'
		print 'Solution: ',opt[0],'\nTotal weight: ',opt[1],'\nProfit gained: ',opt[2]
		
print '\n--------WEIGHTS--------\n'
for i in range(int(n)):
	print 'Enter the weight of element ',i+1,' :'
	t=raw_input()
	w.append(t)
print '\n--------PROFITS--------\n'
for i in range(int(n)):
	print 'Enter the value of element ',i+1,' :'
	t=raw_input()
	b.append(t)
max_size=int(math.pow(2.0,float(n)))
print 'Enter the size of initial population (1-',max_size,') :'
s = int(raw_input())
if s<1 or s>max_size:
	raise ValueError('Invalid population size, cannot create unique individuals')
print '\n--------INITIAL POPULATION--------\n'
sol=initPopulation(max_size,s)
for i in range(len(sol)):
	v,weight=validCheck(sol[i])
	p=calculateProfit(sol[i])
	population.update({i:[sol[i],weight,p,v]})
displaySolution(population)
for i in range(2):
	print '\n*****ITERATION',i+1,'******\n'
	new,indexl=crossover(select(population))
	replace(new,indexl)
	print '\n--------AFTER ITERATION',i+1,'--------\n'
	displaySolution(population)
findOptimal()


