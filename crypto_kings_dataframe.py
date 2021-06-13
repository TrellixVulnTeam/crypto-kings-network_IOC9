import pandas as pd
import crypto_kings as ck

def main():
    """main"""
    db = ck.Database("crypto_kings.db")

    df_coins = pd.read_sql_query("SELECT * FROM coins", db.conn)
    df_holders = pd.read_sql_query("SELECT * FROM holders", db.conn)
    df_data = pd.read_sql_query("SELECT * FROM data", db.conn)

    out = (df_data.merge(df_holders, left_on='holder_id', right_on='id', how='outer'))
    out = (out.merge(df_coins, left_on='coin_id', right_on='id', how='outer'))

           #.reindex(columns=['id', 'store', 'address', 'warehouse']))

    out.to_excel('EXCEL/out.xlsx')

if __name__ == '__main__':
    """check"""
    main()