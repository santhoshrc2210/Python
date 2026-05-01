import pandas as pd
import numpy as np
import re

# Filter all warnings. If you would like to see the warnings, please comment the two lines below.
import warnings
warnings.filterwarnings('ignore')
"""
Q.1
Load the energy data from the file assets/Energy Indicators.xls, which is a list of indicators of energy supply and renewable electricity production from the United Nations for the year 2013, and should be put into a DataFrame with the variable name of Energy.

Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:

['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable]

Convert Energy Supply to gigajoules (Note: there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as np.NaN values.

Rename the following list of countries (for use in later questions):

"Republic of Korea": "South Korea", "United States of America": "United States", "United Kingdom of Great Britain and Northern Ireland": "United Kingdom", "China, Hong Kong Special Administrative Region": "Hong Kong"

There are also several countries with parenthesis in their name. Be sure to remove these, e.g. 'Bolivia (Plurinational State of)' should be 'Bolivia'. Additionally, there are several countries with Numeric digits in their name. Make sure to remove these as well, e.g. 'Italy9' should be 'Italy'.

Next, load the GDP data from the file assets/world_bank.csv, which is a csv containing countries' GDP from 1960 to 2015 from World Bank. Call this DataFrame GDP.

Make sure to skip the header, and rename the following list of countries:

"Korea, Rep.": "South Korea",  "Iran, Islamic Rep.": "Iran", "Hong Kong SAR, China": "Hong Kong"

Finally, load the Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology from the file assets/scimagojr-3.xlsx, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame ScimEn.

Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15).

The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015'].

This function should return a DataFrame with 20 columns and 15 entries, and the rows of the DataFrame should be sorted by "Rank".

"""

