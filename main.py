from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from caption_extract import extract_captions
from web_scraper import extract_text_from_webpage, save_text_to_file


import os
os.environ["OPENAI_API_KEY"] = "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"
os.environ["SERPAPI_API_KEY"] = "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"
content_type = 'text' #video or text


if content_type=='video':
    #user input
    video_url = 'https://www.youtube.com/watch?v=gs-IDg-FoIQ'
    extract_captions(video_url)


elif content_type=='text':
    web_page_url = 'https://en.wikipedia.org/wiki/Deep_learning'
    text_content = extract_text_from_webpage(web_page_url)
    if text_content:
        save_text_to_file(text_content)


# Specify the correct path to your text file
file_path = './script.txt'

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

query = input('Ask anything:')
docs = document_search.similarity_search(query)
result = chain.run(input_documents=docs, question=query)
print("result: ", result)
