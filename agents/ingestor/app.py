"""
The entry point of the pipeline. 
Its job is to read all the textfiles from the input folder and 
combine them into a single file that Summarize agent can process 
JUST READING AND WRITING!!!

"""

import os 
import logging

#Setup structured logging 
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger("ingestor")

INPUT_DIR = "data/input"
OUTPUT_FILE = "data/ingested.txt"

def ingest():

    content = ""
    files_processed = 0

    for filename in sorted(os.listdir(INPUT_DIR)):
        filepath = os.path.join(INPUT_DIR, filename)
        if os.path.filename is filepath:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content += f"---- {filename} ----"
                    content += f.read()
                    content += "\n"
                    files_processed += 1 
            except Exception as e:
                logger.error(f"Failed to open {filename} : {e}")

    if files_processed == 0:
        logging.warning(f"No input files in found in {INPUT_DIR}")
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write(content)
    logging.info(f"Ingested {files_processed} files -> {OUTPUT_FILE}")

if __name__ == "__main__":
    ingest()
