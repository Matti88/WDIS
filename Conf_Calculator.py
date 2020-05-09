import pandas as pd
import numpy as np
import copy 
import json
import importlib.util
spec = importlib.util.spec_from_file_location("string_sum", "C:\\Users\\zuzan\\Desktop\\Projects\\WDIS\\string_sum.pyd")
sr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sr)
 
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
    '''
    Utility Function: 
    '''
    sku_w_tags = lambda x: 'tag' in x
    cols_tags =  list(filter(sku_w_tags, df.columns.to_list()))
    return copy.copy(df[cols_tags])

def column_renamer(df, sheet_name):
    '''
    Utility Function: 
    '''
    df.columns = [ sheet_name+'_' + x if (('sku' in x) or ('qty' in x)) else x for x in  df.columns.to_list()]
    return df

def dataframes_splitter(path_to_the_file = r'./uploads/MyCompany.xls', prices_tables=['Street_Prices', 'List_Prices'], order_tables = ['OrderData']):
    '''
    Utility Function: 
    '''
    OCpR_dfs, Prices_dfs,  Orders_dfs = [], [], []
    
    excel_ = pd.ExcelFile(path_to_the_file)

    worksheets_names = excel_.sheet_names
    for ws_ in worksheets_names:

        if (ws_ in prices_tables) or ('Prices_' in ws_) :
            some_details = pd.read_excel(excel_, sheet_name=ws_)
            some_details.title = ws_
            Prices_dfs.append(some_details )
        elif (ws_ in order_tables) or ('Order' in ws_) :

            Order_tables = pd.read_excel(excel_, sheet_name=ws_)
            Order_tables.title = ws_
            Orders_dfs.append(Order_tables)
        else:
            df_comb = filter_out_descriptions_and_non_tags(pd.read_excel(excel_, sheet_name=ws_))
            
            OCpR_dfs.append(column_renamer(df_comb, ws_))
    return OCpR_dfs, Prices_dfs, Orders_dfs

def common_tags(df_l, df_r):
    '''
    Utility Function: 
    '''
    left_ = df_l.columns.to_list()
    rigth_ = df_r.columns.to_list()
    return list(set(left_).intersection(rigth_))

def loop_thru_dataframes(df_list, howhow='inner'):
    '''
    Utility Function: 
    '''
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
    '''
    Utility Function: 
    '''
    sku_and_qty = lambda x : ('sku' in x) or ('qty' in x)
    tag = lambda x : ('tag' in x) 
    cols_ = df.columns.to_list()
    return  pd.concat( [ df[list(filter(sku_and_qty, cols_))], df[list(filter(tag, cols_))] ], axis=1)

def OCpR_stacker(df):
    '''
    Utility Function: 
    '''
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

def ConfigurationBoundleString(list_of_items):
    '''
    Utility Function: 
    '''
    exit_string = ''
    for elem_pos in range(len(list_of_items)):
        if (elem_pos + 1)%2 == 0:
            exit_string = exit_string + '~' + str(list_of_items[elem_pos])
        else:
            exit_string = exit_string + ',' + str(list_of_items[elem_pos])
    
    return exit_string[1:]

def getOrderDat_returnBoundleToOrder(dataFrameOfOrders):
    '''
    Utility Function: 
    '''
    string_out = ''
    list_storing_strings = []
    months = []
    seq_numbers = []
    month = None
    OrderSeq = None
    for  index, row in dataFrameOfOrders.iterrows():

        #first line
        if (month is None) and (OrderSeq is None):
            string_out = row['SKU'] + '~' + str(row['qty'])
            month, OrderSeq = row['Month'], row['OrdSeq']

        elif (month != row['Month']) or( OrderSeq != row['OrdSeq']):
            list_storing_strings.append(string_out)
            months.append(month)
            seq_numbers.append(OrderSeq)
            
            string_out = row['SKU'] + '~' + str(row['qty'])
            month, OrderSeq = row['Month'], row['OrdSeq'] 
        else:
            string_out = string_out + str(row['SKU']) + '~' + str(row['qty']) + ',' 

    d = {'boundles': list_storing_strings, 'month': months, 'seqNumb':seq_numbers }
    boundlesToMonthSquenceOrders = pd.DataFrame(data=d)     
    return boundlesToMonthSquenceOrders

