from dotenv import load_dotenv
from readerllamaindex.pineconer import Pineconer

load_dotenv()


def test_pinecone():
    pine = Pineconer()
    index = pine.load()
    storage_context = pine.get_storage(index)
