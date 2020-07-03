import pandas as pd
from numpy import savetxt
import numpy as np

#input parameters
MAXNODE = 3
MAXAGE = 100
AGE = 10
YEARS = 100
GENDER = 'Male'

# node names
HSD =  ['H', 'S', 'D']
# csv filenames
filenames = ['HDGender.csv','HS.csv']

class EdgeType:
    value = 0
    is_csv = False
    def __init__(self, v, ic):
        self.value = v
        self.is_csv = ic

# using index as age for now, will have to change later
my_csv = []
for fn in filenames:
    temp_df = pd.read_csv(fn)
    if 'Rate' in temp_df.columns:
        my_csv.append(temp_df)
    else:
        my_csv.append(pd.concat([temp_df['Age'],temp_df[GENDER].rename('Rate')],axis=1))

edges = {
    ('H','S'): EdgeType(1, True),
    ('H','D'): EdgeType(0, True),
    ('S','H'): EdgeType(0.95, False),
    ('S','D'): EdgeType(0.1, False),
    ('D','S'): EdgeType(0.0, False),
    ('D','H'): EdgeType(0.0, False)
}

#generate the rows for population csv iterativetly
def updatePop(counter, pop, edges):
    #for each node
    for i in range(0,MAXNODE):
        pop[counter+1][i] = iteratePop(i, pop, counter, edges)


#helper for updatePop
def iteratePop(node_index, pop, pop_counter, edges):
    subsum = 0
    addsum = 0
    subsum_incr = 0
    addsum_incr = 0
    for i in range(1,MAXNODE):
        # for reference: orginal formula that used values instead of tables:
        # subsum += edges[(HSD[node_index],HSD[(node_index+i)%MAXNODE])]
        # addsum += pop[pop_counter][(node_index+i)%MAXNODE]*edges[(HSD[(node_index+i)%MAXNODE],HSD[node_index])]
        temp_EdgeType = edges[(HSD[node_index],HSD[(node_index+i)%MAXNODE])]
        if (temp_EdgeType.is_csv):
            #checking for index out of bound cases
            if AGE+pop_counter <= 100:
                subsum_incr = my_csv[temp_EdgeType.value]['Rate'][AGE+pop_counter]
            else:
                subsum_incr = my_csv[temp_EdgeType.value]['Rate'][MAXAGE]
        else:
            subsum_incr = temp_EdgeType.value
        subsum += subsum_incr

        temp_EdgeType = edges[(HSD[(node_index+i)%MAXNODE],HSD[node_index])]
        if (temp_EdgeType.is_csv):
            #checking for index out of bound cases
            if AGE+pop_counter <= 100:
                addsum_incr = pop[pop_counter][(node_index+i)%MAXNODE]*my_csv[temp_EdgeType.value]['Rate'][AGE+pop_counter]
            else:
                addsum_incr = pop[pop_counter][(node_index+i)%MAXNODE]*my_csv[temp_EdgeType.value]['Rate'][MAXAGE]
        else:
            addsum_incr = pop[pop_counter][(node_index+i)%MAXNODE]*temp_EdgeType.value
        addsum += addsum_incr
    #final formula after calculating subsum and addsum
    return round(pop[pop_counter][node_index]*(1-subsum)+addsum,5)

#init our array for storing population
pop = np.zeros((YEARS+1,MAXNODE))
pop[0] = [100,0,0]

#init array for population_change
pop_change = np.zeros((YEARS+1, MAXNODE*2))

for i in range(YEARS):
    updatePop(i, pop, edges)

#save to csv
#savetxt('population-new.csv', pop, delimiter=',', fmt='%.3f')
column_names = ['H','S','D']
pop_df = pd.DataFrame(pop, columns = column_names)
pop_df.insert(loc=0, column='Age', value=np.arange(AGE,AGE+YEARS+1))
pop_df.to_csv('population.csv', index=False, float_format='%.3f')