def answer_one():
    # YOUR CODE HERE
    energy_ind='assets/Energy Indicators.xls'
    ENERGY=pd.read_excel(energy_ind)

    #remove footer
    #print(ENERGY.iloc[246:])
    rows_to_drop = ENERGY.index[244:] 
    ENERGY= ENERGY.drop(rows_to_drop)
    #print(ENERGY.tail())

    #remove header
    #print(ENERGY.iloc[:14])
    rows_to_drop = ENERGY.index[:17] 
    ENERGY= ENERGY.drop(rows_to_drop)
    #print(ENERGY.head())

    #remove first 2 coloumns
    #print(ENERGY.columns)
    ENERGY.drop(columns=['Unnamed: 0', 'Unnamed: 1'],inplace=True)
    #print(ENERGY.head())
    #print(ENERGY.columns)

    # change column names
    new_column_names = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    ENERGY.columns = new_column_names
    #print(ENERGY.columns)
    #print(ENERGY.head())

    #Convert Energy Supply to gigajoules (Note: there are 1,000,000 gigajoules in a petajoule)
    ENERGY['Energy Supply'] = ENERGY['Energy Supply'].replace('...', np.NaN)
    scal_value = 1000000
    ENERGY['Energy Supply'] = ENERGY['Energy Supply'] * scal_value
    #print(ENERGY.head())
    #print(ENERGY.columns)

    #Rename the following list of countries
    replacements = {'Republic of Korea': 'South Korea', 'United States of America20': 'United States', 'United Kingdom of Great Britain and Northern Ireland19': 'United Kingdom', 
                    'China, Hong Kong Special Administrative Region3': 'Hong Kong'}
    ENERGY['Country'] = ENERGY['Country'].replace(replacements)
    #print(ENERGY.iloc[211:])

    #print(ENERGY.tail(20))
    #country names cleaning, using a function
    def clean_ctry_name(pattern):
        replacements = {}
        #pattern = r'\b(.+)\s*\((.+)\)'
        needs_corr = ENERGY['Country'].str.contains(pattern, regex=True)
        matching_names = ENERGY.loc[needs_corr, 'Country']
        for ctry in list(matching_names):
            match = re.search(pattern, ctry)
            replacements[ctry] = match.group(1)
        #print(replacements)
        return replacements

    #print(clean_ctry_name(r'([A-Za-z]+)(\d+)'))
    #print(clean_ctry_name(r'\b(.+)\s*\((.+)\)'))
    #word followed by number
    ENERGY['Country'] = ENERGY['Country'].replace(clean_ctry_name(r'([a-zA-Z\s,]+)(\d+)'))
    #word followed by another in brackets
    ENERGY['Country'] = ENERGY['Country'].replace(clean_ctry_name(r'\b([a-zA-Z\s]+)\s\((.+)\)'))
    #print(ENERGY.tail(20))
    
    #print all values in coloumn
    #print(ENERGY['Country'].to_string(index=False, header=False))  
    
    #print(ENERGY.columns())
    
    #read csv file and skip header
    GDP= pd.read_csv('assets/world_bank.csv', header=4)
    #print(GDP.head())
    #print(GDP.columns)

    #Rename the following list of countries
    replacements_gdp = {"Korea, Rep.": "South Korea",  "Iran, Islamic Rep.": "Iran", "Hong Kong SAR, China": "Hong Kong"}
    GDP['Country Name'] = GDP['Country Name'].replace(replacements_gdp)
    #print(GDP.head())
    #for new_name in replacements_gdp.values():
    #    print(GDP.loc[GDP['Country Name'] == new_name])

    sci_mag= 'assets/scimagojr-3.xlsx'
    ScimEn=pd.read_excel(sci_mag)
    #print(ScimEn.head())
    #print(ScimEn.columns)

    #print(ENERGY.head())
    #print(GDP.columns)
    #print(ScimEn.head(15))

    #Use only the last 10 years (2006-2015) of GDP data
    GDP.drop(columns=['1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968',
           '1969', '1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977',
           '1978', '1979', '1980', '1981', '1982', '1983', '1984', '1985', '1986',
           '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995',
           '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004',
           '2005'], inplace=True)
    #print(GDP.columns)
    #print(GDP.head(15))

    #only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15).
    ScimEn = ScimEn.drop(ScimEn.index[15:])
    #print(ScimEn.head(16))

    #Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names)
    GDP.rename(columns={'Country Name': 'Country'}, inplace=True)
    #print(GDP.columns)

    ENERGY = ENERGY.set_index('Country')
    GDP = GDP.set_index('Country')
    ScimEn = ScimEn.set_index('Country')

    #test script
    country_list = ['Australia', 'Bolivia', 'China', 'Hong Kong', 'China, Macao Special Administrative Region', 'Denmark', 'Falkland Islands', 'France', 'Greenland', 'Indonesia', 'Iran', 'Italy', 'Japan', 'Kuwait', 'Micronesia', 'Netherlands', 'Portugal', 'South Korea', 'Saudi Arabia', 'Serbia', 'Sint Maarten', 'Spain', 'Switzerland', 'Ukraine', 'United Kingdom', 'United States', 'Venezuela']
    for i in range(len(country_list)):
        if country_list[i] not in ENERGY.index.values.tolist():
            print(country_list[i])
    
    test= pd.merge(ScimEn, GDP, how='left', left_index=True, right_index=True) 
    #print(test)
    merged_df= pd.merge(test, ENERGY, how='left', left_index=True, right_index=True) 
    #print(merged_df)


    #The index of this DataFrame should be the name of the country, and the columns should be 
    #['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 'H index', 
    #'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
    #print(merged_df.columns)

    merged_df = merged_df[['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 'H index', 
    'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']]

    #print(merged_df.columns)
    #print(merged_df.shape)
    #return 0
    return merged_df
    raise NotImplementedError()
#print(answer_one())

