from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain_community.llms import HuggingFaceEndpoint
from langchain_voyageai import VoyageAIEmbeddings

from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
#from utils.load_config import LoadConfig
from utils.load_config import LoadConfig
from utils.clean_refer import *
import os
import time
import re
from dotenv import load_dotenv

APPCFG = LoadConfig()
class ChatBot:
    """
    Class representing a chatbot with document retrieval and response generation capabilities.

    This class provides static methods for responding to user queries, handling feedback, and
    cleaning references from retrieved documents.
    """
    @staticmethod
    def respond(chatbot: list, message: str, data_type: str = "Preprocessed doc", temperature: float = 0.0) -> tuple:
        """
        Generate a response to a user query using document retrieval and language model completion.

        Parameters:
            chatbot (List): List representing the chatbot's conversation history.
            message (str): The user's query.
            data_type (str): Type of data used for document retrieval ("Preprocessed doc" or "Upload doc: Process for RAG").
            temperature (float): Temperature parameter for language model completion.

        Returns:
            Tuple: A tuple containing an empty string, the updated chat history, and references from retrieved documents.
        """
        load_dotenv()
        voyage_api_key = os.getenv("VOYAGE_API_KEY")
        embedding = VoyageAIEmbeddings(voyage_api_key=voyage_api_key, model="voyage-large-2-instruct")
        # embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        if data_type == "Preprocessed doc":
            # directories
            if os.path.exists(APPCFG.persist_directory):
                vectordb = FAISS.load_local(APPCFG.persist_directory,embedding,allow_dangerous_deserialization=True)
        
            else:
                chatbot.append(
                    (message, f"VectorDB does not exist. Please first execute the 'upload_data_manually.py' module. For further information please visit {hyperlink}."))
                return "", chatbot, None

        elif data_type == "Upload doc: Process for RAG":
            if os.path.exists(APPCFG.custom_persist_directory):
                vectordb = FAISS.load_local(APPCFG.custom_persist_directory,embedding,allow_dangerous_deserialization=True)
        
            else:
                chatbot.append(
                    (message, f"No file was uploaded. Please first upload your files using the 'upload' button."))
                return "", chatbot, None



        load_dotenv()
        groq_api_key = os.getenv("GROQ_API_KEY")
        llm = ChatGroq(groq_api_key= groq_api_key, model_name= "Gemma-7b-it")

        # Create a conversation buffer memory
        memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

        # Define a custom template for the question prompt
        custom_template = APPCFG.llm_system_role

        # Create a PromptTemplate from the custom template
        CUSTOM_QUESTION_PROMPT = PromptTemplate.from_template(custom_template)

        # Create a ConversationalRetrievalChain from an LLM with the specified components
        conversational_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            chain_type="stuff",
            retriever=vectordb.as_retriever(),
            memory=memory,
            condense_question_prompt=CUSTOM_QUESTION_PROMPT
        )
        response = conversational_chain({"question":message})
        # print(response)
        # Ensure the response is a string
        answer = response['answer']
        if isinstance(answer, list):
            answer = ' '.join(answer)

        chatbot.append(
             (message, answer))
        time.sleep(2)
        retrieved_content = vectordb.similarity_search(message, k=APPCFG.k)
        # print(retrieved_content)
        clean_reference_str = clean_references1(retrieved_content)
        
        # retrieved_content = ChatBot.clean_references(docs)
        return "", chatbot, clean_reference_str

    @staticmethod
    def clean_references(documents: list) -> str:
        """
        Clean and format references from retrieved documents.

        Parameters:
            documents (List): List of retrieved documents.

        Returns:
            str: A string containing cleaned and formatted references.
        """
        server_url = "http://localhost:8000"
        documents = [str(x)+"\n\n" for x in documents]
        markdown_documents = ""
        counter = 1
        for doc in documents:
            # Extract content and metadata
            content, metadata = re.match(
                r"page_content=(.*?)( metadata=\{.*\})", doc).groups()
            metadata = metadata.split('=', 1)[1]
            metadata_dict = ast.literal_eval(metadata)

            # Decode newlines and other escape sequences
            content = bytes(content, "utf-8").decode("unicode_escape")

            # Replace escaped newlines with actual newlines
            content = re.sub(r'\\n', '\n', content)
            # Remove special tokens
            content = re.sub(r'\s*<EOS>\s*<pad>\s*', ' ', content)
            # Remove any remaining multiple spaces
            content = re.sub(r'\s+', ' ', content).strip()

            # Decode HTML entities
            content = html.unescape(content)

            # Replace incorrect unicode characters with correct ones
            content = content.encode('latin1').decode('utf-8', 'ignore')

            # Remove or replace special characters and mathematical symbols
            # This step may need to be customized based on the specific symbols in your documents
            content = re.sub(r'â', '-', content)
            content = re.sub(r'â', '∈', content)
            content = re.sub(r'Ã', '×', content)
            content = re.sub(r'ï¬', 'fi', content)
            content = re.sub(r'â', '∈', content)
            content = re.sub(r'Â·', '·', content)
            content = re.sub(r'ï¬', 'fl', content)

            pdf_url = f"{server_url}/{os.path.basename(metadata_dict['source'])}"

            # Append cleaned content to the markdown string with two newlines between documents
            markdown_documents += f"# Retrieved content {counter}:\n" + content + "\n\n" + \
                f"Source: {os.path.basename(metadata_dict['source'])}" + " | " +\
                f"Page number: {str(metadata_dict['page'])}" + " | " +\
                f"[View PDF]({pdf_url})" "\n\n"
            counter += 1

        return markdown_documents

# response = ChatBot.respond([],'What is node js',"Upload doc: Process for RAG",0.0)