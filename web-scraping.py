from langchain.document_loaders import AsyncChromiumLoader
from langchain.document_transformers import BeautifulSoupTransformer

loader = AsyncChromiumLoader(["https://joshuahodgeswriting.wordpress.com/2020/10/05/shark-a-short-creative-writing-piece/"])
html = loader.load()

bs_transformer = BeautifulSoupTransformer()
docs_transformed = bs_transformer.transform_documents(html, unwanted_tags=["script", "style"])

print(docs_transformed[0].page_content)

