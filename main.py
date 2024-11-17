import os
import tiktoken
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings, ChatNVIDIA
from langchain_community.vectorstores import FAISS
from caption_extract import extract_captions
from web_scraper import extract_text_from_webpage, save_text_to_file
from langchain.chains.question_answering import load_qa_chain
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load the NVIDIA API key
os.environ['NVIDIA_API_KEY'] = 'api_key_here'
file_path = './script.txt'

# Initialize the tokenizer from tiktoken
tokenizer = tiktoken.get_encoding("cl100k_base")  # This is for models like GPT, adjust if necessary

def tokenize_text(text):
    """
    Tokenizes the input text and returns the token count.
    """
    return len(tokenizer.encode(text))

def split_text_by_tokens(text, max_tokens=512):
    """
    Split the text into chunks of max `max_tokens` tokens, ensuring that no chunk exceeds the token limit.
    """
    chunks = []
    current_chunk = []
    current_tokens = 0

    # Split the text into sentences or lines, and process each segment
    for line in text.split("\n"):
        line_tokens = tokenize_text(line)

        # If adding the current line exceeds the max token size, start a new chunk
        if current_tokens + line_tokens > max_tokens:
            if current_chunk:
                chunks.append(" ".join(current_chunk))  # Add the current chunk to the list
            current_chunk = [line]  # Start a new chunk
            current_tokens = line_tokens
        else:
            current_chunk.append(line)
            current_tokens += line_tokens

    # Add the last chunk if it exists and is non-empty
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    # Ensure all chunks are non-empty
    return [chunk for chunk in chunks if chunk.strip()]

def content_extract(content_type, url):
    """
    Extracts the content based on the type (text or video).
    """
    if content_type == 'video':
        # Extract captions from video (e.g., YouTube)
        extract_captions(url)
    elif content_type == 'text':
        # Extract text from the provided URL and save it
        text_content = extract_text_from_webpage(url)
        if text_content:
            save_text_to_file(text_content)

def summarize(url, content_type):
    """
    Summarizes the content of the provided URL.
    """
    if content_type == 'youtube':
        content_type = 'video'
    else:
        content_type = 'text'

    content_extract(content_type, url)

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read the entire content of the file
            raw_test = file.read()

    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Split the text into chunks that fit within the token limit
    texts = split_text_by_tokens(raw_test, max_tokens=512)

    # Ensure there are no empty chunks before processing
    if not texts:
        print("No valid text chunks found. Please check the content extraction process.")
        return None

    # Download embeddings from NVIDIA
    embeddings = NVIDIAEmbeddings()

    # Process the documents in smaller chunks
    document_search = FAISS.from_texts(texts, embeddings)

    chain = load_qa_chain(ChatNVIDIA(model="meta/llama3-70b-instruct"), chain_type="stuff")

    query = 'Summarize this text in brief'
    docs = document_search.similarity_search(query)
    result = chain.run(input_documents=docs, question=query)
    print("Summary result: ", result)
    return result

def interacter_ask(url, query):
    """
    Uses the provided URL and query to return an answer based on the extracted content.
    """
    if 'youtube' in url:
        content_type = 'video'
    else:
        content_type = 'text'

    content_extract(content_type, url)

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read the entire content of the file
            raw_test = file.read()

    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Split the text into chunks that fit within the token limit
    texts = split_text_by_tokens(raw_test, max_tokens=512)

    # Ensure there are no empty chunks before processing
    if not texts:
        print("No valid text chunks found. Please check the content extraction process.")
        return None

    # Download embeddings from NVIDIA
    embeddings = NVIDIAEmbeddings()

    # Process the documents in smaller chunks
    document_search = FAISS.from_texts(texts, embeddings)

    chain = load_qa_chain(ChatNVIDIA(model="meta/llama3-70b-instruct"), chain_type="stuff")

    docs = document_search.similarity_search(query)
    result = chain.run(input_documents=docs, question=query)
    print("Result from ask: ", result)
    return result

def SpeakText(command):
    """
    Convert the result text to speech.
    """
    # Initialize the text-to-speech engine (optional)
    import pyttsx3
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

def speech_input():
    """
    Get speech input from the user.
    """
    import speech_recognition as sr

    r = sr.Recognizer()
    while True:
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.1)

                print("Listening...")
                audio2 = r.listen(source2)

                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()

                print("You said:", MyText)
                return MyText

        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
        except sr.UnknownValueError:
            print("Unknown error occurred")
            return None

if __name__ == '__main__':
    # Example usage of the summarize and interacter_ask functions
    op = summarize(url='https://www.youtube.com/watch?v=KWgYha0clzw', content_type='video')
    result = interacter_ask(url='https://aws.amazon.com/blogs/machine-learning/', query='What is the latest news on AWS Machine Learning?')