"""
Q.2
The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
"""
def answer_two():
    energy_ind='assets/Energy Indicators.xls'
    ENERGY=pd.read_excel(energy_ind)

    #remove footer
    #print(ENERGY.iloc[246:])
    rows_to_drop = ENERGY.index[244:] 
    ENERGY= ENERGY.drop(rows_to_drop)
    #print(ENERGY.tail())

    #remove header
    #print(ENERGY.iloc[:14])
    rows_to_drop = ENERGY.index[:17] 
    ENERGY= ENERGY.drop(rows_to_drop)
    #print(ENERGY.head())

    #remove first 2 coloumns
    #print(ENERGY.columns)
    ENERGY.drop(columns=['Unnamed: 0', 'Unnamed: 1'],inplace=True)
    #print(ENERGY.head())
    #print(ENERGY.columns)

    # change column names
    new_column_names = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    ENERGY.columns = new_column_names
    #print(ENERGY.columns)
    #print(ENERGY.head())

    #Convert Energy Supply to gigajoules (Note: there are 1,000,000 gigajoules in a petajoule)
    ENERGY['Energy Supply'] = ENERGY['Energy Supply'].replace('...', np.NaN)
    scal_value = 1000000
    ENERGY['Energy Supply'] = ENERGY['Energy Supply'] * scal_value
    #print(ENERGY.head())
    #print(ENERGY.columns)

    #Rename the following list of countries
    replacements = {'Republic of Korea': 'South Korea', 'United States of America20': 'United States', 'United Kingdom of Great Britain and Northern Ireland19': 'United Kingdom', 
                    'China, Hong Kong Special Administrative Region3': 'Hong Kong'}
    ENERGY['Country'] = ENERGY['Country'].replace(replacements)
    #print(ENERGY.iloc[211:])

    #print(ENERGY.tail(20))
    #country names cleaning, using a function
    def clean_ctry_name(pattern):
        replacements = {}
        #pattern = r'\b(.+)\s*\((.+)\)'
        needs_corr = ENERGY['Country'].str.contains(pattern, regex=True)
        matching_names = ENERGY.loc[needs_corr, 'Country']
        for ctry in list(matching_names):
            match = re.search(pattern, ctry)
            replacements[ctry] = match.group(1)
        return replacements

    #print(clean_ctry_name(r'([A-Za-z]+)(\d+)'))
    #print(clean_ctry_name(r'\b(.+)\s*\((.+)\)'))
    #word followed by number
    ENERGY['Country'] = ENERGY['Country'].replace(clean_ctry_name(r'([a-zA-Z\s,]+)(\d+)'))
    #word followed by another in brackets
    ENERGY['Country'] = ENERGY['Country'].replace(clean_ctry_name(r'\b([a-zA-Z\s]+)\s\((.+)\)'))
    #print(ENERGY.tail(20))

    #read csv file and skip header
    GDP= pd.read_csv('assets/world_bank.csv', header=4)
    #print(GDP.head())
    #print(GDP.columns)

    #Rename the following list of countries
    replacements_gdp = {"Korea, Rep.": "South Korea",  "Iran, Islamic Rep.": "Iran", "Hong Kong SAR, China": "Hong Kong"}
    GDP['Country Name'] = GDP['Country Name'].replace(replacements_gdp)
    #print(GDP.head())
    #for new_name in replacements_gdp.values():
    #    print(GDP.loc[GDP['Country Name'] == new_name])

    sci_mag= 'assets/scimagojr-3.xlsx'
    ScimEn=pd.read_excel(sci_mag)
    #print(ScimEn.head())
    #print(ScimEn.columns)

    #print(ENERGY.head())
    #print(GDP.columns)
    #print(ScimEn.head(15))

    #Use only the last 10 years (2006-2015) of GDP data
    GDP.drop(columns=['1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968',
           '1969', '1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977',
           '1978', '1979', '1980', '1981', '1982', '1983', '1984', '1985', '1986',
           '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995',
           '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004',
           '2005'], inplace=True)
    #print(GDP.columns)
    #print(GDP.head(15))

    #only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15).
    #ScimEn = ScimEn.drop(ScimEn.index[15:])
    #print(ScimEn.head(16))

    #Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names)
    GDP.rename(columns={'Country Name': 'Country'}, inplace=True)
    #print(GDP.columns)   
    
    #print(len(ENERGY))
    #print(len(GDP))
    #print(len(ScimEn))
   
    
    #inner merge
    df1= pd.merge(ENERGY, GDP, how='inner', on=['Country'])
    df2= pd.merge(ScimEn, df1 , how='inner', on=['Country'])
    #print(df2)
    #outer merge
    df3= pd.merge(ENERGY, GDP, how='outer', on=['Country'])
    df4= pd.merge(ScimEn, df3, how='outer', on=['Country'])    
    
    #print(len(df2))
    #print(len(df4))
    missing_rows= len(df4)-len(df2)
    return missing_rows

