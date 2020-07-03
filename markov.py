import pandas as pd
import numpy as np
import constants

class EdgeType:
    value = 0
    is_csv = False
    def __init__(self, v, ic):
        self.value = v
        self.is_csv = ic

def calculateMarkov(nodenames, filenames):
    MAXNODE = constants.MAXNODE
    MAXAGE = constants.MAXAGE
    AGE = constants.AGE
    YEARS = constants.YEARS
    GENDER = constants.GENDER

    # node names
    #HSD =  ['H', 'S', 'D']
    HSD = nodenames
    # csv filenames
    #filenames = ['./pop/HD.csv','./pop/HS.csv','./pop/SD.csv','./pop/SH.csv']

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
        ('S','H'): EdgeType(3, True),
        ('S','D'): EdgeType(2, True),
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
                if AGE+pop_counter <= MAXAGE:
                    subsum_incr = my_csv[temp_EdgeType.value]['Rate'][AGE+pop_counter]
                else:
                    subsum_incr = my_csv[temp_EdgeType.value]['Rate'][MAXAGE]
            else:
                subsum_incr = temp_EdgeType.value
            subsum += subsum_incr

            temp_EdgeType = edges[(HSD[(node_index+i)%MAXNODE],HSD[node_index])]
            if (temp_EdgeType.is_csv):
                #checking for index out of bound cases
                if AGE+pop_counter <= MAXAGE:
                    addsum_incr = pop[pop_counter][(node_index+i)%MAXNODE]*my_csv[temp_EdgeType.value]['Rate'][AGE+pop_counter]
                else:
                    addsum_incr = pop[pop_counter][(node_index+i)%MAXNODE]*my_csv[temp_EdgeType.value]['Rate'][MAXAGE]
            else:
                addsum_incr = pop[pop_counter][(node_index+i)%MAXNODE]*temp_EdgeType.value
            pop_change[node_index][pop_counter][i-1] = addsum_incr
            addsum += addsum_incr
        #final formula after calculating subsum and addsum
        return round(pop[pop_counter][node_index]*(1-subsum)+addsum,6)

    #init our array for storing population
    pop = np.zeros((min(YEARS, MAXAGE-AGE)+1,MAXNODE))
    #hardcoded, have to change later?
    pop[0] = [1.0,0,0]

    #init array for population_change
    pop_change = np.zeros((MAXNODE,min(YEARS, MAXAGE-AGE), MAXNODE-1))

    for i in range(min(YEARS, MAXAGE-AGE)):
        updatePop(i, pop, edges)

    #save pop to csv
    #savetxt('population-new.csv', pop, delimiter=',', fmt='%.3f')
    pop_df = pd.DataFrame(pop, columns = HSD)
    pop_df.insert(loc=0, column='Age', value=np.arange(AGE,min(AGE+YEARS,MAXAGE)+1))
        # for later: pop_df.index = np.arange(AGE,min(AGE+YEARS,MAXAGE)+1)
        # for later: pop_df.index.name='Agee'
    pop_df.to_csv('./pop/population.csv', index=True, float_format='%.6f')

    #saving pop_change to csv
    pop_change_df = pd.DataFrame()
    for i in range(MAXNODE):
        for j in range(MAXNODE-1):
            pop_change_df[HSD[(i+j+1)%MAXNODE]+'->'+HSD[i]] = pd.Series(pop_change[i,:,j])

    pop_change_df.insert(loc=0, column='Age', value=np.arange(AGE,min(AGE+YEARS,MAXAGE)))
    pop_change_df.to_csv('./pop/population_delta.csv', index=False, float_format='%.6f')
    return (pop_df, pop_change_df)
