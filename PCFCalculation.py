import pandas as pd
import numpy as np
import constants

def calculatePCF(PCF_df,pop_df):

    index_cap = min(constants.AGE+constants.YEARS, constants.AGE+constants.CALC_YEARS, constants.MAXAGE)
    size_cap = min(constants.YEARS, constants.CALC_YEARS, constants.MAXAGE-constants.AGE)

    # filenames = ['./cash_flow/PCF.csv','./pop/population.csv']
    # BCF = []
    # for fn in filenames:
    #     BCF.append(pd.read_csv(fn))

    BCF = [PCF_df, pop_df]

    # idle cash flow code
    exp_premium = pd.DataFrame()
    for name in BCF[0].columns:
        exp_premium[name] = (BCF[1][name][0:size_cap]*BCF[0][name][0:size_cap].values)
    exp_premium['Total'] = exp_premium.sum(axis=1)

    # export to csv
    exp_premium.insert(loc=0, column='Age', value=np.arange(constants.AGE, index_cap))
        # for later: exp_premium.index.name='Agee'
    exp_premium.to_csv('./cash_flow/exp_premium.csv', index=False, float_format='%.6f')
