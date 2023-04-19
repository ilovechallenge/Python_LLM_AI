import pickle
import os
import inspect

from lmql.runtime.lmql_runtime import LMQLQueryFunction
from lmql import LMQLResult

# cache query results by query code and arguments
global cache_file
cache_file = None
global cache
cache = None

stats = {
    "total": 0,
    "cached": 0
}

def set_cache(path):
    global cache, cache_file
    cache_file = path
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "rb") as f:
                cache = pickle.load(f)
        except:
            print("warning: failed to load cache file {}".format(cache_file))
            cache = {}
    else:
        cache = {}

def caching(state):
    global cache
    global cache_file

    if state:
        set_cache(".lmql-algorithms-cache")
    else:
        cache_file = None
        cache = None

def persist_cache():
    global cache
    global cache_file
    if cache is not None and cache_file is not None:
        with open(cache_file, "wb") as f:
            pickle.dump(cache, f)

async def apply(q, *args):
    # handle non-LMQL queries
    if type(q) is not LMQLQueryFunction:
        if inspect.iscoroutinefunction(q):
            return await q(*args)
        return q(*args)

    global stats
    stats["total"] += 1

    # get source code for q.__fct__
    try:
        # convert dict to list
        key_args = [tuple(sorted(list(a.items()))) if type(a) is dict else a for a in args]
        key_args = [tuple(a) if type(a) is list else a for a in key_args]
        key = (q.lmql_code, *key_args).__hash__()
        key = (q.lmql_code, *key_args)
    except:
        print("warning: cannot hash LMQL query arguments {}. Change the argument types to be hashable.".format(args))
        key = str(q.lmql_code) + str(args)
    
    if key in cache.keys():
        stats["cached"] += 1
        return cache[key]
    else:
        result = await q(*args)
        if len(result) == 1:
            result = result[0]
        if type(result) is LMQLResult:
            if "RESULT" in result.variables.keys():
                result = result.variables["RESULT"].strip()

        cache[key] = result
        persist_cache()

        return result

def get_stats():
    global stats
    return "lmql.algorithms Stats: Total queries: {}, Cached queries: {}".format(stats["total"], stats["cached"])