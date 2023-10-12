from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from dotenv import load_dotenv

load_dotenv()

user_file_path = input("Please enter the file path (ex. \Adam\Desktop\lalka.pdf) : ")

loader = PyPDFLoader(file_path=user_file_path)
documents = loader.load()
text_splitter = CharacterTextSplitter(
    chunk_size=1000, chunk_overlap=30, separator="\n"
)

docs = text_splitter.split_documents(documents=documents)

embeddings = OpenAIEmbeddings()

vectorstore = FAISS.from_documents(docs, embeddings)
vectorstore.save_local("faiss_index_react")

new_vectorstore = FAISS.load_local("faiss_index_react", embeddings)
qa = RetrievalQA.from_chain_type(
    llm=OpenAI(), chain_type="stuff", retriever=new_vectorstore.as_retriever()
)
final_answer = qa.run(input("Please input Your question: "))
print(final_answer)
