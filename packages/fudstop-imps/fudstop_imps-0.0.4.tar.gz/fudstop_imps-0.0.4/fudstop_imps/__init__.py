from fudstop4.apis.occ.occ_sdk import occSDK
from fudstop4.apis.newyork_fed.newyork_fed_sdk import FedNewyork
from fudstop4.apis.polygonio.polygon_options import PolygonOptions
from fudstop4.apis.webull.webull_options.webull_options import WebullOptions
from fudstop4.apis.helpers import generate_webull_headers
from fudstop4._markets.list_sets.ticker_lists import most_active_tickers
from fudstop4.apis.helpers import format_large_numbers_in_dataframe2
from fudstop4.all_helpers import chunk_string
from discord_webhook import AsyncDiscordWebhook, DiscordEmbed
from fudstop4._markets.list_sets.dicts import hex_color_dict
from fudstop4.apis.ultimate.ultimate_sdk import UltimateSDK
from fudstop4.apis.webull.webull_trading import WebullTrading
from fudstop4.apis.webull.webull_markets import WebullMarkets
from fudstop4.apis.y_finance.yf_sdk import YfSDK
from fudstop4.apis.master.master_sdk import MasterSDK
from openai import OpenAI
from asyncio import Semaphore
import asyncio
import logging
from typing import Dict, List, Tuple, Union, Optional, Any, Callable, Coroutine, Generator, AsyncIterator, Awaitable, AsyncGenerator
from datetime import datetime, timedelta
from itertools import islice
from more_itertools import chunked
from pathlib import Path
import sys
import os
from dotenv import load_dotenv
load_dotenv()
import time

import pandas as pd

import aiohttp
import json
import requests
import numpy as np
import logging
from tabulate import tabulate


ULTIMATE = UltimateSDK()
MASTER = MasterSDK()
WBTRADING = WebullTrading()
WBMARKETS = WebullMarkets()
WBOPTIONS = WebullOptions()
DB = PolygonOptions()
OCC = occSDK()
FEDNY = FedNewyork()
OPENAI = OpenAI(api_key=os.environ.get('OPENAI_KEY'))
YFSDK = YfSDK()
