import pandas as pd
import numpy as np
import copy 

#FUNCTIONS
def filter_out_descriptions_and_non_tags(df):
    '''
    Utility Function: 
    '''
    sku_desc_filter_out = lambda x: 'sku_desc' not in x
    sku_qty_tag = lambda x: not( ('sku' not in x) and ('qty' not in x) and ('tag' not in x))
    cols_non_desc =  list(filter(sku_desc_filter_out, df.columns.to_list()))
    cols_non_desc =  list(filter(sku_qty_tag, cols_non_desc))
    return copy.copy(df[cols_non_desc])

def filter_out_tags(df):
    '''
    Utility Function: 
    '''
    sku_w_tags = lambda x: 'tag' not in x
    cols_non_desc =  list(filter(sku_w_tags, df.columns.to_list()))
    return copy.copy(df[cols_non_desc])

def keep_tags(df):
    sku_w_tags = lambda x: 'tag' in x
    cols_tags =  list(filter(sku_w_tags, df.columns.to_list()))
    return copy.copy(df[cols_tags])

def column_renamer(df, sheet_name):
    df.columns = [ sheet_name+'_' + x if (('sku' in x) or ('qty' in x)) else x for x in  df.columns.to_list()]
    return df

def dataframes_splitter(path_to_the_file = r'.\uploads\VxRail_E560N.xls', list_for_splits=['Street_Prices', 'List_Prices']):
    OCpR_dfs, Prices_dfs = [], []
    
    excel_ = pd.ExcelFile(path_to_the_file)

    worksheets_names = excel_.sheet_names
    for ws_ in worksheets_names:

        if (ws_ in list_for_splits) or ('Prices_' in ws_) :
            some_details = pd.read_excel(excel_, sheet_name=ws_)
            some_details.title = ws_
            Prices_dfs.append(some_details )
        else:
            df_comb = filter_out_descriptions_and_non_tags(pd.read_excel(excel_, sheet_name=ws_))
            
            OCpR_dfs.append(column_renamer(df_comb, ws_))
    
    return OCpR_dfs, Prices_dfs

def common_tags(df_l, df_r):
    left_ = df_l.columns.to_list()
    rigth_ = df_r.columns.to_list()
    return list(set(left_).intersection(rigth_))

def loop_thru_dataframes(df_list, howhow='inner'):
    ocpr_df = pd.DataFrame()
    counter =  1
    for d_ in df_list:
        if counter == 1:
            ocpr_df = d_
            counter += 1
        else:
            cmmn_tags_list = common_tags(ocpr_df, d_)
            if len(cmmn_tags_list) == 0:
                ocpr_df['comKey'] = 1
                d_['comKey'] = 1
                ocpr_df = pd.merge( ocpr_df, d_, on ='comKey', how=howhow)
                ocpr_df = ocpr_df.drop(columns=['comKey'])
            else:
                ocpr_df = pd.merge( ocpr_df, d_, on=cmmn_tags_list ,how=howhow)    
    return ocpr_df


def order_columns(df):
    sku_and_qty = lambda x : ('sku' in x) or ('qty' in x)
    tag = lambda x : ('tag' in x) 
    cols_ = df.columns.to_list()
    return  pd.concat( [ df[list(filter(sku_and_qty, cols_))], df[list(filter(tag, cols_))] ], axis=1)

def OCpR_stacker(df):
    
    OCpR_stackable = filter_out_tags(df)
    OCpR_conf_tags = keep_tags(df)
    list_to_add_as_code =[x+1 for x in  OCpR_conf_tags.index.to_list().copy()]     
    OCpR_conf_tags['code'] = list_to_add_as_code
    
    rows_to_stack = [] 
    for row in OCpR_stackable.iterrows():
        conf_number = row[0]
        col_ = 1
        elements_to_stuck = []
        for elem_ in row[1]: 

            if col_%2 == 0:
                                
                elements_to_stuck.append(elem_)
                elements_to_stuck.append(conf_number+1)
                rows_to_stack.append(elements_to_stuck)
                elements_to_stuck = []
            else:
                elements_to_stuck.append(elem_)

            col_ +=1
    return pd.DataFrame(rows_to_stack, columns=['SKU', 'qty','code']), OCpR_conf_tags

def AnalysisDF(path_to_the_file__ ):

    dfs, details_dfs = dataframes_splitter(path_to_the_file = path_to_the_file__)
    OCpR = loop_thru_dataframes(dfs)
    OCpR_staked, OCpR_tags = OCpR_stacker(OCpR)
    details_dfs.insert(0,OCpR_staked)
    df_ca = loop_thru_dataframes(details_dfs, howhow='left')

    #ListPrices
    df_ca['q_by_Lp'] = df_ca['List_Price'] * df_ca['qty']
    df_ca = df_ca.fillna(0.0)
    Conf_List_prices = df_ca[['code','q_by_Lp']].groupby('code').sum()
    Conf_List_prices['code'] = Conf_List_prices.index
    Conf_List_prices.index = Conf_List_prices.index.rename('index')

    #StreetPrices
    df_ca['q_by_Sp'] = df_ca['Street_Price'] * df_ca['qty']
    df_ca = df_ca.fillna(0.0)
    Conf_Street_prices = df_ca[['code','q_by_Sp']].groupby('code').sum()
    Conf_Street_prices['code'] = Conf_List_prices.index
    Conf_Street_prices.index = Conf_Street_prices.index.rename('index')

    final_df = pd.merge(OCpR_tags,Conf_List_prices, on='code', how='inner')

    final_df = pd.merge(final_df,Conf_Street_prices, on='code', how='inner')
    
    return final_df