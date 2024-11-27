import os
import faiss
import numpy as np
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import nltk
from nltk import tokenize
nltk.download('punkt_tab')
from dotenv import load_dotenv
import os
import pdfplumber

load_dotenv()

##Getting the vectorization model from the directory
model_directory = "./my_saved_model"
model = SentenceTransformer(model_directory)

def extract_pdf_content(pdf_path):
    # Open the PDF
    with pdfplumber.open(pdf_path) as pdf:
        text_chunks = []
        images = []
        metadata = []

        for page_num, page in enumerate(pdf.pages):
            # Extract text
            text = page.extract_text()
            if text:
                text_chunks.append({
                    "text": text,
                    "page_number": page_num + 1  ## We are also keeping track of the page no.s
                })

    return text_chunks

def split_into_chunks(text_chunks, max_length=512):
    chunks = []
    for item in text_chunks:
        page_text = item["text"]
        page_num = item["page_number"]
        sentences = tokenize.sent_tokenize(page_text)

        current_chunk = []
        current_length = 0
        for sentence in sentences:
            if current_length + len(sentence.split()) > max_length:
                chunks.append({
                    "text": " ".join(current_chunk),
                    "page_number": page_num
                })
                current_chunk = []
                current_length = 0
            current_chunk.append(sentence)
            current_length += len(sentence.split())

        if current_chunk:  # Add remaining chunk
            chunks.append({
                "text": " ".join(current_chunk),
                "page_number": page_num
            })

    return chunks

def createCollection(collection_name):
    # Connect to DB
    client = MongoClient(os.getenv('MongoURI'))
    # Selecting my database
    db = client.Cluster0

    # Defining the JSON schema
    doc_schema = {
        "bsonType": "object",
        "required": [ "page_number", "text", "vector"],
        "properties": {
            "page_number": {
                "bsonType": "int",
                "minimum": 1,
                "description": "must be an integer and at least 18"
            },
            "text": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "vector": {
                "bsonType": "array",
                "description": "must be an array of numbers and is required"
            }
        }
    }
    # Create the collection with schema validation
    db.create_collection(collection_name, validator={"$jsonSchema": doc_schema})
    return db[collection_name]

def push_vectors_to_db(chunks, collection):
    for chunk in chunks:
      try:
        collection.insert_one({
          "page_number": chunk["page_number"],
          "text": chunk["text"],
          "vector": model.encode(chunk["text"]).tolist()
        })
        print("vector inserted successfully")
      except Exception as e:
        print(f"Error inserting document: {e}")
