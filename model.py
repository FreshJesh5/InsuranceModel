import pandas as pd
import numpy as np
import constants
import os
from PCFCalculation import calculatePCF
from BCFCalculation import calculateBCF
from markov import calculateMarkov
import valueCalculation
from logger import printFormat

def runModel(**kwargs):
    constants.AGE = kwargs.get('age', 10)
    constants.MAXAGE = kwargs.get('maxage', 110)
    constants.YEARS = kwargs.get('years', 100)
    constants.CALC_YEARS = kwargs.get('calc_years', 20)
    constants.EXPENSE_LOADING = kwargs.get('expense_loading', 0.1)
    constants.GENDER = kwargs.get('gender', 'Male')

    # check filepath
    outdir = './output'
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    # markov inputs
    HSD =  ['H', 'S', 'D']
    filenames = [   ('./input/' + fn) for fn in ['HD.csv','HS.csv','SD.csv','SH.csv']]
    # inputs for the rest of the steps
    BCFIdle_df = pd.read_csv(constants.readpath + constants.BCFIdle)
    BCFDelta_df = pd.read_csv(constants.readpath + constants.BCFDelta)

    interest_df = pd.read_csv(constants.readpath + constants.interest)

    (pop_df, pop_delta_df) = calculateMarkov(HSD,filenames)

    (EBI_df, EBD_df) = calculateBCF(BCFIdle_df, BCFDelta_df, pop_df, pop_delta_df)
    interest_df = valueCalculation.calculateActualValue(interest_df)

    PCF_df = pd.read_csv(constants.readpath + constants.PCF)
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

runModel(age=20)
