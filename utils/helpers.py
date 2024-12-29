
import json
import logging
import uuid


def extract_file_content(file):
    logging.info(f"Extracting content from file: {file}")
    logging.info(f"File type: {type(file)}")

    isError: bool = False
    file_content = None

    try:
        file_content = file.decoded_content
    except Exception as e:
        pass

    if file_content != None:
        return file_content

    try:
        file_content = file.content
    except Exception as e:
        pass
    if file_content != None:
        return file_content

    try:
        # Download the file content
        file_path = file.download_url
        logging.info(f"Trying to download file contents: {file_path}")
        # Download the file content
        with open(file_path, "r") as f:
            file_content = f.read()

    except Exception as e:
        logging.error(f"Error extracting content from file: {file}")
        logging.error(f"Error trying to download file: {e}")

    return file_content


'''
Before we input to the database, we need to format the content returned from our ai model.
input: content: str
output: str
'''


def format_analysis_content(content: str) -> str:
    logging.info(f"Formatting analysis content")
    # Find "* **" and replace with "\n* **" to create a new line
    content = content.replace("* **", "\n* **")

    return content
