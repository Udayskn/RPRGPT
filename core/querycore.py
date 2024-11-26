import os
import faiss
import numpy as np
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

##Getting the vectorization model from the directory
model_directory = "./my_saved_model"
model = SentenceTransformer(model_directory)

# Connect to DB
client = MongoClient("mongodb+srv://praneethn116:ZJRHLvlrd4LGXGPq@cluster0.d0bev.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
# Selecting my database
db = client.Cluster0
collection = db["academics"]

ids = []
vectors = []
for document in collection.find():
  vector = np.array(document['vector'])
  ids.append(document['_id'])
  vectors.append(vector)
vectors = np.array(vectors, dtype='float32')

def FaissSearch(query, vectors=vectors, k=10):
  
  # Converting the query into a vector
  query_vector = model.encode(query)
  query_vector = np.array(query_vector, dtype='float32')

  faiss.normalize_L2(vectors)
  # 3. Build a FAISS index
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
  pages = set(pages)

  return Context, pages

query = "Tell me about credits and courses for Electrical Engineering"

Context, pages = FaissSearch(query,k=5)

print(Context)