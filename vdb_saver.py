import chromadb
import json

# Read the important information from the file
with open('important_information.json', 'r') as f:
    data = json.load(f)
important_info = data['important_info']

# Create a ChromaDB client and a collection
client = chromadb.PersistentClient()
collection = client.create_collection("important_info_collection")

# Add the important information to the collection
collection.add(
    documents=[important_info],
    metadatas=[{"source": "chatbot"}],
    ids=["important_info"],
)

print("Important information saved to the database.")