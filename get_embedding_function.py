from langchain_huggingface.embeddings import HuggingFaceEmbeddings


def get_embedding_function():
    embeddings = HuggingFaceEmbeddings()
    return embeddings
