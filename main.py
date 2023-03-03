from sentence_transformers import SentenceTransformer, util
import pinecone
import openai
import docx2txt


# Split text into smaller parts to be indexed separately
def split_text_into_chunks(plain_text, max_chars=2000):
    text_chunks = []
    current_chunk = ""
    for line in plain_text.split("\n"):
        if len(current_chunk) + len(line) + 1 <= max_chars:
            current_chunk += line + " "
        else:
            text_chunks.append(current_chunk.strip())
            current_chunk = line + " "
    if current_chunk:
        text_chunks.append(current_chunk.strip())
    return text_chunks


# Add data to Pinecone index
def addData(corpusData):
    id = index.describe_index_stats()['total_vector_count']
    for i in range(len(corpusData)):
        chunk = corpusData[i]
        chunkInfo = (str(id + i),
                     model.encode(chunk).tolist(),
                     {'context': chunk})
        index.upsert(vectors=[chunkInfo])


# Query Pinecone index and return matching contexts
def find_match(query, k):
    query_em = model.encode(query).tolist()
    result = index.query(query_em, top_k=k, includeMetadata=True)
    return [result['matches'][i]['metadata']['context'] for i in range(k)]


# Generate a prompt based on the retrieved context and query
def create_prompt(context, query):
    prompt = f"Question: {query}\nContext: {context}\nAnswer:"
    return prompt


# Use GPT-3 to generate an answer to the prompt
def generate_answer(prompt):
    # Set up OpenAI API credentials
    openai.api_key = "Insert openai API here"
    model_engine = "text-embedding-002"

    # Generate answer using OpenAI's GPT-3 API
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    answer = response.choices[0].text.strip()

    return answer


# Combine all the functions to provide a full user query experience
def user_query(query, k=5):
    # Search Pinecone index for matching contexts
    matching_contexts = find_match(query, k)

    # Generate prompts for each matching context and query
    prompts = [create_prompt(context, query) for context in matching_contexts]

    # Generate an answer to each prompt using GPT-3
    answers = [generate_answer(prompt) for prompt in prompts]

    # Return the matching contexts and their associated answers
    return dict(zip(matching_contexts, answers))


if __name__ == "__main__":
    # Load the SentenceTransformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    text = docx2txt.process('DataLaw.docx')

    # Initialize Pinecone vector database
    pinecone.init(api_key="", environment="")
    index_name = "my_index"
    index = pinecone.Index(index_name)

    text_chunks = split_text_into_chunks(text)
    addData(text_chunks)
    user_query("How can I do this?")
