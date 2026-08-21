from langchain_core.globals import set_llm_cache
from langchain_core.caches import InMemoryCache
from langchain_community.cache import SQLiteCache

# Global instances to avoid re-initializing
_in_memory_cache = InMemoryCache()
_sqlite_cache = SQLiteCache(database_path=".langchain.db")

def configure_cache(cache_type: str):
    """
    Configures LangChain global cache.
    cache_type must be either 'InMemory' or 'SQLite' or 'None'.
    """
    if cache_type == "InMemory":
        set_llm_cache(_in_memory_cache)
    elif cache_type == "SQLite":
        set_llm_cache(_sqlite_cache)
    else:
        set_llm_cache(None)
