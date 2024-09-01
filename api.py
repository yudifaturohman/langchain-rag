from flask import Flask, request, jsonify
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from get_embedding_function import get_embedding_function
import os

app = Flask(__name__)

CHROMA_PATH = "chroma"
os.environ["GROQ_API_KEY"] = "gsk_pasteyourapikey"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

def query_rag(query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    model = ChatGroq(model='mixtral-8x7b-32768')
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = {
        "response": response_text,
        "sources": sources
    }
    return formatted_response

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    query_text = data.get("query_text", "")

    if not query_text:
        return jsonify({"error": "query_text is required"}), 400

    result = query_rag(query_text)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
