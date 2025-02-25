import os
import time
from datetime import datetime, timedelta

import fire
import pandas
import tushare as ts
from dolthub_client import get_index_last_update_date
from tqdm import tqdm

ts.set_token(os.environ["TUSHARE"])
pro=ts.pro_api()
file_path = os.path.dirname(os.path.realpath(__file__))

index_list = [
    '000905.SH', # csi500
    '399300.SZ', # csi300
    '000906.SH', # csi800
    '000852.SH', # csi1000
    '000985.SH', # csiall
    ]


def dump_index_data(output_path=f"{file_path}/index_weight", user="kidylee", database="investment_data", branch="master"):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    last_update_date = get_index_last_update_date(user, database, branch)

    time_step = timedelta(days=15)

    for index_name in tqdm(index_list):
        start_date = last_update_date.get(index_name,'1990-01-01')
        start_date = datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=1) # update from the next day
        index_end_date = start_date + time_step

        filename = f'{output_path}/{index_name}.csv'
        result_df_list = []
        while index_end_date < datetime.now():
            df = pro.index_weight(index_code=index_name, start_date = start_date.strftime('%Y%m%d'), end_date=index_end_date.strftime('%Y%m%d'))
            start_date += time_step
            index_end_date += time_step
            if df.empty:
                continue
            result_df_list.append(df)
            time.sleep(0.5)
        if len(result_df_list) == 0:
            continue
        result_df = pandas.concat(result_df_list)
        result_df["stock_code"] = result_df["con_code"]
        result_df.to_csv(filename, index=False)

if __name__ == '__main__':
    fire.Fire(dump_index_data)
