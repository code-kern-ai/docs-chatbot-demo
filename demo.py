import gradio as gr
import requests


def get_answer(input_question):
    response = requests.get(
        "http://localhost:8000/get_answer", params={"question": input_question}
    )
    print(response)
    return response.json()["result"]


iface = gr.Interface(
    fn=get_answer,
    inputs=["text"],
    outputs=["markdown"],
    title="Documentation Q&A",
    description = "Ask a question about refinery and the combined power of embeddings, GPT, and a well-written documentation will provide you with an answer.",
    allow_flagging="never"
)

if __name__ == "__main__":
    iface.launch(favicon_path="refinery-favicon.ico")
