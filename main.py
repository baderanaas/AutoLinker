import pandas as pd
import logging
from autoLinker import autoLinker

# Configure logging
logging.basicConfig(
    filename="auto_linker.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Load data
data = pd.read_csv("companies.csv")
data.columns = data.columns.str.strip()

if data.shape[0] == 0:
    logging.error("No data to process.")
    exit()

for index, row in data.iterrows():
    link = row["Link"]
    note = row["Note"]
    message = row["Message"]
    Done = row["Done"]
    if Done:
        logging.info(f"Skipping {link} as it's already done.")
        continue
    attempts = 0
    success = False
    while attempts < 3 and not success:
        try:
            autoLinker(link, message, note, premium=True)
            data.at[index, "Done"] = True
            data.to_csv("companies.csv", index=False)
            logging.info(f"Processed {link} successfully.")
            success = True
        except Exception as e:
            attempts += 1
            logging.error(f"Attempt {attempts} - Error processing {link}: {e}")
    if not success:
        logging.error(f"Failed to process {link} after 3 attempts.")
