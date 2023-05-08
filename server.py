from fastapi import FastAPI
import os
import requests
import openai

# TODO Change this to the ID of your project
KERN_PROJECT_ID = "3f89b654-640e-4c60-87a5-0f096121df59"

OPEN_AI_KEY = os.getenv("OPENAI_API_KEY")
GATES_KEY = os.getenv("CHATBOT_GATES")
OPEN_AI_ORG_KEY = os.getenv("OPENAI_ORG_ID")

openai.organization = OPEN_AI_ORG_KEY
openai.api_key = OPEN_AI_KEY

app = FastAPI()


def get_similar_records(question: str):
    """
    helper function to call gates for similarity search
    """

    url = f"https://app.kern.ai/commercial/v1/predict/project/{KERN_PROJECT_ID}"

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"{KERN_PROJECT_ID} {GATES_KEY}",
    }

    example_data = {"running_id": 0, "content": question}

    response = requests.post(url, headers=headers, json=example_data)

    similar_records_dict = response.json()["similarRecords"]
    embedd1_similar_records = similar_records_dict[list(similar_records_dict.keys())[0]]

    return [x["content"] for x in embedd1_similar_records]


@app.get("/get_answer")
async def get_answer(question: str):
    context = get_similar_records(question)
    print(context)
    if len(context) > 0:
        my_context = "\n".join(context)
        openai_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that was trained to extract information from relevant passages in a documentation of a product called 'refinery' that was made by the company 'Kern AI'. Every request will contain a question and some context. Please answer according to the given context and if you are not fully sure, please disclose that the requested information is not in the context that you were given.",
                },
                {
                    "role": "user",
                    "content": f"question: what is a labeling task?\n\ncontext:{my_context}",
                },
            ],
        )
        answer = openai_response["choices"][0]["message"]["content"]
        return {"result": answer}
    else:
        return {
            "result": "We could not find any passages matching your question. Please reformulate the question, be as precise as you can, and try again."
        }
