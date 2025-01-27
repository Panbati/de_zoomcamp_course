from pathlib import Path
from sqlalchemy import create_engine
from time import time
from urllib.request import urlretrieve

import pandas as pd
import argparse
import logging
import gzip

console = logging.StreamHandler()
console.setLevel(logging.INFO)
log = logging.getLogger()
parser = argparse.ArgumentParser(description='Ingest parquet data to PostgreSQL')

def main(params):
    user = params.username
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    chunk_size = params.chunk_size
    if_exists = params.if_exists

    file_type = Path(url).suffix
    file_name = f'output{file_type}'

    print(f'Starting {file_type} download')
    urlretrieve(url, file_name)

    try:
        df = pd.read_csv(file_name, compression='gzip'
                         , sep=','
                         , encoding='utf-8'
                         , engine='python'
                         , on_bad_lines='warn'
                         )
    except gzip.BadGzipFile:
        df = pd.read_csv(file_name
                         , sep=','
                         , encoding='utf-8'
                         , engine='python'
                         , on_bad_lines='warn'
                         )
    except Exception as e:
        df = pd.read_parquet(file_name, engine='pyarrow')
        log.exception('Not workie')

    print(f'{file_name} downloaded')
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    start_time = time()
    end_time = 0

    print('Starting database ingestion')
    try:
        df.to_sql(name=table_name, con=engine, if_exists=if_exists, index=False, chunksize=chunk_size)
        end_time = time()
    except Exception as e:
        log.exception('Database ingestion failed')
        exit()

    print('Database ingestion finished')
    print(round(end_time - start_time, 0), 'seconds to finish')

if __name__ == '__main__':
    parser.add_argument('--username', help='Username for the account')
    parser.add_argument('--password', help='Password for the account')
    parser.add_argument('--host', help='Database hosting endpoint')
    parser.add_argument('--port', help='Database port')
    parser.add_argument('--db', help='Database name')
    parser.add_argument('--table_name', help='Name of table ingesting the results')
    parser.add_argument('--url', help='Location of the parquet file')
    parser.add_argument('--chunk_size', type=int, default=100000, help='Determine the chunks of inserting to the database')
    parser.add_argument('--if_exists', default='replace', help='What to do if the ingested data already exists')

    args = parser.parse_args()
    main(args)