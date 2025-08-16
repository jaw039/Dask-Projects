import json
import ctypes
from dask.distributed import Client
import dask.dataframe as dd

def trim_memory() -> int:
    libc = ctypes.CDLL("libc.so.6")
    return libc.malloc_trim(0)

def PA0(path_to_user_reviews_csv):
    client = Client()
    # Helps fix any memory leaks.
    client.run(trim_memory)
    client = client.restart()

    def helpful_total(part):
        helpful_str = part['helpful'].fillna('[0, 0]').str.strip('[]')
        split_vals = helpful_str.str.split(', ')
    
        part['helpful_votes'] = split_vals.str[0].astype(int)
        part['total_votes'] = split_vals.str[1].astype(int)
        return part


    needed_cols = ['reviewerID', 'helpful', 'overall', 'reviewTime']
    df = dd.read_csv(path_to_user_reviews_csv, usecols = needed_cols)
    df['year'] = df['reviewTime'].str[-4:].astype(int)
    df = df.drop(columns = ['reviewTime'], axis = 1)
    meta = df._meta.assign(helpful_votes=0, total_votes=0)
    df = df.map_partitions(helpful_total, meta=meta)
    df = df.drop(columns = ['helpful'], axis = 1)
    df = df.repartition(npartitions = 25)
    df = df.persist()

    grouped = df.groupby('reviewerID', sort = False).agg({
        'overall': ['count', 'mean'],
        'year': 'min',
        'helpful_votes': 'sum',
        'total_votes': 'sum'
    }, split_out = 25).reset_index()
    grouped.columns = ['reviewerID', 'number_products_rated', 'avg_ratings', 'reviewing_since', 'helpful_votes', 'total_votes']
    
    submit = grouped.describe().compute().round(2)    
    with open('results_PA0.json', 'w') as outfile: 
        json.dump(json.loads(submit.to_json()), outfile)