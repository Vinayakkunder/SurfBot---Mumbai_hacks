from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from caption_extract import extract_captions

import os
os.environ["OPENAI_API_KEY"] = "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"
os.environ["SERPAPI_API_KEY"] = "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"

#user input
video_url = 'https://www.youtube.com/watch?v=SM6GYz-lZaM'
extract_captions(video_url)


# Specify the correct path to your text file
file_path = 'F:\Mumbai_hacks\script.txt'

try:
    # Open the file in read mode ('r')
    with open(file_path, 'r') as file:
        # Read the entire content of the file
        raw_test = file.read()


except FileNotFoundError:
    print(f"The file '{file_path}' does not exist.")
except Exception as e:
    print(f"An error occurred: {e}")

# We need to split the text using Character Text Split such that it sshould not increse token size
text_splitter = CharacterTextSplitter(
    separator = "\n",
    chunk_size = 800,
    chunk_overlap  = 200,
    length_function = len,
)
texts = text_splitter.split_text(raw_test)

print(len(texts))

# Download embeddings from OpenAI
embeddings = OpenAIEmbeddings()

document_search = FAISS.from_texts(texts, embeddings)

from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

chain = load_qa_chain(OpenAI(), chain_type="stuff")

query = "what are they exploring? give me the timestamp as well."
docs = document_search.similarity_search(query)
result = chain.run(input_documents=docs, question=query)
print("result: ", result)
