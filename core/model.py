from sentence_transformers import SentenceTransformer

# Specify a directory to save the model
model_directory = "./my_saved_model"

try:
    # Load the model from the directory
    model = SentenceTransformer(model_directory)
    print("Model loaded from the local directory.")
except:
    # If loading fails, download the model and save it locally
    model = SentenceTransformer('all-MiniLM-L6-v2')  # Replace with your desired model
    model.save_pretrained(model_directory)
    print(f"Model downloaded and saved to {model_directory}.")

# Now you can use the model
sentences = ["This is an example sentence", "Each sentence is converted"]
embeddings = model.encode(sentences)
print(embeddings)