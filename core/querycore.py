import os
import faiss
import numpy as np
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

os.environ["TOKENIZERS_PARALLELISM"] = "false"

##Getting the vectorization model from the directory
model_directory = "./my_saved_model"
model = SentenceTransformer(model_directory)

def getVectors(collection_name):
  client = MongoClient(os.getenv("MongoURI"))
  db = client.get_database("Cluster0")
  collection = db.get_collection(collection_name)

  ids = []
  vectors = []
  for document in collection.find():
   vector = np.array(document['vector'])
   ids.append(document['_id'])
   vectors.append(vector)
  vectors = np.array(vectors, dtype='float32')

  return vectors,collection, ids

def FaissSearch(query:str,collection, ids, vectors, k=10):
  
  # Converting the query into a vector
  query_vector = model.encode(query)
  query_vector = np.array(query_vector, dtype='float32')

  faiss.normalize_L2(vectors)
  # Build a FAISS index
  dimension = vectors.shape[1]  # Assuming vectors are of uniform length
  index = faiss.IndexFlatIP(dimension)  # Cosine similarity
  index.add(vectors)

  # Normalize the query vector
  faiss.normalize_L2(query_vector.reshape(1, -1))

  # Conduct similarity search
  # k Number of nearest neighbors to retrieve
  distances, indices = index.search(query_vector.reshape(1, -1), k)

  # Map indices back to IDs
  result_ids = [ids[i] for i in indices[0]]

  Context = ""
  pages = []
  cursor = collection.find({"_id": {"$in": result_ids}})
  # Process the cursor as before (iterate or convert to list)
  for document in cursor:
    Context += document['text']
    pages.append(document['page_number'])
  pages = list(pages)

  return Context, pages
