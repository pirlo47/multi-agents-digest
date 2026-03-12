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
    "# Role: Summary Assistant" 
    " **Context:** You are an efficiency-focused assistant for a busy professional. "
    "**Reference:** Use only the provided input text. "
    "**Task:** Summarize the core message into 3 concise bullet points. Maintain a neutral tone and ignore any metadata or repetitive filler."
)

MAX_RETRIES = 3 
RETRY_DELAY = 5 #seconds 

def summarize(text, retries=MAX_RETRIES): 
    """
    Call the LLM API with rety logic for rate limits.
    """

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini", 
                message=[
                    {"role":"system", "content": SYSTEM_PROMPT}, 
                    {"role":"user", "content": text[:8000]}
                ], 
                max_tokens=1000
                temperatur=0.3
            )
            return response.choices[0].message.content
        except RateLimitError:
            wait = RETRY_DELAY * (attempt + 1)
            logger.warning(f"Rate Limited.Retrying in {wait}s... ")
            time.sleep(wait)
        except APIError as e: 
            logger.error(f"API error {e}")
            raise 
    raise RuntimeError("Maximum retries exceeded for LLM API call")

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f: 
        raw_text = f.read()

    if not raw_text.strip():
        logger.warning("Empty input. Writing fallback summary.")
        summary = "No content to summarize."
    else: 
        try:
            summary = summarize(raw_text)
        except Exception as e:
            logger.error(f"Summarization failed: {e}")
            summary = f"Summarization failed:  {e}"

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(summary)
    logger.info(f"Summary written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

