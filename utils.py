import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def save_list_as_file(text_list, file_name):
    with open(f"{file_name}.txt", "w", encoding="utf-8") as file:
        for text in text_list:
            file.write(f"{text}\n")

        logger.info(f"{file_name} saved successfully.")
        
