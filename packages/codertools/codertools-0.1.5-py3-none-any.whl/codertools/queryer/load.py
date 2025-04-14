from llama_index.core import load_index_from_storage, StorageContext


async def load(persist_dir:str,similarity_top_k=3):

    storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
    index = load_index_from_storage(storage_context)
    
    return index.as_query_engine(similarity_top_k = similarity_top_k)    
