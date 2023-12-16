from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from caption_extract import extract_captions
from web_scraper import extract_text_from_webpage, save_text_to_file
import config
import os
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY
os.environ["SERPAPI_API_KEY"] = config.SERPAPI_API_KEY
file_path = './script.txt'



def content_extract(content_type, url):
    if content_type=='video':
        #user input
        extract_captions(url)


    elif content_type=='text':
        text_content = extract_text_from_webpage(url)
        if text_content:
            save_text_to_file(text_content)


def interacter_ask(url, content_type, query):

    # if content_type=='video':
    #     #user input
    #     extract_captions(url)


    # elif content_type=='text':
    #     text_content = extract_text_from_webpage(url)
    #     if text_content:
    #         save_text_to_file(text_content)

    content_extract(content_type, url)


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

    chain = load_qa_chain(OpenAI(), chain_type="stuff")

    # query = input('Ask anything:')
    docs = document_search.similarity_search(query)
    result = chain.run(input_documents=docs, question=query)
    print("result_ask: ", result)
    return result

def summarize(url, content_type):
    content_extract(content_type, url)

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

    chain = load_qa_chain(OpenAI(), chain_type="stuff")

    query = 'Summarize this Text in brief'
    docs = document_search.similarity_search(query)
    result = chain.run(input_documents=docs, question=query)
    print("result_summarizer: ", result)
    return result

if __name__=='__main__':
    summarize(url='https://www.youtube.com/watch?v=gs-IDg-FoIQ', content_type='video')
    interacter_ask(url='https://www.youtube.com/watch?v=gs-IDg-FoIQ', content_type='video', query='what is the method called?')