def secretFormulaGeneratingSeuquencesSalesData(list_of_conf_code):
    '''
    Utility Function: for generating sequence of Sales Data
    '''
    import random

    weight_for_confs = []
    months = [1,2,3,4,5]
    percentages = [0.3,0.2, 0.25]
    month_outcome = {}

    for conf_ in list_of_conf_code:
        weight_for_confs.append(random.betavariate(1.3,5))

    norm = [float(i)/sum(weight_for_confs) for i in weight_for_confs]
    prob_conf = sorted(list(zip(norm, list_of_conf_code)), key=lambda x: x[0], reverse=True)

    for month_ in months:
        selected_items = []
        rangeSelected = prob_conf[0:random.randint(100,120)]
        for i in range(int(round(len(rangeSelected) * random.choice(percentages),0))):
            selected_items.append(random.choice(rangeSelected))
        month_outcome[month_] = selected_items

    return month_outcome

def secretFormula_salesData(dict_month_sales, order_data_extract):
    '''
    Utility Function: Generates Sales Data with 
    '''
    dataSales = None
    for month_ in dict_month_sales.keys():
        ord_seq = 1
        for item in dict_month_sales[month_]:
            singleOrder = order_data_extract[order_data_extract['code'] == item[1]].copy()
            singleOrder['Month']  = month_
            singleOrder['OrdSeq'] = ord_seq
            ord_seq += 1
            if dataSales is None:
                dataSales = singleOrder
            else:
                dataSales = pd.concat([dataSales , singleOrder])
    return dataSales

def AnalysisDF(path_to_the_file__ ):
    '''
    Process Function: 
    '''
    #Generating Basic df
    dfs, details_dfs, orders_dfs = dataframes_splitter(path_to_the_file = path_to_the_file__)
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

    #adding to the OCpR basic the List and Street Prices
    final_df = pd.merge(OCpR_tags,Conf_List_prices, on='code', how='inner')
    final_df = pd.merge(final_df,Conf_Street_prices, on='code', how='inner')
    
    return final_df

def ADOT_dfs(MyCompany=r'./uploads/MyCompany.xls', Competitor=r'./uploads/Competitor.xls'):
    '''
    Process Function: 
    '''
    #basic DataFrames
    Competitor0 = AnalysisDF(MyCompany)
    Competitor1 = AnalysisDF(Competitor)

    #clearing out the configuration code in a very complicated way
    Comp0 = pd.concat([Competitor0[list(filter(lambda x: 'tag' in x,  Competitor0.columns))], Competitor0[['q_by_Lp','q_by_Sp']] ] , axis=1)
    Comp1 = pd.concat([Competitor1[list(filter(lambda x: 'tag' in x,  Competitor1.columns))], Competitor1[['q_by_Lp','q_by_Sp']] ] , axis=1)

    #summarying all the combinations of tags against the average prices related to those 
    Comp0_grouped = Comp0.groupby(list(filter(lambda x: 'tag' in x,  Comp0.columns))).mean().reset_index() 
    Comp1_grouped = Comp1.groupby(list(filter(lambda x: 'tag' in x,  Comp1.columns))).mean().reset_index() 

    return [Competitor0, Competitor1, Comp0, Comp1, Comp0_grouped, Comp1_grouped]

