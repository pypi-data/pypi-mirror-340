from pinecone import Pinecone
from pinecone import ServerlessSpec
from pinecone.data.index import Index
from llama_index.core import StorageContext
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.vector_stores.postgres import PGVectorStore
import os
from enum import Enum


class Pineconer():
    def __init__(self,api_key = None):
        self.api_key = api_key or os.getenv("PINECONE_API_KEY")
        self.pc = Pinecone(api_key=self.api_key)

    def create(self):
        self.pc.create_index(
            "api-documents-index",
            dimension=1536, # 维度1536
            metric="euclidean",#欧式空间 "cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
    
    def load(self)->Index:
        pinecone_index = self.pc.Index("api-documents-index")
        return pinecone_index
    
    def get_storage(self,pinecone_index:Index)->StorageContext:
        vector_store = PineconeVectorStore(pinecone_index=pinecone_index,namespace = "test1")
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        return storage_context


class PGInfo(Enum):
    host = ''

class PortGreser():
    def __init__(self,info:PGInfo = None):
        self.info = info

    def create(self):
        pass

    
    def load(self):
        pass
    
    def get_storage(self,index_name:str)->StorageContext:
        vector_store = PGVectorStore.from_params(
            database="vector_db",
            host=self.info.host,
            password=self.info.password,
            port=self.info.port,
            user=self.info.user,
            table_name=index_name,
            embed_dim=1536,  # openai embedding dimension
            hnsw_kwargs={
                "hnsw_m": 16,
                "hnsw_ef_construction": 64,
                "hnsw_ef_search": 40,
                "hnsw_dist_method": "vector_cosine_ops",
                },
        )
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        return storage_context
