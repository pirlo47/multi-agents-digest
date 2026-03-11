"""
Reads the ingested text an calls an LLM API to produce concise summary. This is the 
only agent that makes a network call. 

"""
import os 
import logging
import time 
from openai import OPENAI, RateLimitError, APIError

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger("summarizer")

INPUT_FILE = "/data/ingested.txt"
OUTPUT_FILE = "/data/summary.txt"

# reads OPENAI_API_KEY from environment 
client = OPENAI() 

SYSTEM_PROMPT = (
    "You are a helpful assitant that summarizes long text "
    "into key bullet points. Each bullet should be one" 
    "consice sentence capturing a core insight"
)