def ListStreetCal(file_, D3_ChartJS = True):
    '''
    Process Function: Calculating the List vs Street Data
    '''
    dfs, details_dfs , orders_dfs       = dataframes_splitter(path_to_the_file=file_)
    OCpR                                = loop_thru_dataframes(dfs)
    OCpR_staked, OCpR_tags              = OCpR_stacker(OCpR)
    details_dfs.insert(0,OCpR_staked)
    df_ca                               = loop_thru_dataframes(details_dfs, howhow='left')

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

    #creating a data List and Street
    final_df = pd.merge(OCpR_tags,Conf_List_prices, on='code', how='inner')
    final_df = pd.merge(final_df,Conf_Street_prices, on='code', how='inner')
    
    #choose the format for the return
    result_ = None
    if D3_ChartJS:
        result_ = final_df[['q_by_Lp', 'q_by_Sp']]

    else:
        lod = []
        points = list(zip(final_df['q_by_Lp'].to_list(), final_df['q_by_Sp'].to_list()))
        for elem in points:
            lod.append({'x':elem[0], 'y':elem[1]})

        result_ = {'datasets': [{
            'label': 'Scatter Competition Points',
            'data': lod
            }]
        }

    return result_

def AdvantageDisadvantageCal(MyCompany=r'./uploads/MyCompany.xls', Competitor=r'./uploads/Competitor.xls'):
    '''
    Process Function: Calculating all the situation onto which MyCompany has an advantage or disadvantage against Competitor
    '''
    #generating all dataFrames
    dfs_ = ADOT_dfs(MyCompany, Competitor)
    Competitor0, Competitor1, Comp0, Comp1, Comp0_grouped, Comp1_grouped  = dfs_[0], dfs_[1], dfs_[2], dfs_[3], dfs_[4], dfs_[5]
  
    #selecting the columns 
    cmmn_tags_list = list(filter(lambda x: not(('q_by_Lp' in x) or ('q_by_Sp' in x)) , common_tags(Comp0_grouped, Comp1_grouped)))
    ocpr_df = pd.merge(Comp0_grouped, Comp1_grouped, on=cmmn_tags_list ,how='inner', suffixes=('_0', '_1'))     

    #criteria for selections
    MyCompany_LP_Advantage  = ocpr_df[ocpr_df['q_by_Lp_0'] < ocpr_df['q_by_Lp_1']].to_json(orient="records")
    MyCompany_SP_Advantage  = ocpr_df[ocpr_df['q_by_Sp_0'] < ocpr_df['q_by_Sp_1']].to_json(orient="records")
    Competitor_SP_Advantage = ocpr_df[ocpr_df['q_by_Sp_0'] > ocpr_df['q_by_Sp_1']].to_json(orient="records")
    Competitor_LP_Advantage = ocpr_df[ocpr_df['q_by_Lp_0'] > ocpr_df['q_by_Lp_1']].to_json(orient="records")

    competition_Vantages = "{" + f""" "MyCompany_LP_Advantage" : {MyCompany_LP_Advantage}
                                    , "MyCompany_SP_Advantage" : {MyCompany_SP_Advantage} 
                                    , "Competitor_SP_Advantage" : {Competitor_SP_Advantage} 
                                    , "Competitor_LP_Advantage" : {Competitor_LP_Advantage} """ + "}"

    file_like_object = json.loads(competition_Vantages)

    return file_like_object

def ThreatsOpportunitiesCal(MyCompany=r'./uploads/MyCompany.xls', Competitor=r'./uploads/Competitor.xls'):
    '''
    Process Function: Calculating all the situation onto which MyCompany has an Threaths or Opportunity against Competitor
    '''
    dfs_ = ADOT_dfs(MyCompany, Competitor)

    Competitor0, Competitor1, Comp0, Comp1, Comp0_grouped, Comp1_grouped  = dfs_[0], dfs_[1], dfs_[2], dfs_[3], dfs_[4], dfs_[5]

    TO_dict = {'Threats' : [Competitor1, Comp0_grouped], 'Opportunities':[Competitor0, Comp1_grouped]}
    Threats_and_Opportunities = {}
    for key_ in TO_dict.keys():
        
        _comparison_items =  TO_dict[key_]
        comp_0, comp_1 = _comparison_items[0], _comparison_items[1]

        competition = pd.merge(
                        comp_0,
                        comp_1,
                    on= list(filter(lambda x: 'tag' in x,  common_tags(Competitor0,Comp1_grouped))),
                    how='inner', 
                    suffixes=('_AdvSrch', '_CompAdv'))  

        criteria_advantage_LP = competition['q_by_Lp_AdvSrch'] < competition['q_by_Lp_CompAdv']
        criteria_advantage_SP = competition['q_by_Sp_AdvSrch'] < competition['q_by_Sp_CompAdv']
        
        Advantage_LP = (json.loads(competition[criteria_advantage_LP].to_json(orient="records")))
        Advantage_SP = (json.loads(competition[criteria_advantage_SP].to_json(orient="records")))

        Threats_and_Opportunities[key_] = [{'ListPrices':Advantage_LP},{'StreetPrices':Advantage_SP}]

    return Threats_and_Opportunities

