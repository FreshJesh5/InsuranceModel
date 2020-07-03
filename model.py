import pandas as pd
import numpy as np
import constants
from PCFCalculation import calculatePCF
from BCFCalculation import calculateBCF
from markov import calculateMarkov
import valueCalculation

HSD =  ['H', 'S', 'D']
filenames = ['./pop/HD.csv','./pop/HS.csv','./pop/SD.csv','./pop/SH.csv']

(pop_df, pop_change_df) = calculateMarkov(HSD,filenames)
PCF_df = pd.read_csv('./cash_flow/PCF.csv')
calculatePCF(PCF_df,pop_df)


calculateBCF()
print(valueCalculation.calculateGP(constants.EXPENSE_LOADING))
