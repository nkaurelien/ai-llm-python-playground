import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores import FAISS

from langchain_community import embeddings

from langchain_community.llms import Ollama

from langchain_core.runnables import RunnablePassthrough

from langchain_core.output_parsers import StrOutputParser

from langchain_core.prompts import ChatPromptTemplate

from langchain.text_splitter import CharacterTextSplitter 


    # URL processing
def process_input(urls: str, question):
    model_local = Ollama(model="mistral")
    
    # Convert string of URLs to list
    urls_list = [url.strip() for url in urls.split("\n") if url != '']
    # print(urls_list)
    # exit(0)
    docs = [WebBaseLoader(url).load() for url in urls_list]
    docs_list = [item for sublist in docs for item in sublist]
    
    
    #split the text into chunks
    
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=7500, chunk_overlap=100)
    doc_splits = text_splitter.split_documents(docs_list)
    
    #convert text chunks into embeddings and store in vector database

    # vectorstore = Chroma.from_documents(
    #     documents=doc_splits,
    #     collection_name="rag-chroma",
    #     embedding=embeddings.OllamaEmbeddings(model='nomic-embed-text'),
    # )

    #convert text chunks into embeddings and store in vector database

    vectorstore = FAISS.from_documents(
        documents=doc_splits,
        collection_name="rag-chroma",
        embedding=embeddings.OllamaEmbeddings(model='nomic-embed-text'),
    )

    print(vectorstore.index.ntotal)
    exit(0)
    retriever = vectorstore.as_retriever()
    
    #perform the RAG 
    
    after_rag_template = """Answer in french, the question based only on the following context:
    {context}
    Question: {question}
    """
    after_rag_prompt = ChatPromptTemplate.from_template(after_rag_template)
    after_rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | after_rag_prompt
        | model_local
        | StrOutputParser()
    )
    return after_rag_chain.invoke(question) 

st.title("Document Query with Ollama")
st.write("Enter URLs (one per line) and a question to query the documents.")

# Input fields
ccn_urls="""https://www.smartdatapay.com/public/conventions/md/KALICONT000005635085.md
"""
urls = st.text_area("Enter URLs separated by new lines", height=150, value=ccn_urls)
question = st.text_input("Question", value="Quel est le texte de base de la convention collective de boulanger?")

# Button to process input
if st.button('Query Documents'):
    with st.spinner('Processing...'):
        answer = process_input(urls, question)
        st.text_area("Answer", value=answer, height=300, disabled=True) 