def sales_analysis_gen_matcher(path_to_the_file = r'./uploads/MyCompany.xls', prices_tables=['Street_Prices', 'List_Prices'], order_tables = ['OrderData']):
    '''
    Process Function: matches all the order data to a single product and it assigns to the order also its price and tags
    '''
    OCpR, Prices, Orders = dataframes_splitter(path_to_the_file = r'./uploads/MyCompany.xls', prices_tables=['Street_Prices', 'List_Prices'], order_tables = ['OrderData'])
    finalizedModel = loop_thru_dataframes(OCpR)
    finalizedModel = finalizedModel[ list(filter( lambda x : 'tag' not in x,  finalizedModel.columns)) ]
    config_boundles = pd.DataFrame()
    config_boundles['code'] = finalizedModel.index
    config_boundles['concat'] = pd.Series(finalizedModel.fillna('').values.tolist()).map(lambda x: ConfigurationBoundleString(x))
    dataFrameOfOrders = Orders[0]
    boundlesToMonthSquenceOrders = getOrderDat_returnBoundleToOrder(dataFrameOfOrders)
    conf_list_of_boundles_data = list(map(list,zip(config_boundles['concat'], config_boundles['code'].astype(str))))
    boundlesToMonthSquenceOrders_data = list(map(list,zip(  boundlesToMonthSquenceOrders['boundles'], boundlesToMonthSquenceOrders['month'].astype(str)+ "_" + boundlesToMonthSquenceOrders['seqNumb'].astype(str)  )))
    b = sr.loop_two_lists_rayon_codes(conf_list_of_boundles_data , boundlesToMonthSquenceOrders_data, 0.8) #TODO: decide how to use this value 
    fictionary_matching_results = {}
    for i in b:
        if i.orderseq in fictionary_matching_results.keys():
            if (i.score > fictionary_matching_results[i.orderseq][1]):
                fictionary_matching_results[i.orderseq] =  [i.boundle_code, i.score]
        else:
            fictionary_matching_results[i.orderseq] =  [i.boundle_code, i.score]

    month = []
    seq   = []
    match = []
    for match_ in fictionary_matching_results.keys():
        l_identity_order = match_.split('_') 
        month.append(int(l_identity_order[0]))
        seq.append(int(l_identity_order[1]))
        match.append(fictionary_matching_results[match_][0])
    d = {'Month': month, 'OrdSeq': seq, 'match': match}
    matched_df = pd.DataFrame(data=d)

    dataFrameOfOrders['unit_Price_QTY'] = dataFrameOfOrders['unit_Price'] * dataFrameOfOrders['qty']

    orders_totals = dataFrameOfOrders[['Month', 'OrdSeq', 'unit_Price_QTY']].groupby(['Month', 'OrdSeq']).sum().reset_index()

    orders_match_prices = pd.merge( matched_df, orders_totals, on=['Month', 'OrdSeq'],how='inner')
    orders_match_prices.rename(columns={'match':'code'}, inplace=True)
    orders_match_prices['code'] = orders_match_prices['code'].astype(int)


    OCpR, Prices, Orders = dataframes_splitter()
    Model_Tags = loop_thru_dataframes(OCpR)
    Model_Tags = Model_Tags[ list(filter( lambda x : 'tag' in x,  Model_Tags.columns))  ]
    Model_Tags['code'] = Model_Tags.index
    Model_Tags['code'] = Model_Tags['code'].astype(int)

    analyzed_orders = pd.merge(orders_match_prices, Model_Tags, on=['code'])
    data =  {'data' : json.loads(analyzed_orders.to_json(orient="records") )}
    return data

