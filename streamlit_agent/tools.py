import os
from datetime import datetime, timedelta
from typing import Optional

from dotenv import load_dotenv
from exa_py import Exa
from langchain_core.tools import tool

load_dotenv()

exa = Exa(api_key=os.environ["EXA_API_KEY"])


@tool
def search(query: str,
           num_results: int = 5,
           start_published_date: datetime = None,
           end_published_date: datetime = None):
    """Search for a webpage based on the query."""
    if start_published_date:
        start_published_date = start_published_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    if end_published_date:
        end_published_date = end_published_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    print(f"start_published_date, end_published_date: {start_published_date, end_published_date}")
    return exa.search(f"{query}",
                      use_autoprompt=True,
                      num_results=num_results,
                      include_domains=["mooool.com", "gooood.cn",
                                       "baike.baidu.com", "zh.wikipedia.org"
                                       "mooool.com", "archiposition.com",
                                       "archdaily.cn", "arch-exist.com",
                                       "tlaidesign.com", "hhlloo.com"],
                      type="neural",
                      start_published_date=start_published_date,
                      end_published_date=end_published_date
                      )


@tool
def find_similar(url: str, num_results: int = 5):
    """Search for webpages similar to a given URL.
    The url passed in should be a URL returned from `search`.
    """
    return exa.find_similar(url,
                            num_results=num_results)


@tool
def get_contents(ids: list[str]):
    """Get the contents of a webpage.
    The ids passed in should be a list of ids returned from `search`.
    """
    return exa.get_contents(ids)
