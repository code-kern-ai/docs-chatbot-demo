import gradio as gr
import requests


def get_answer(input_text):
    print(input_text)
    response = requests.get(
        "http://localhost:8000/get_answer", params={"question": input_text}
    )
    print(response)
    return response.json()["result"]


iface = gr.Interface(
    fn=get_answer,
    inputs=gr.inputs.Textbox(label="Input Text"),
    outputs=gr.outputs.Textbox(label="Answer"),
)

if __name__ == "__main__":
    iface.launch()
