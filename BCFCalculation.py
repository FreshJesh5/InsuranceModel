import pandas as pd
import numpy as np
import constants

def calculateBCF():
    filenames = ['./cash_flow/BCFIdle.csv','./cash_flow/BCFChange.csv', './pop/population.csv','./pop/population_delta.csv']
    index_cap = min(constants.AGE+constants.YEARS,constants.MAXAGE)
    BCF = []

    for fn in filenames:
        BCF.append(pd.read_csv(fn))

    # idle cash flow code
    exp_benefit_idle = pd.DataFrame()
    for name in BCF[0].columns:
        exp_benefit_idle[name] = (BCF[2][name]*BCF[0][name][constants.AGE:index_cap+1].values)
    exp_benefit_idle['Total'] = exp_benefit_idle.sum(axis=1)
    # change cash flow code
    exp_benefit_change = pd.DataFrame()
    for name in BCF[1].columns:
        exp_benefit_change[name] = (BCF[3][name]*BCF[1][name][constants.AGE:index_cap].values)
    exp_benefit_change['Total'] = exp_benefit_change.sum(axis=1)

    # export to csv
    exp_benefit_idle.insert(loc=0, column='Age', value=np.arange(constants.AGE, index_cap+1))
        # for later: exp_benefit_idle.index.name='Agee'
    exp_benefit_idle.to_csv('./cash_flow/exp_benefit_idle.csv', index=False, float_format='%.6f')

    exp_benefit_change.insert(loc=0, column='Age', value=np.arange(constants.AGE,index_cap))
    exp_benefit_change.to_csv('./cash_flow/exp_benefit_delta.csv', index=False, float_format='%.6f')