#print(answer_two())
"""
q.3

What are the top 15 countries for average GDP over the last 10 years?

This function should return a Series named avgGDP with 15 countries and their average GDP sorted in descending order.
"""
def answer_three():
    # YOUR CODE HERE
     #read csv file and skip header
    GDP= answer_one()
    # Using apply with a lambda function
    GDP['average_gdp'] = GDP[['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014',
       '2015']].apply(lambda row: np.nanmean(row), axis=1)
     
    GDP=GDP.sort_values(by='average_gdp', ascending=False)
    
    #GDP = GDP.set_index('Country')
    avgGDP = GDP['average_gdp']
    #print(type(avgGDP))
    
    return avgGDP
    raise NotImplementedError()
    
#print(answer_three())
"""
q.4

By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?

This function should return a single number.
"""
def answer_four():
    # YOUR CODE HERE
      #read csv file and skip header
    GDP= answer_one()
    
    #print(GDP.loc['United Kingdom'])
    
    uk_gdp_06 = GDP.loc['United Kingdom', '2006']
    uk_gdp_15 = GDP.loc['United Kingdom', '2015']
    #print(uk_gdp_15,uk_gdp_06)
    return uk_gdp_15-uk_gdp_06
    raise NotImplementedError()
#print(answer_four())
"""
q.5

What is the mean energy supply per capita?

This function should return a single number.
"""
def answer_five():
    # YOUR CODE HERE
    ENERGY=answer_one()
    
    ENERGY['Energy Supply per Capita'] = ENERGY['Energy Supply per Capita'].replace('...', np.NaN)
    #print(ENERGY.columns)
    #print(ENERGY.head())
    return ENERGY['Energy Supply per Capita'].mean()
    raise NotImplementedError()
    

#print(answer_five())    

"""
q.6

What country has the maximum % Renewable and what is the percentage?

This function should return a tuple with the name of the country and the percentage.
"""

def answer_six():
    # YOUR CODE HERE
    ENERGY=answer_one()
    
    ENERGY['% Renewable'] = ENERGY['% Renewable'].replace('...', np.NaN)
    ENERGY['% Renewable'] = pd.to_numeric(ENERGY['% Renewable'], errors='coerce')
    
    ctry_name=ENERGY['% Renewable'].idxmax()
    #print(ENERGY.head())
    max_ren_energ=ENERGY['% Renewable'].max()
    #print(ctry_name, max_ren_energ)
    ans=(ctry_name, max_ren_energ)
    return ans   
    raise NotImplementedError()
    
#print(answer_six())
"""
q.7

Create a new column that is the ratio of Self-Citations to Total Citations. What is the maximum value for this new column, and what country has the highest ratio?

This function should return a tuple with the name of the country and the ratio.
"""
def answer_seven():
    # YOUR CODE HERE
    df=answer_one()
    
    df['ratio_citations'] = df['Self-citations'] / (df['Citations'])
    #print(df.columns)
    
    ctry_name=df['ratio_citations'].idxmax()
    #print(ENERGY.head())
    max_ratio=df['ratio_citations'].max()
    #print(ctry_name, max_ren_energ)
    ans=(ctry_name, max_ratio)
    return ans 
    raise NotImplementedError()
