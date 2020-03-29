import pandas as pd
import re
import pandasql as psql
import json




def comb_estimator(filename):
    #filename = 'HCI categorization V-P570 and V-P570F V2.xlsx'      

    stringToRemove = '.' + '\\' + 'uploads' + '\\'
    data = {'main':[], "err":[],"warn":[] , "est": [], 'close':[], 'address':filename.replace(stringToRemove,"")}


    sheets = pd.ExcelFile(filename)
    dataFrames_List = sheets.sheet_names
    sheets.close()
    estimate = 1
    tagged_dataframes = []
    for sheetname in dataFrames_List:
        message = f"Checking sheet \'{sheetname}\' in file \'{filename}\'"
        data['main'].append("{}".format(message) )
            
        dataframe = pd.read_excel(filename, sheet_name=sheetname)
        tags = 0
        unique_rows = 1
        for c in dataframe.columns:
            if "_tag" in c:
                tags = tags +1
                            
        if(tags > 0):
            df2 = dataframe.filter(regex='_tag')
            q = 'select * from df2'
            df_unique_rows = psql.sqldf(q)
            tagged_dataframes.append(df_unique_rows)

        columns = list(dataframe.columns.values)
        res = dataframe.columns.duplicated()
        if True in res:
            message = f"Error: Duplicate column names in \'{sheetname}\' in file \'{filename}\' !"
            data['err'].append("{}".format(message) )
            
        rows = dataframe.shape[0]
        columnos = dataframe.shape[1]
        rownum = len(dataframe.index)
        if (tags==0):
            estimate = estimate * rownum
        
        message = "Sheet {} has {} columns, {} rows, {} tags".format(sheetname, columnos, rows, tags)
        data['main'].append("{}".format(message) )
        
        
        #CHECK COLNAMES:
        i=0
        counter=1
        while i<len(columns):
            
            if (re.sub('[0-9]','',columns[i]))== 'sku':
                if((columns[i]) != 'sku{}'.format(counter)):
                    message = 'WARNING: Column headers are not correct.'
                    data['warn'].append("{}".format(message) )
                        
                else:
                    if(columns[i+1]) == 'sku_desc{}'.format(counter) and (columns[i+2]) == 'qty{}'.format(counter):
                        i = i + 3
                        counter = counter + 1
                        continue
                    else:
                        message = 'WARNING: Column headers are not correct.'
                        data['warn'].append("{}".format(message) )
                        
                        break
            i = i+1
            counter = counter + 1

            #CHECK COLUMNS
            for column in dataframe:
                if ((dataframe[column] == 0).all()):
                    message = f'WARNING: column \'{column}\': all values 0'
                    data['warn'].append("{}".format(message) )


                elif((dataframe[column] == None).all()):
                    message = f'WARNING: column \'{column}\': all values None'
                    data['warn'].append("{}".format(message) )


                elif(dataframe[column].isnull().all()):
                    message = f'WARNING: column \'{column}\': all values NaN'
                    data['warn'].append("{}".format(message) )

            #CHECK ROWS
            for index, row in dataframe.iterrows():
                row_series = dataframe.iloc[index, :]
                if(row_series.isnull().all()):
                    message = f'WARNING: row \'{index}\': all values NaN'
                    data['warn'].append("{}".format(message) ) 

                elif((row_series == 0).all()):
                    message = f'WARNING: row \'{index}\': all values 0'
                    data['warn'].append("{}".format(message) )

                elif((row_series == None).all()):
                    message = f'WARNING: row \'{index}\': all values None'
                    data['warn'].append("{}".format(message) ) 

    estimate = estimate * compute_join_nomerge(tagged_dataframes)
    estimate = 1 + estimate
 
    data['est'].append("{}".format(estimate) )

    #TERMINATE EVENT SOURCE
    data['close'].append("{}".format("OK")  )
    
    
    sheets = None

    return json.dumps(data) #True
    #end of function



#-------------------------------------------------------

#Helper function used by main processing function 
def remove_duplicates(t):
    s = []
    for i in t:
       if i not in s:
          s.append(i)
    return s

#Helper function used by main processing function 
def compute_join_nomerge(dataframes):
    val_counts = []
    dframes = []
    common_values = []

    for df in dataframes:
        df_tags_only = df.filter(regex='_tag')
        dframes.append(df_tags_only)
        for column in df_tags_only:
            dataframe = df_tags_only[column].value_counts()
            val_counts.append(dataframe)
            common_values.append(list(df_tags_only[column].unique()))
    flat_list = [item for sublist in common_values for item in sublist]
    common_values = remove_duplicates(flat_list)

    val_counts = pd.concat(val_counts)
    val_counts = pd.DataFrame({'level_of_service_tag':val_counts.index, 'prod': val_counts.values})
    val_counts = val_counts.groupby('level_of_service_tag', as_index=False).prod()
    total = val_counts['prod'].sum()
    return total

#Helper function used by main processing function 
def calculate_join(dataframe_set):
    ext_df = pd.DataFrame()
    for df in dataframe_set:
        if ext_df is None:
            ext_df = df.copy()
        else:
            try:
                ext_df = pd.merge(ext_df, df)
            except:
                df["key1"] = 0
                ext_df["key1"] = 0
                ext_df = pd.merge(ext_df, df)
    return ext_df.shape[0]

#-------------------------------------------------------
