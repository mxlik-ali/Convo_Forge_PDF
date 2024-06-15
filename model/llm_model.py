from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

def llm_response(vectorstores):
    # Create a conversation buffer memory
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

    # Define a custom template for the question prompt
    custom_template = """Given the following conversation and a follow-up question, rephrase the follow-up question to be a standalone question, in its original English.
                            Chat History:
                            {chat_history}
                            Follow-Up Input: {question}
                            Standalone question:"""

    # Create a PromptTemplate from the custom template
    CUSTOM_QUESTION_PROMPT = PromptTemplate.from_template(custom_template)

    # Create a ConversationalRetrievalChain from an LLM with the specified components
    conversational_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(),
        memory=memory,
        condense_question_prompt=CUSTOM_QUESTION_PROMPT
    )