def threats_opportunities(path_to_the_file = r'./uploads/MyCompany.xls', prices_tables=['Street_Prices', 'List_Prices'], order_tables = ['OrderData']):
    '''
    Process Function: matches all the order data to a single product and it assigns to the order also its price and tags AND analyzes the threats and opportunities
    '''
    orderData = sales_analysis_gen_matcher()
    advantages_disadvantages = AdvantageDisadvantageCal()
    return True

def Product_on_confrontation(MyCompany=r'./uploads/MyCompany.xls', Competitor=r'./uploads/Competitor.xls'):
    #Competitors dataFrame
    Competitor0 = AnalysisDF(MyCompany)
    Competitor1 = AnalysisDF(Competitor)

    #clearing out the configuration code in a very complicated way
    Comp0 = pd.concat([Competitor0[list(filter(lambda x: 'tag' in x,  Competitor0.columns))], Competitor0[['q_by_Lp','q_by_Sp']] ] , axis=1)
    Comp1 = pd.concat([Competitor1[list(filter(lambda x: 'tag' in x,  Competitor1.columns))], Competitor1[['q_by_Lp','q_by_Sp']] ] , axis=1)

    #summarying all the combinations of tags against the average prices related to those 
    Comp0_grouped = Comp0.groupby(list(filter(lambda x: 'tag' in x,  Comp0.columns))).mean().reset_index() 
    Comp1_grouped = Comp1.groupby(list(filter(lambda x: 'tag' in x,  Comp1.columns))).mean().reset_index() 
    cmmn_tags_list = list(filter(lambda x: not(('q_by_Lp' in x) or ('q_by_Sp' in x)) , common_tags(Comp0_grouped, Comp1_grouped)))
    ocpr_df = pd.merge(Comp0_grouped, Comp1_grouped, on=cmmn_tags_list ,how='inner', suffixes=('_0', '_1'))  

    #creating specific confrontation
    bag_of_dfs_differnet_tags = {}
    tags_of_average_combinations = list(filter(lambda x: ('_tag' in x), ocpr_df.columns))
    for index, row_ in ocpr_df.iterrows():
        bag_of_tags = []
        for tag_name in tags_of_average_combinations:
            bag_of_tags.append(str(row_[tag_name]))

        dic_for_selection = dict(zip(tags_of_average_combinations, bag_of_tags))
        query = ' and '.join([f'{k} == {repr(v)}' for k, v in dic_for_selection.items()]) 

        averages_  = ocpr_df.query(query)
        My_Company = Competitor0.query(query)
        Competitor = Competitor1.query(query)
        step_1 = pd.merge(averages_,  My_Company,  on=common_tags(averages_,  My_Company), how='inner')
        step_2 = pd.merge(averages_,  Competitor,  on=common_tags(averages_,     Competitor), how='inner')

        step_1['Vendor'] = 'MyCompany'
        step_2['Vendor'] = 'Competitor'
        concatenated = pd.concat( [step_1,step_2 ], ignore_index=True)
        bag_of_dfs_differnet_tags['_'.join(bag_of_tags)] = concatenated.to_json(orient="records") 

    #generating json file 
    string_JSON  = ''
    for tags_compositions in bag_of_dfs_differnet_tags.keys():
        string_JSON_template = "{" + f""" "{tags_compositions}" : {bag_of_dfs_differnet_tags[tags_compositions]} """ + '} ,' 
        string_JSON = string_JSON + string_JSON_template
    return_string_JSON = "[" + string_JSON[:-2] + "]"
    file_like_object = json.loads(return_string_JSON)

    return file_like_object