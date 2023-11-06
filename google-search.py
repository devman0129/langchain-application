import os

os.environ["GOOGLE_CSE_ID"] = "<Google CSE Id>" # https://programmablesearchengine.google.com/controlpanel/create
os.environ["GOOGLE_API_KEY"] = "<Google API Key>" # https://console.cloud.google.com/apis/credentials

from langchain.tools import Tool
from langchain.utilities import GoogleSearchAPIWrapper

search = GoogleSearchAPIWrapper()

def top5_results(query):
    return search.results(query, 5)


tool = Tool(
    name="Google Search Snippets",
    description="Search Google for recent results.",
    func=top5_results,
)

result = tool.run("What is react?")

print(result)