#print(answer_seven())
"""
q.8

Create a column that estimates the population using Energy Supply and Energy Supply per capita. What is the third most populous country according to this estimate?

This function should return the name of the country
"""
def answer_eight():
    # YOUR CODE HERE
    df=answer_one()
    
    df['pop_est'] = df['Energy Supply'] / (df['Energy Supply per Capita'])
    #print(df.columns)
        
    df=df.sort_values(by='pop_est', ascending=False)
        
    ctry_pop = df['pop_est']
    #print(ctry_pop)
    ctry=ctry_pop.index[2]
   
    return ctry
    raise NotImplementedError()
#print(answer_eight())
"""
q.9

Create a column that estimates the number of citable documents per person. What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the .corr() method, (Pearson's correlation).

This function should return a single number.

(Optional: Use the built-in function plot9() to visualize the relationship between Energy Supply per Capita vs. Citable docs per Capita)
"""
def answer_nine():
    # YOUR CODE HERE
    df=answer_one()
    df['pop_est'] = df['Energy Supply'] / (df['Energy Supply per Capita'])
    df['Citable documents per person'] = df['Citable documents'] / (df['pop_est'])
    
    
    #print(df.dtypes)
    df['Energy Supply per Capita'] = pd.to_numeric(df['Energy Supply per Capita'], errors='coerce')
    df['Citable documents per person'] = pd.to_numeric(df['Citable documents per person'], errors='coerce')
    correlation_coefficient = df['Energy Supply per Capita'].corr(df['Citable documents per person'])
    return correlation_coefficient
    raise NotImplementedError()
    
#print(answer_nine())    


"""
q.10

Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.

This function should return a series named HighRenew whose index is the country name sorted in ascending order of rank.
"""
def answer_ten():
    # YOUR CODE HERE
    df=answer_one()
    
    #print(df.columns)
    median_ren = df['% Renewable'].median()
    df['Renewable rank'] = np.where(df['% Renewable']>=median_ren, 1, 0)
    
    #df=df.sort_values(by=['Renewable rank', 'Country'], ascending=True)
    HighRenew = df['Renewable rank']
    #print(type(HighRenew))
    return HighRenew
    raise NotImplementedError()
    
#print(answer_ten())

"""
q.11

Use the following dictionary to group the Countries by Continent, then create a DataFrame that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.

ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
This function should return a DataFrame with index named Continent ['Asia', 'Australia', 'Europe', 'North America', 'South America'] and columns ['size', 'sum', 'mean', 'std']
"""
def answer_eleven():
    # YOUR CODE HERE
    df=answer_one()
    df['pop_est'] = df['Energy Supply'] / (df['Energy Supply per Capita'])
    
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    df = df.reset_index()
    #print(df)
    
    for ctry in ContinentDict.keys():
        df.loc[df['Country'] == ctry, 'Continent'] = ContinentDict[ctry]
    #print(df[['Country', 'Continent']])
    
    
    cont_counts = df.groupby('Continent').size()
    #print(cont_counts)
    
    cont_sum=df.groupby('Continent')['pop_est'].sum()
    #print(cont_sum)
    
    cont_mean=df.groupby('Continent')['pop_est'].mean()
    #print(cont_mean)
    
    cont_std=df.groupby('Continent')['pop_est'].std()
    #print(cont_std)
      
    data = {
  "size": cont_counts,
  "sum": cont_sum,
  "mean": cont_mean,
  "std": cont_std,      
   }

    # Load data into a DataFrame object
    df_comb = pd.DataFrame(data)
    #print(df_comb)
    #print(df_comb.index)
    return df_comb
    raise NotImplementedError()

#print(answer_eleven())

