# Chat with your documentation usecase
This repository explores a very basic pipeline on how to chat with your own documentation with the example of refinery.

## Setup
The example of refinery is already set up, but let me briefly explain the steps for other projects that follow this apporach.

### Data and application
1. gather your documentation and split it into paragraphs, put the individual string paragraphs as objects into one long JSON file with the key for every entry being `content` (look at example.json)
2. create a new project in refinery, upload that JSON file
3. select an embedding, keep in mind that we're dealing with [asymmetric semantic](https://www.sbert.net/examples/applications/semantic-search/README.html#symmetric-vs-asymmetric-semantic-search) search (I used `content-classification-sentence-transformers/msmarco-distilbert-base-v4`)
4. create a new read/write access token in the admin area in refinery, save that as an environment variable called `CHATBOT_GATES`
5. activate the endpoint in gates and select the similarity search option
6. lastly, change the `KERN_PROJECT_ID` in `server.py` to your Kern project ID

### OpenAI keys
1. save your organization-ID under the environment variable `OPENAI_ORG_ID`
2. save your OpenAI API key under the environment variable `OPENAI_API_KEY`

### Python environment
1. create new environment (e.g. `conda create --name docs_chatbot python=3.10`)
2. activate it (e.g. `conda activate docs_chatbot`)
3. install dependencies `pip install -r requirements.txt`

### Restart
Depending on your system, the new environment variables are not immediately available. You could use a jupyer notebook to test if the variables are set. If not, for me a restart of my system helped (win11).

## Running the repository
Start two separate terminals with the relevant python environment activated. Type `uvicorn server:app` into the first one and `python demo.py` into the second (in that order). You should now have access to the gradio demo at `http://127.0.0.1:7860/` or under whatever route your terminal tells you. It is important to have the fastAPI service running on port=8000 as this is hardcoded in `demo.py`.