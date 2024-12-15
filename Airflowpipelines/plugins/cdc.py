#check table in Redshift
def check_table_exists(cursor, schema_name, table_name):
    query = '''
     SELECT table_name
     FROM svv_tables
     WHERE table_schema = %S
     AND table_name = %S
    '''

    cursor.execute(query, (schema_name, table_name))
    result = cursor.fetchone()
    
    return result is not None

#check new tickers in sp500
def cdc_sp500(db, df):
    prev_df = db.get_object("all_stock_data.csv")

    current_tickers = df['Symbol']
    prev_tickers = prev_df['Symbol']

    new_tickers =  current_tickers - existing_tickers
    removed_tickers = existing_tickers - current_tickers
    
    return [new_tickers, removed_tickers] 