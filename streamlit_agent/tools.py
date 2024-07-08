import os
from datetime import datetime

from dotenv import load_dotenv
from exa_py import Exa
from langchain_core.tools import tool

load_dotenv()

exa = Exa(api_key=os.environ["EXA_API_KEY"])


@tool
def search(query: str, start_published_date: datetime, end_published_date: datetime):
    """Search for a webpage based on the query."""
    start_published_date_str = start_published_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    end_published_date_str = end_published_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return exa.search(f"{query}",
                      use_autoprompt=True,
                      num_results=10,
                      include_domains=["mooool.com", "gooood.cn",
                                       "baike.baidu.com",
                                       "mooool.com", "archiposition.com",
                                       "archdaily.cn", "arch-exist.com",
                                       "tlaidesign.com", "hhlloo.com"],
                      type="neural",
                      start_published_date=start_published_date_str,
                      end_published_date=end_published_date_str,
                      )


@tool
def find_similar(url: str):
    """Search for webpages similar to a given URL.
    The url passed in should be a URL returned from `search`.
    """
    return exa.find_similar(url,
                            num_results=5)


@tool
def get_contents(ids: list[str]):
    """Get the contents of a webpage.
    The ids passed in should be a list of ids returned from `search`.
    """
    return exa.get_contents(ids)
