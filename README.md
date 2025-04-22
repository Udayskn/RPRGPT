# RPR GPT - Retrieval-Augmented Generation System

## Frontend System
Refer to
git - https://github.com/susanth-24/RPRGPT-FE

## Overview
RPR GPT is a Retrieval-Augmented Generation (RAG) system designed to simplify access to complex academic resources like UG/PG handbooks, faculty websites, and campus information. It leverages cutting-edge AI technologies to retrieve relevant information and generate context-aware responses efficiently.

## Goals
The project aims to:
- Provide a user-friendly system for retrieving academic information.
- Enhance data accessibility using **RAG** and **Chain-of-Thought (CoT)** techniques.
- Bridge gaps in knowledge by making institutional resources more comprehensible.

## Key Features
- **Data Collection**: Automated extraction of data from handbooks, faculty profiles, and campus websites.
- **Preprocessing & Embedding**: Structured data processing and semantic embedding generation for efficient retrieval.
- **Context-Aware Responses**: Accurate, user-friendly answers powered by **Groq**, an advanced language model.
- **Interactive Interface**: Dynamic frontend for seamless user interaction.
- **Scalable Deployment**: Hosted on Amazon S3 for accessibility and scalability.

## Technologies Used
- **Language Model**: Groq for response generation.
- **Embeddings**: SentenceTransformer (all-MiniLM-L6-v2) for semantic data representation.
- **Database**: MongoDB for storing embeddings and metadata.
- **Web Scraping**: BeautifulSoup and Requests for data extraction.
- **PDF Parsing**: pdfplumber for handling document-based data.
- **Backend**: Flask for API handling and backend logic.
- **Frontend**: ReactJS for creating a user-friendly interface.
- **Hosting**: Amazon S3 for deployment.

## System Workflow
1. **Data Collection**: Extract data using web scraping and PDF parsing.
2. **Preprocessing**: Clean and tokenize data into manageable chunks.
3. **Embedding Generation**: Create semantic embeddings for data using SentenceTransformer.
4. **Data Storage**: Store processed embeddings and metadata in MongoDB.
5. **Query Processing**: Convert user queries into embeddings and perform similarity searches to retrieve relevant data.
6. **Response Generation**: Use **Groq** to generate precise, context-aware responses.
7. **Frontend Interaction**: Present responses to users via a ReactJS-based interface.

## Contributions
- **Satya (2021EEB1172)**: Data collection, web scraping.
- **Praneeth (2021EEB1189)**: Data preprocessing, embedding generation, RAG pipeline integration.
- **Pratheek (2021EEB1224)**: Model evaluation, CoT prompting.
- **Uday (2021MCB1253)**: Backend development.
- **Susanth (2021CHB1053)**: Deployment and testing.
- **Rishik (2021CSB1142)**: Frontend development.

## Future Enhancements
- **Public Chat Feature**: Enable group discussions for users.
- **Expanded Data Sources**: Integrate additional institutional data like faculty research and news.
- **Enhanced Features**: Add more interactive functionalities, such as visual analytics and notification systems.

## GitHub Repositories
- [Backend Repository](https://github.com/susanth-24/RPRGPT-BE)
- [Frontend Repository](https://github.com/susanth-24/RPRGPT-FE)

## Conclusion
RPR GPT demonstrates how advanced AI techniques can transform access to academic information, fostering better knowledge sharing and user engagement. Our system sets a foundation for smarter, scalable solutions in educational environments.
