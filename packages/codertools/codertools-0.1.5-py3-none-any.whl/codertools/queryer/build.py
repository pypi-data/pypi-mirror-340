import os
from llama_index.core import SimpleDirectoryReader
from llama_index.core import VectorStoreIndex
from .reader import CustObsidianReader
import shutil

async def build(file_path:str,persist_dir="./obsidian_kb"):

    file_extractor = {
        ".md": CustObsidianReader()  # 使用自定义Reader
    }
    reader = SimpleDirectoryReader(
        input_dir=file_path,
        file_extractor=file_extractor,
        recursive=True,
    )
    documents = reader.load_data()
    documents = documents[:10]
    index = VectorStoreIndex.from_documents(documents)
    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)
    index.storage_context.persist(persist_dir=persist_dir)

    return len(documents)


