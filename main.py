from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from caption_extract import extract_captions
from web_scraper import extract_text_from_webpage, save_text_to_file
import config
import os
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
# from googletrans import Translator
import speech_recognition as sr
import pyttsx3 
# from ai4bharat.transliteration import XlitEngine

os.environ["OPENAI_API_KEY"] = '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'
os.environ["SERPAPI_API_KEY"] = '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'
file_path = './script.txt'



def content_extract(content_type, url):
    if content_type=='video':
        #user input
        extract_captions(url)


    elif content_type=='text':
        text_content = extract_text_from_webpage(url)
        if text_content:
            save_text_to_file(text_content)

# def translate(text):
#     translator = Translator()

#     translate_text = ""
#     translate_text += " " + translator.translate(text, dest='hi').text
#     print(translate_text)

    # e = XlitEngine("hi", beam_width=10, rescore=True)
    # out = e.translit_word(text, topk=5)
    # print(out)

def SpeakText(command):
	
	# Initialize the engine
	engine = pyttsx3.init()
	engine.say(command) 
	engine.runAndWait()

def speech_input():
    r = sr.Recognizer()
    while(1): 
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.1)
                
                #listens for the user's input 
                print("listening...")
                audio2 = r.listen(source2)
                
                # Using google to recognize audio
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()

                print("you said: ",MyText)
                return MyText

        
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            return 0
		
        except sr.UnknownValueError:
            print("unknown error occurred")
            return 0




def interacter_ask(url, query):
    if 'youtube' in url:
        content_type = 'video'
    else:
        content_type = 'text'
    content_extract(content_type, url)
    
    try:
        # Open the file in read mode ('r')
        with open(file_path, 'r', encoding='utf-8') as file:
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

    # print(len(texts))

    # Download embeddings from OpenAI
    embeddings = OpenAIEmbeddings()

    document_search = FAISS.from_texts(texts, embeddings)

    chain = load_qa_chain(OpenAI(), chain_type="stuff")

    # query = input('Ask anything:')
    docs = document_search.similarity_search(query)
    result = chain.run(input_documents=docs, question=query)
    print("result_ask: ", result)
    # SpeakText(result)
    return result

def summarize(url):
    if 'youtube' in url:
        content_type = 'video'
    else:
        content_type = 'text'
    content_extract(content_type, url)

    # try:
    # Open the file in read mode ('r')
    with open(file_path, 'r', encoding='utf-8') as file:
        # Read the entire content of the file
        raw_test = file.read()


    # except FileNotFoundError:
    #     print(f"The file '{file_path}' does not exist.")
    # except Exception as e:
    #     print(f"An error occurred: {e}")

    # We need to split the text using Character Text Split such that it sshould not increse token size
    text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 800,
        chunk_overlap  = 200,
        length_function = len,
    )
    texts = text_splitter.split_text(raw_test)

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
    # op = summarize(url='https://en.wikipedia.org/wiki/Ashlesha_Thakur', content_type='text')
    # print(op)
    # text_inp = speech_input()
    text_inp = 'summarize the content'
    interacter_ask(url='https://aws.amazon.com/blogs/machine-learning/', content_type='text', query=text_inp)
    # translate(text='programming kya hota hai?')
