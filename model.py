import pandas as pd
import numpy as np
import constants
from PCFCalculation import calculatePCF
from BCFCalculation import calculateBCF
from markov import calculateMarkov
import valueCalculation
from logger import printFormat


# markov inputs
HSD =  ['H', 'S', 'D']
filenames = ['./pop/HD.csv','./pop/HS.csv','./pop/SD.csv','./pop/SH.csv']
# inputs for the rest of the steps
BCFIdle_df = pd.read_csv('./cash_flow/BCFIdle.csv')
BCFDelta_df = pd.read_csv('./cash_flow/BCFDelta.csv')
interest_df = pd.read_csv('./cash_flow/interest.csv')

(pop_df, pop_delta_df) = calculateMarkov(HSD,filenames)

(EBI_df, EBD_df) = calculateBCF(BCFIdle_df, BCFDelta_df, pop_df, pop_delta_df)
interest_df = valueCalculation.calculateActualValue(interest_df)

PCF_df = pd.read_csv('./cash_flow/PCF.csv')
EP_df = calculatePCF(PCF_df,pop_df)

# print(pop_df)
# print(pop_delta_df)
# print(EP_df)
# print(EBI_df)
# print(EBD_df)

BPV = valueCalculation.calculateBPV(EBI_df, EBD_df, interest_df)
PPV = valueCalculation.calculatePPV(EP_df, interest_df)
NP = valueCalculation.calculateNP(BPV,PPV)
GP = valueCalculation.calculateGP(NP, constants.EXPENSE_LOADING)

printFormat("Premium Present Value", PPV)
printFormat("Benefit Present Value", BPV)
printFormat("Net Premium", NP)
printFormat("Gross Premium", GP)
