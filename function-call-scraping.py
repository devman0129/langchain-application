from langchain.document_loaders import AsyncChromiumLoader
from langchain.document_transformers import BeautifulSoupTransformer
from langchain.chains import create_extraction_chain

import os
os.environ["OPENAI_API_KEY"] = "<OpenAI API Key>"

import pprint
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

schema = {
    "properties": {
        "content_of_webpage": {"type": "string"},
        "url_of_image": {"type": "string"},
        "title_of_article": {"type": "string"},
    },
    "required": ["content_of_webpage", "url_of_image", "title_of_article"],
}

def extract(content: str, schema: dict):
    return create_extraction_chain(schema=schema, llm=llm).run(content)

def scrape_with_playwright(urls, schema):
    loader = AsyncChromiumLoader(urls)
    docs = loader.load()
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(
        docs, unwanted_tags=["script", "style"]
    )
    print("Extracting content with LLM")

    # Grab the first 1000 tokens of the site
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000, chunk_overlap=0
    )
    splits = splitter.split_documents(docs_transformed)

    # Process the first split
    for split in splits:
        print(split.page_content)
        print("------------------------------------------------------------------------------------")
        extracted_content = extract(schema=schema, content=split.page_content)
        pprint.pprint(extracted_content)


urls = ["https://eightify.app/summary/climate-change/step-by-step-walkthrough-multi-agent-autogen-group-chat-implementations"]
extracted_content = scrape_with_playwright(urls, schema=schema)





