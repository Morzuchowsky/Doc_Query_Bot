from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


def get_valid_file_path():
    """
    Asks the user to input a file path and checks its validity.
    Repeats until a valid file path is provided or the user decides to exit.
    """
    while True:
        try:
            file_path = input(
                "Please enter the file path (ex. C:\\Adam\\Desktop\\lalka.pdf) or type 'quit' or 'wyjdz' to exit: ")

            # Check if the user wants to quit
            if file_path.lower() in ['quit', 'wyjdz']:
                print("Exiting...")
                exit()

            if os.path.exists(file_path):
                return file_path
            else:
                print("The file path does not exist. Please try again.")
        except Exception as e:
            print(f"Error: {e}. Please try again.")


def ask_questions_until_exit(question_answering_system):
    """
    Allows the user to ask questions repeatedly until they type 'quit' or 'wyjdz'.
    """
    while True:
        question = input("Please input your question (or type 'quit' or 'wyjdz' to exit): ")
        if question.lower() in ['quit', 'wyjdz']:
            break
        answer = question_answering_system.run(question)
        print(answer)


def load_documents_from_path():
    """
    Load documents using the given file path.
    """
    document_loader = PyPDFLoader(file_path=file_path)
    return document_loader.load()


def split_documents_into_chunks(documents):
    """
    Split documents into manageable chunks.
    """
    text_splitter = CharacterTextSplitter(
        chunk_size=1000, chunk_overlap=30, separator="\n"
    )
    return text_splitter.split_documents(documents=documents)


def create_and_save_vector_store(documents, embeddings):
    """
    Create a vector store from documents using the provided embeddings engine and save it locally.
    """
    vector_store = FAISS.from_documents(documents, embeddings)
    vector_store.save_local("faiss_index_react")
    return vector_store


def load_vector_store_and_setup_qa_system(embeddings):
    """
    Load the locally saved vector store and set up the QA system.
    """
    loaded_vector_store = FAISS.load_local("faiss_index_react", embeddings)
    return RetrievalQA.from_chain_type(
        llm=OpenAI(), chain_type="stuff", retriever=loaded_vector_store.as_retriever()
    )


# Main execution
file_path = get_valid_file_path()
loaded_documents = load_documents_from_path()
split_docs = split_documents_into_chunks(loaded_documents)
embeddings_engine = OpenAIEmbeddings()
create_and_save_vector_store(split_docs, embeddings_engine)
qa_system = load_vector_store_and_setup_qa_system(embeddings_engine)
ask_questions_until_exit(qa_system)
