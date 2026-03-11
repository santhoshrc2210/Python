Question1:

import pandas as pd

def proportion_of_education():
    df = pd.read_csv('assets/NISPUF17.csv', index_col=0)
    total_num_child = df.shape[0]
    
    #print(df['EDUC1'].unique())
    
    #less than high school
    less_hs_df=df[df['EDUC1'] == 1]
    less_hs_prop=less_hs_df['EDUC1'].shape[0]/total_num_child
    #print(less_hs_prop)
    
    #equal to high school
    eq_hs_df=df[df['EDUC1'] == 2]
    eq_hs_prop=eq_hs_df['EDUC1'].shape[0]/total_num_child
    #print(eq_hs_prop)
    
    #more than high school
    mr_hs_df=df[df['EDUC1'] == 3]
    mr_hs_prop=mr_hs_df['EDUC1'].shape[0]/total_num_child
    #print(mr_hs_prop)
    
    #college graduate
    clg_df=df[df['EDUC1'] == 4]
    clg_prop=clg_df['EDUC1'].shape[0]/total_num_child
    #print(clg_prop)
    
    #print(less_hs_prop + eq_hs_prop + mr_hs_prop + clg_prop)
    
    educ_prop = {"less than high school":less_hs_prop,
    "high school":eq_hs_prop,
    "more than high school but not college":mr_hs_prop,
    "college":clg_prop}
    return educ_prop
    # YOUR CODE HERE
    raise NotImplementedError()
    
#print(proportion_of_education()) 

Question2:

import pandas as pd

def average_influenza_doses():
    df = pd.read_csv('assets/NISPUF17.csv', index_col=0)
    #df.fillna(0, inplace=True) #replace nan by 0
    
    #print(df['CBF_01'].unique()) #[ 1  2 99 77] yes, no, dont know, missing
    #print(df['P_NUMFLU'].unique()) #[nan  3.  0.  2.  1.  4.  5.  6.] floating point type
    #print(df['P_NUMFLU'].head())
    
    new_df=df[df['P_NUMFLU'] >= 0]
    #print(len(new_df))
    #rcvd brstmilk
    rcvd_brstmlk_df=new_df[new_df['CBF_01'] == 1]
    num_child_rcvd_brstmlk = rcvd_brstmlk_df.shape[0]
    num_inf_vacc=rcvd_brstmlk_df['P_NUMFLU'].sum()
    
    
    #did not rcv brstmilk
    no_brstmlk_df=new_df[new_df['CBF_01'] == 2]
    num_child_no_brstmlk=no_brstmlk_df.shape[0]
    num_inf_vacc1=no_brstmlk_df['P_NUMFLU'].sum()
    #print(no_brstmlk_df['CBF_01'].head())
    
    
    return (num_inf_vacc/num_child_rcvd_brstmlk, num_inf_vacc1/num_child_no_brstmlk)
    # YOUR CODE HERE
    raise NotImplementedError()
    
print(average_influenza_doses())

Question3:

import pandas as pd

def chickenpox_by_sex():
    df = pd.read_csv('assets/NISPUF17.csv', index_col=0)
    df.fillna(0, inplace=True) #replace nan by 0
    
    # children vaccinated varicella dose atleast one
    #print(df['P_NUMVRC'].unique()) #total number of doses[nan  1.  0.  2.  3.]
    
    #print(df['SEX'].unique()) #[1 2] M F
    
    #chickenpox diagnosed
    #chickenpox not diagnosed
    #print(df['HAD_CPOX'].unique()) #[ 1  2 77 99] yes no
    
    #male
    ml_df = df[df['SEX'] == 1]  
    vacc_ml_df = ml_df[ml_df['P_NUMVRC'] >= 1]
    num_ml_vacc_cpx = vacc_ml_df[vacc_ml_df['HAD_CPOX'] == 1].shape[0]
    num_ml_vacc_nocpx = vacc_ml_df[vacc_ml_df['HAD_CPOX'] == 2].shape[0]
    
    #female
    fml_df = df[df['SEX'] == 2]
    vacc_fml_df = fml_df[fml_df['P_NUMVRC'] >= 1]
    num_fml_vacc_cpx = vacc_fml_df[vacc_fml_df['HAD_CPOX'] == 1].shape[0]
    num_fml_vacc_nocpx = vacc_fml_df[vacc_fml_df['HAD_CPOX'] == 2].shape[0]
    
     
    return {"male" : num_ml_vacc_cpx/num_ml_vacc_nocpx, "female" :num_fml_vacc_cpx/num_fml_vacc_nocpx}
    # YOUR CODE HERE
    raise NotImplementedError()

#print(chickenpox_by_sex())

Question4:

def corr_chickenpox():
    import scipy.stats as stats
    import numpy as np
    import pandas as pd
    
    # this is just an example dataframe
    #df=pd.DataFrame({"had_chickenpox_column":np.random.randint(1,3,size=(100)),
                   #"num_chickenpox_vaccine_column":np.random.randint(0,6,size=(100))})

    # here is some stub code to actually run the correlation
    #corr, pval=stats.pearsonr(df["had_chickenpox_column"],df["num_chickenpox_vaccine_column"])
    
    # just return the correlation
    #return corr
    
    # YOUR CODE HERE
    df = pd.read_csv('assets/NISPUF17.csv', index_col=0)
    #df.fillna(0, inplace=True)
    
    new_df=df[df['HAD_CPOX'] <=2]
    new_df=new_df[new_df['P_NUMVRC'] >= 0]
    #df.sort_index(inplace=True)
    #print(len(new_df))
    corr, pval=stats.pearsonr(new_df["HAD_CPOX"],new_df["P_NUMVRC"])
    
    return corr
    
    raise NotImplementedError()

print(corr_chickenpox()) 

