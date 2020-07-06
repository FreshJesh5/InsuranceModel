import pandas as pd
import numpy as np
import constants

def calculateActualValue(interest_df):
    # interest_df = pd.read_csv(filename)
    interest = interest_df['Interest'].to_numpy()
    actual_value = np.zeros(len(interest))
    #print(len(actual_value))
    actual_value[0] = 1.0
    for i in range(1,len(actual_value)):
        actual_value[i] = actual_value[i-1]/(1+interest[i-1])
    interest_df['Actual Value']=pd.Series(actual_value)
    #print(interest_df)
    return interest_df

def calculatePPV(EP_df, interest_df):
    size_cap = min(constants.YEARS, constants.CALC_YEARS, constants.MAXAGE-constants.AGE)
    # EP_df = pd.read_csv('./cash_flow/exp_premium.csv')
    # interest_df = calculateActualValue('./cash_flow/interest.csv')
    output = ((EP_df['Total']*interest_df['Actual Value'][0:size_cap].values)).sum()
    # print(interest_df['Actual Value'])
    # print(EP_df['Total'])
    # print((EP_df['Total']*interest_df['Actual Value'][0:size_cap].values))
    return output

def calculateBPV(EBI_df, EBD_df, interest_df):
    size_cap = min(constants.YEARS, constants.MAXAGE-constants.AGE)
    # EBI_df = pd.read_csv('./cash_flow/exp_benefit_idle.csv')
    # EBD_df = pd.read_csv('./cash_flow/exp_benefit_delta.csv')
    # interest_df = calculateActualValue('./cash_flow/interest.csv')
    output = ((EBI_df['Total']+EBD_df['Total'])*interest_df['Actual Value'][0:size_cap+1].values).sum()
    return output

def calculateNP(BPV,PPV):
    return BPV/PPV

def calculateGP(NP,expense_loading):
    # NP = calculateNP()
    return NP/(1-expense_loading)

#print(calculateGP(constants.EXPENSE_LOADING))
