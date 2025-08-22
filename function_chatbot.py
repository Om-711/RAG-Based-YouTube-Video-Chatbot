from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
# from langchain.chains import RunnableWithHistory
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory



def url_2_id(url):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    # normal YouTube link with ?v=
    if "v" in query:
        return query["v"][0]

    # shortened youtu.be link
    if "youtu.be" in parsed.netloc:
        return parsed.path.lstrip("/")

    # embed format
    if "embed" in parsed.path:
        return parsed.path.split("/")[-1]

    # shorts format
    if "shorts" in parsed.path:
        return parsed.path.split("/")[-1]

    raise ValueError(f"Invalid YouTube URL (no video id found): {url}")


def indexing(video_id):
    """
    It will take the caption from the youtube video for the content
    """
    ytt_api = YouTubeTranscriptApi()
    transcipt = ytt_api.fetch(video_id, languages=['en', 'hi'])

    texts = [snippet.text for snippet in transcipt]
    t = " ".join(texts)

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.create_documents([t])
    chunks = chunks[:2000]

    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vector_store = FAISS.from_documents(chunks, embeddings)

    return vector_store

def format_docs(retriever_docs):
    context = "".join(doc.page_content for doc in retriever_docs)
    return context


def retriever_chain(vector_store, question):

    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.5)
    
    prompt = PromptTemplate(
        template="""
    You are a helpful assistant.
    Answer all questions using only the context. If the context is insufficient, just say you don't know.
    Give all answer in English even if the video caption is in the hindi or any other langugae.

    {chat_history}

    Context:
    {context}

    QUESTION: {question}
    """,
        input_variables=["context", "question", "chat_history"]  
    )


    docs = vector_store.similarity_search(question, k=2)

    context = format_docs(docs)
        
    memory = ConversationBufferMemory(memory_key="chat_history", input_key="question")

    chain = LLMChain(llm=llm, prompt=prompt, memory=memory)

    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        memory=memory
    )

    response = chain.invoke({'context' : context, 'question' : question})

    return response


# def retriever_chain(vector_store, question):
#     retriever = vector_store.as_retriever(search_type = "similarity", search_kwargs={"k" : 2})
    
#     llm = ChatGoogleGenerativeAI(
#         model="gemini-2.5-flash",
#         temperature=0.5)
    
#     prompt = PromptTemplate(
#         template=""" 
#         You are a helpful assistant .
#         Answer all the question from the context only, if the context is insufficient just say you don't know.

#         {context}
#         QUESTION : {question}
#         """,
#         input_variables=['context', 'question']   
#     )

#     parallel_chain = RunnableParallel({
#         'context': retriever | RunnableLambda(format_docs),
#         'question' : RunnablePassthrough()
#     })

#     parser = StrOutputParser()

#     main_chain = parallel_chain | prompt | llm | parser

#     response = main_chain.invoke(question)

#     return response

