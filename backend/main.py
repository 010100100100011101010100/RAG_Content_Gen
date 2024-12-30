from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from annoy import AnnoyIndex
import numpy as np

def load_and_chunk(file_path):
    # Load and chunk the document
    loader = TextLoader(file_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
    chunks = splitter.split_documents(documents)
    return chunks

def generate_embeddings(chunks):
    # Generate embeddings for the text chunks
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    vectorized_chunks = [embeddings.embed_query(chunk.page_content) for chunk in chunks]
    return vectorized_chunks

def create_index(embeddings, dimension=512):
    # Create an Annoy index for the embeddings
    index = AnnoyIndex(dimension, 'angular')  

    for i, embedding in enumerate(embeddings):
        index.add_item(i, embedding)
    
    index.build(10)  
    return index

def query_index(index, embeddings, chunks, query_text):
    # Query the Annoy index
    query_embedding = embeddings.embed_query(query_text)

    
    indices = index.get_nns_by_vector(query_embedding, 3)
    
    results = [(chunks[idx].page_content, idx) for idx in indices]
    return results

def process_content(text):
    

    # Step 1: Load and Chunk Document (text is the input here)
    chunks = load_and_chunk(text)

    # Step 2: Generate Embeddings for Chunks
    embeddings = generate_embeddings(chunks)

    # Step 3: Create Annoy Index
    index = create_index(embeddings)

    # Step 4: Query the Index (You could use a fixed query or pass dynamic queries)
    query_text = "What is this document about?"
    results = query_index(index, embeddings, chunks, query_text)
    print("Content processed")
    return {"results": results}
