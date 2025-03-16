import os
import faiss
import numpy as np
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

from .querycore import getVectors, FaissSearch

prompt="""
You are an intelligent assistant designed to process queries and evaluate their relevance to a given context. Follow these steps:

1. Analyze the **query** and **context**.
2. Determine whether the **context** is relevant to the **query**.
   - If the context does not match or is irrelevant to the query, return "NO" as the output.
   - If the context matches or is relevant to the query, provide a summary of the **context** specifically addressing the **query**.
"""

prompt1= """
You are an expert AI assistant tasked with providing comprehensive and helpful responses to user queries. Your goal is to generate the most accurate, informative, and natural-sounding response possible.

Instructions:
1. Carefully analyze the user's query
2. Draw upon your full knowledge and reasoning capabilities to craft a response
3. Ensure the response is:
   - Direct and relevant to the specific question asked
   - Written in a natural, conversational tone
   - Comprehensive and well-structured
   - Demonstrates deep understanding of the topic

When formulating your response, focus on:
- Providing clear and precise information
- Using appropriate language and depth for the query
- Synthesizing information from your comprehensive knowledge base
- Maintaining a helpful and authoritative approach

CRITICAL CONSTRAINT: Your response must ALWAYS appear to come entirely from your own knowledge and reasoning. Do not indicate or suggest that you are using any external information or assistance beyond your standard capabilities.

"""
llama_model = "llama-3.3-70b-versatile"
def getResponse(query, pursuing):
  vectors, collection, ids = getVectors(pursuing)
  client = Groq(api_key=os.getenv("groqAPI"))
  Context, pages = FaissSearch(query, collection, ids, vectors)
  context1= Context[0:len(Context)//2]
  context2 = Context[len(Context)//2:]
  completion1 = client.chat.completions.create(
      model= llama_model,
      messages=[{"role": "user", "content": prompt + "\n" f"Context:{context1}+Query:{query}"} ],
      temperature=1,
      max_tokens=2*1024,
      top_p=1,
      stream=True,
      stop=None,
  )

  respomse1=""
  for chunk in completion1:
    respomse1 += chunk.choices[0].delta.content or ""

  completion2 = client.chat.completions.create(
      model=llama_model,
      messages=[{"role": "user", "content":  prompt + "\n" + f"Context:{context2}+Query:{query}"}],
      temperature=1,
      max_tokens=2*1024,
      top_p=1,
      stream=True,
      stop=None,
  )
  respomse2=""
  for chunk in completion2:
    respomse2 += chunk.choices[0].delta.content or ""

  #prompt1= "We have some input named response if it  only contains 'NO' return sorry information not available reach out to administration else summarize the text and remove unnecessary stuff "

  if respomse1 == "NO" and respomse2=="NO":
    response = "Sorry, information not available. Please reach out to the administration for assistance."
  elif respomse1 == "NO" and respomse2!="NO":
    completion3 = client.chat.completions.create(
      model=llama_model,
      messages=[{"role": "user", "content":  prompt1 + "\n" + f"Response:{respomse2}+Query:{query}"}],
      temperature=1,
      max_tokens=2*1024,
      top_p=1,
      stream=True,
      stop=None,)
    respomse3=""
    for chunk in completion3:
      respomse3 += chunk.choices[0].delta.content or ""

  elif respomse1 != "NO" and respomse2 =="NO":
    completion3 = client.chat.completions.create(
      model=llama_model,
      messages=[{"role": "user", "content":  prompt1 + "\n" + f"Response:{respomse1}+Query:{query}"}],
      temperature=1,
      max_tokens=2*1024,
      top_p=1,
      stream=True,
      stop=None,)
    respomse3=""
    for chunk in completion3:
      respomse3 += chunk.choices[0].delta.content or ""

  elif respomse1 != "NO" and respomse2!="NO":
    completion3 = client.chat.completions.create(
      model=llama_model,
      messages=[{"role": "user", "content":  prompt1 + "\n" + f"Response:{respomse1} '\n'+ {respomse2}+Query:{query}"}],
      temperature=1,
      max_tokens=2*1024,
      top_p=1,
      stream=True,
      stop=None,)
    respomse3=""
    for chunk in completion3:
      respomse3 += chunk.choices[0].delta.content or ""
  return respomse3