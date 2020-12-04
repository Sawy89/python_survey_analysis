import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# %% Functions
def clean_data(df):
    # Multiindex
    idx = df.columns.str.replace('::',':')
    idx = idx.str.split(':', expand=True).swaplevel()
    df.columns = idx

    # boolean
    for col_tupla in df.columns:
        values = list(set(df[col_tupla]))
        if np.nan in values:
            values = [x for x in values if str(x) != 'nan']
        if col_tupla[1] == values[0]:
            if len(values) == 1: 
                df[col_tupla] = df[col_tupla].apply(lambda x: True if x == values[0] else False)
            elif len(values) == 0:
                df[col_tupla] = False
    
    cols_fillna = [(np.nan, 'Do you consider yourself as a Data-Scientist?'),
                  (np.nan, 'Is Python the main language you use for your current projects?')]
    df[cols_fillna] = df[cols_fillna].fillna('not answered')
    
    return df
    
   
# %% Classes
class AnalyzeSingleQuestion:
    
    def __init__(self, DF, colname_reference, colname_tocompare):
        self.DF = DF
        self.colname_reference = colname_reference
        self.colname_tocompare = colname_tocompare
        
        if type(colname_tocompare) == tuple:
            self.singlecol = True
        else:
            self.singlecol = False
            self.possible_answer = list(set(DF[colname_reference]))
    
    
    def calcHist(self, perc=True, ordered_row=None, drop_answer=None):
        '''
        Calculate the histogram with colname_tocompare as label
        INPUT:
        - perc: if True, calculate the percentage
        - ordered_row is the list of rows to be shown in order
        - drop_answer is the list of rows to drop
        '''
        assert self.singlecol == True
        df_hist = self.DF.groupby([self.colname_tocompare, self.colname_reference]).count()[(np.nan,'response_id')].unstack()
        if drop_answer != None:
            df_hist = df_hist.drop(index=drop_answer)
        if ordered_row != None:
            df_hist = df_hist.loc[ordered_row]
        if perc == True:
            df_hist = np.round(100 * df_hist / df_hist.sum(),2)
        self.df_hist = df_hist
        return df_hist
    
    
    def plotBar(self, limit=None, title='Titolo'):
        if self.singlecol == True:
            df_plot = self.df_hist
        else:
            df_plot = self.df_hist.transpose()
        
        if limit == None:
            ax = df_plot.plot.bar(figsize=(15,5), title=title)
        else:
            ax = df_plot.loc[df_plot[limit['name']]>limit['value']].plot.bar(figsize=(15,5), title=title)
                
        ax.set_ylabel("%")

    
    def calcHistMulti(self, perc=True):
        assert self.singlecol == False
        df_hist = self.DF.groupby(self.colname_reference).sum()[self.colname_tocompare]
        df_hist.columns.name = self.colname_tocompare
        
        if perc == True:
            df_hist = df_hist.apply(lambda x: np.round(100 * x / df_hist.sum(axis=1),2) )
        self.df_hist = df_hist
        return df_hist