"""
q.12

Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?

This function should return a Series with a MultiIndex of Continent, then the bins for % Renewable. Do not include groups with no countries.
"""
def answer_twelve():
    # YOUR CODE HERE
    df=answer_one()
    
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    df = df.reset_index()
    #print(df)
    
    for ctry in ContinentDict.keys():
        df.loc[df['Country'] == ctry, 'Continent'] = ContinentDict[ctry]
    #print(df[['Country', 'Continent']])
    
    
    #cont_counts = df.groupby('Continent').size()
    #print(cont_counts)
    #print(df.columns)
    
    #print(df['% Renewable'])
    df['% Renewable'] = pd.to_numeric(df['% Renewable'], errors='coerce')
    df['% Renewable old'] = df['% Renewable']
    df['% Renewable'] = pd.cut(df['% Renewable old'], bins=5)
    ren_counts = df.groupby('% Renewable').size()
    #print(ren_counts)
    #df.set_index(['Continent','% Renewable_group'])
    #print(df)
    
    grouped=df.groupby(['Continent', '% Renewable'])
    #print(grouped['Country'].size())
    
    return grouped['Country'].size()
    raise NotImplementedError()

#print(answer_twelve())
"""
q.13

Convert the Population Estimate series to a string with thousands separator (using commas). Use all significant digits (do not round the results).

e.g. 12345678.90 -> 12,345,678.90

This function should return a series PopEst whose index is the country name and whose values are the population estimate string
"""
def answer_thirteen():
    # YOUR CODE HERE
    df=answer_one()
    df['pop_est'] = df['Energy Supply'] / (df['Energy Supply per Capita'])
    
    #print(df['pop_est'])
    
     #function to return list of number of characters to split by
    def lst_char_splt(int_num):
        int_num_len= len(int_num)
        int_num_d= int_num_len // 3
        int_num_r= int_num_len % 3
        
        lst_num_char_splt = []
        #print(int_num_len, int_num_d, int_num_r)
        if int_num_r != 0:
            lst_num_char_splt.append(int_num_r)
            iter=0
            while iter < int_num_d:
                lst_num_char_splt.append(3)
                iter+=1
        if int_num_r == 0:
            iter=0
            while iter < int_num_d:
                lst_num_char_splt.append(3)
                iter+=1        
        return lst_num_char_splt
    
    #function to split num based on list of char to split by, return a list of the number split
    def split_int_num(lst_splt, num):
        num_str=str(num)
        splt_num_lst = []
        start_ind = 0
        end_ind = 0
        for splt_num in lst_splt:
            end_ind=end_ind+splt_num
            splt_num_lst.append(num_str[start_ind:end_ind])
            start_ind=end_ind
        return splt_num_lst
    #print(split_int_num([1, 3, 3, 3], 1367645161))
    
    #function to add the numbers in list by comma
    def comb_num(lst_num):
            
        combnd_num=lst_num[0]
        for idx in range(1,len(lst_num)):  
            combnd_num= combnd_num + ',' + lst_num[idx]           
        return  combnd_num    
    #print(comb_num(['1', '367', '645', '161']))
            
               
    lst_pop_format = []
    for pop in df['pop_est']:
        int_pop, dec_pop = str(pop).split(".")
        lst_num_char = lst_char_splt(int_pop)
        splt_num = split_int_num(lst_num_char, int_pop)
        comb_num_comm = comb_num(splt_num)
        int_dec_comb = comb_num_comm + '.' + dec_pop
        lst_pop_format.append(int_dec_comb)
    #print(lst_pop_format)
   
    #print(df['pop_est'])
    PopEst = pd.Series(lst_pop_format, index=['China', 'United States', 'Japan', 'United Kingdom',
       'Russian Federation', 'Canada', 'Germany', 'India', 'France',
       'South Korea', 'Italy', 'Spain', 'Iran', 'Australia', 'Brazil'])       
    
    return PopEst
    raise NotImplementedError()
    
#print(answer_thirteen())
