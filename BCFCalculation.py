import pandas as pd
import numpy as np
import constants
from logger import logCSV

def calculateBCF(BCFIdle_df, BCFDelta_df, pop_df, pop_delta_df):
    # filenames = ['./cash_flow/BCFIdle.csv','./cash_flow/BCFDelta.csv', './pop/population.csv','./pop/population_delta.csv']
    # BCF = []
    # for fn in filenames:
    #     BCF.append(pd.read_csv(fn))
    index_cap = min(constants.AGE+constants.YEARS,constants.MAXAGE)
    inputs = [BCFIdle_df, BCFDelta_df, pop_df, pop_delta_df]



    # idle cash flow code
    exp_benefit_idle = pd.DataFrame()
    for name in inputs[0].columns:
        exp_benefit_idle[name] = (inputs[2][name]*inputs[0][name][constants.AGE:index_cap+1].values)
    exp_benefit_idle['Total'] = exp_benefit_idle.sum(axis=1)
    # change cash flow code
    exp_benefit_delta = pd.DataFrame()
    for name in inputs[1].columns:
        exp_benefit_delta[name] = (inputs[3][name]*inputs[1][name][constants.AGE:index_cap+1].values)
    exp_benefit_delta['Total'] = exp_benefit_delta.sum(axis=1)

    # export to csv
    #exp_benefit_idle.insert(loc=0, column='Age', value=np.arange(constants.AGE, index_cap+1))
    exp_benefit_idle.to_csv(constants.savepath + constants.expected_benefit_idle, index=True, float_format='%.6f')
    # exp_benefit_delta.insert(loc=0, column='Age', value=np.arange(constants.AGE,index_cap))
    exp_benefit_delta.to_csv(constants.savepath + constants.expected_benefit_delta, index=True, float_format='%.6f')

    logCSV("Expected Benefit Idle", constants.savepath + constants.expected_benefit_idle)
    logCSV("Expected Benefit Delta", constants.savepath + constants.expected_benefit_delta)

    return (exp_benefit_idle, exp_benefit_delta)
