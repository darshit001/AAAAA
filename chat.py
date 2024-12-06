from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb
import uuid

# Input the path of your PDF file
pdf_docs = ['Redmon_You_Only_Look_CVPR_2016_paper.pdf']  # Add your PDF files in this list

text = ""

for pdf in pdf_docs:
    # Create a PdfReader object to read the PDF
    pdf_reader = PdfReader(pdf)
    
    # Loop through each page in the PDF
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        
        # Extract the text from the page
        text += page.extract_text()
        text_spliter=RecursiveCharacterTextSplitter(
      chunk_size=500,
      chunk_overlap=100,
      separators=["\n\n", "\n", ". ", " ", ""]

  )

chunks=text_spliter.split_text(text)
# for i, chunk in enumerate(chunks):
#     print(f"Chunk {i + 1}:")
#     print(chunk)
#     print("\n" + "-"*20 + "\n")

ids = [str(uuid.uuid4()) for _ in range(len(chunks))]

model = SentenceTransformer('all-MiniLM-L6-v2')
embedding = model.encode(chunks)
clinet=chromadb.Client()
collection = clinet.create_collection(name="pdf")
collection.add(
    documents=chunks,            # All the text chunks
    metadatas=[{"chunk_id": i} for i in range(len(chunks))],  # Metadata for each chunk
    embeddings=embedding,
    ids=ids       # The corresponding embeddings
)
# print(ids[1])
# results = collection.get(include=["documents", "metadatas", "embeddings"])
# results = collection.get(ids=ids[1], include=["documents", "metadatas","embeddings"])
# print(results)
# Print the documents and their corresponding metadata
# for i in range(len(results["documents"])):
#     print(f"Document {i+1}: {results['documents'][i]}")
#     print(f"Metadata: {results['metadatas'][i]}")
#     print(f"Embedding: {results['embeddings'][i]}")
#     print("\n" + "-"*20 + "\n")

results = collection.query(
    query_texts=["what is YOLO "], # Chroma will embed this for you
    n_results=2 # how many results to return
)
print(results)


























