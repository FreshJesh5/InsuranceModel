import pandas as pd
import numpy as np
import constants

def calculateActualValue(filename):
    interest_df = pd.read_csv(filename)
    interest = interest_df['Interest'].to_numpy()
    actual_value = np.zeros(len(interest))
    #print(len(actual_value))
    actual_value[0] = 1.0
    for i in range(1,len(actual_value)):
        actual_value[i] = actual_value[i-1]/(1+interest[i-1])
    interest_df['Actual Value']=pd.Series(actual_value)
    #print(interest_df)
    return interest_df

def calculatePPV():
    EP = pd.read_csv('./cash_flow/exp_premium.csv')
    interest_df = calculateActualValue('./cash_flow/interest.csv')
    output = (interest_df['Actual Value']*(EP['Total'])).sum()
    return output

def calculateBPV():
    EBI = pd.read_csv('./cash_flow/exp_benefit_idle.csv')
    EBC = pd.read_csv('./cash_flow/exp_benefit_delta.csv')
    interest_df = calculateActualValue('./cash_flow/interest.csv')
    output = (interest_df['Actual Value']*(EBI['Total']+EBC['Total'])).sum()
    return output


def calculateNP():
    return calculateBPV()/calculatePPV()

def calculateGP(expense_loading):
    NP = calculateNP()
    return NP/(1-expense_loading)

#print(calculateGP(constants.EXPENSE_LOADING))
