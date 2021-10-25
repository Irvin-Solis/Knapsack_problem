
import random

# creates list of pairs from file 
def convertFile(file, lst):
  f = open(file, "r")
  for x in f:
    arr = list(map(float, x.split()))
    lst.append((arr[0], arr[1]))

#record avg ftns in output.txt
def recordFtness(fit):
  global ten_gen, max_fit, avg_fit
  if(len(ten_gen) < 2):
    ten_gen.append(fit)
  else:
    ten_gen[0] = ten_gen[1]
    ten_gen[1] = fit
  avg_fit = fit
  if (fit > max_fit):
    max_fit = fit
  f = open("output.txt", "a")
  f.write(str(fit))
  f.write("\n")
  f.close

# select rand item to add
def selecItem(lst):
  randnum = random.randrange(0, 399)
  if not(lst[randnum]):
    lst[randnum] = True
  else:
    selecItem(lst)
  

# selection for init pop
def selection():
  lst = MYBITLIST.copy()
  for x in range(20):
    selecItem(lst)
  return lst

# starting of 1st gen
def init_pop(pop, lst):
  fit = []
  for x in range(pop):
    select = selection()
    lst.append(select)
    fit.append(find_ftness(select))
  ftn_avg = findAvgFit(fit)
  recordFtness(ftn_avg)
  

# find list utility/fitness
def find_ftness(lst):
  total_f = 0
  total_w = 0
  for x in range(len(lst)):
    if (lst[x]):
      total_f += myItems[x][0]
      total_w += myItems[x][1]
  
  if(total_w >= 500):
    total_f = 1
  return total_f

# find avg fitness for gen
def findAvgFit(lst):
  return sum(lst) / len(lst)

# chance of mutation is 1/10000
def chance_mut():
  chance = random.randrange(1, 10000)
  if (chance == 1):
    return True
  return False

# create cdf list
def create_cdf(fitLst):
  for x in range(len(fitLst) -1):
    fitLst[x + 1] += fitLst[x]

# L2 normalization
def normalization(lst):
  total = sum(lst)
  for x in range(len(lst)):
    lst[x] = lst[x] / total
  create_cdf(lst)

def mutation(mainLst, fitLst, pop):
  fit = []
  for lst in mainLst:
    for x in range(len(lst)):
      mutate = chance_mut()
      if (mutate):
        if (lst[x]):
          lst[x] = False
        elif (lst[x] == False):
          lst[x] = True

    fitness = find_ftness(lst)
    fitLst.append(fitness **2) #squaring for L2 norm
    fit.append(fitness)
    
  # find avg fitenss for gen and record it in outout.txt
  ftn_avg = findAvgFit(fit)
  recordFtness(ftn_avg)

  # begin cross breeding for next generation
  normalization(fitLst)
  reproduce(fitLst, mainLst, pop)

def find_parent(parent, lst):
  for x in range(len(lst)):
    if (lst[x] > parent):
      return x

def create_offspring(parent_1, parent_2, myList):
  rand_index = random.randrange(0, 399)

  parent_1_gene = myList[parent_1][:rand_index]
  parent_2_gene = myList[parent_2][rand_index:]

  child = parent_1_gene + parent_2_gene
  return child

def reproduce(lst, mainLst, pop):
  new_gen = []
  for x in range(pop):
    parent_1 = find_parent(random.random(), lst)
    parent_2 = find_parent(random.random(), lst)

    offspring = create_offspring(parent_1, parent_2, mainLst)
    new_gen.append(offspring)
  global myList 
  myList = new_gen

def check_improvement(lst):
  imp = 0
  for x in range(9):
    diff = lst[x + 1] - lst[x]
    change = (diff / lst[x]) * 100
    imp += change
  if(imp < 1):
    global stop
    stop = True
  print("Improved: ", imp, "%")

def check(lst):
  diff = lst[1] - lst[0]
  change = (diff / lst[0]) * 100
  global stop
  if(change < 1):
    stop+=1
  else:
    stop = 0
  print("Improved: ", change, "%")

# main program
# list for gen fitness and cdf
myFit = []
# item list
myItems = []
# population/generation, myList of lis
myList = []
# const list of bool to repr selection
MYBITLIST = [False]*400

# myItem => (utility, weight)
convertFile("list.txt", myItems)
ten_gen = []
max_fit = 0
avg_fit = 0
pop = int(input("What is the population?\n"))

# init population and create 1st gen
init_pop(1000, myList)

gen = 1
stop = 0
while(stop < 10):
  gen += 1
  mutation(myList, myFit, pop)
  myFit.clear()
  check(ten_gen)

print("Starting population: ", pop, "\n")
print("Max fitness after ", gen, " generations: ", max_fit)
print("Average fitness: ", avg_fit)