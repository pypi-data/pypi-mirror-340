from llama_index.core import load_index_from_storage, StorageContext
from llama_index.core import SimpleDirectoryReader
from llama_index.core import VectorStoreIndex
from llama_index.core.readers.base import BaseReader
from llama_index.core import Document
from typing import List, Dict,Optional
import yaml
import shutil
import os


def get_data_from_md(text):
    _,infos,content = text.split("---",2)
    data = yaml.safe_load(infos)
    return data, content
    

class CustObsidianReader(BaseReader):
    def load_data(self, file_path: str,
                        extra_info: Optional[Dict] = None) -> List[Document]:
        # 自定义读取逻辑
        with open(file_path, 'r') as file:
            text = file.read()
        data,content = get_data_from_md(text)
        # 使用状态
        status = data.get('编辑状态',None)
        topic = data.get('topic','')
        describe = data.get('describe','')
        creation_date = data.get("creation date",'')
        tags = data.get('tags', [])
        link = data.get('链接','')
        content_cut = content[:6000]
        if len(content_cut) != len(content):
            print(topic,'is too long ***')


        document = Document(text=f"topic: {topic} content: {content}", 
                            metadata={"topic":topic,
                                      "status":status,
                                      "creation_date":str(creation_date),
                                      "tags":tags,
                                      "link":link},
                           )
        return [document]


async def load(persist_dir:str,similarity_top_k=3):

    storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
    index = load_index_from_storage(storage_context)
    
    return index.as_query_engine(similarity_top_k = similarity_top_k)    

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


