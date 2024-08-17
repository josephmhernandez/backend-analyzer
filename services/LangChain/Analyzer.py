import re
import json
import google.generativeai as genai
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import SystemMessage, HumanMessage
import logging
from langchain_google_vertexai import ChatVertexAI
import sys
import time
import os
from github import Github
from langchain_openai import ChatOpenAI
from constants import CODE_FILE_EXTENSIONS, PACKAGE_FILES
# from constants.constants import GH_API_PAT

# llm = ChatOpenAI()
# j = llm.invoke("Hello, world!")
# print(j)


# GitHub repo URL

# Get the file structure

# Get all the files in the repo
# Filter out non-programming files

# Get commit history of the repo: commit message, author, date


# LLM condense packages file into a single file

g = Github(os.getenv("GH_API_PAT"))

README_PATTERN = "/^readme\.(?:markdown|mdown|mkdn|md|textile|rdoc|org|creole|mediawiki|wiki|rst|asciidoc|adoc|asc|pod|txt)/i"


def get_repo_files(username, repositoryName):
    repo = g.get_repo(f"{username}/{repositoryName}")
    contents = repo.get_contents("")
    print(contents)
    files = []
    readme_file = None
    package_files = []
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            # IF file path matches regex README_PATTERN
            if file_content.name.lower().startswith("readme"):
                if readme_file is None:
                    print(
                        f"HOLD UP Found README file: {file_content.name} & {readme_file}")
                readme_file = file_content

            # Filter out non-programming files
            if file_content.name.endswith(tuple(CODE_FILE_EXTENSIONS)):
                files.append(file_content)
            else:
                # print(f"Skipping {file_content.name}")
                pass

            # Filter out package files
            if file_content.name in PACKAGE_FILES:
                package_files.append(file_content)

    return files, readme_file, package_files


def get_repo_commits(username, repositoryName):
    repo = g.get_repo(f"{username}/{repositoryName}")
    commits = repo.get_commits()

    # return the commit names and the dates. Get the percentage of commits in that were
    #  performed by the user. Get the names of the commits that were performed by the user.
    # Get the dates of the commits that were performed by the user. Get the commit messages
    # for commit in commits:
    #     print(commit.commit.message)
    #     print(commit.commit.author.date)
    user_commits = []
    for commit in commits:
        # print(commit.author)
        # only get commits by the user
        try:
            if commit.author.login == username:
                # append commit message and date
                # convert date to string with "YYYY-MM-DD" format
                date_str = commit.commit.author.date.strftime("%Y-%m-%d")
                user_commits.append(
                    {"message": commit.commit.message, "date": date_str})

        except:
            pass
    # reverse the list
    user_commits.reverse()

    # return a string of the commit messages and the dates but only 10 dates evenly spaced
    # out over the commit history
    str_user_commits = ""
    for i, commit in enumerate(user_commits):
        if i % 10 == 0:
            str_user_commits += f"{commit['message']} ({commit['date']})\n"
        else:
            str_user_commits += f"{commit['message']}\n"

    return str_user_commits


# Actual work....
# Start a timer
start_time = time.time()
files, readme_file, package_files = get_repo_files(
    "josephmhernandez", "lyfe-captures")

package_file = package_files[0] if len(package_files) > 0 else None
# condense the package file to only a list of dependency names and versions
package_file_content = package_file.decoded_content
print(package_file_content)
readme_file_content = readme_file.decoded_content

file_paths = [file.path for file in files]

print('file_paths:', file_paths)
# print('readme_file:', readme_file)
# print('package_files:', package_files)


user_commits = get_repo_commits("josephmhernandez", "lyfe-captures")


# End the timer
end_time = time.time()
print(f"Time taken: {end_time - start_time} seconds")

# Do the llm work here.

doing_llm = True
# logger = logging.getLogger(__name__)
if not doing_llm:
    sys.exit()

# Starting the LLM work
start_time = time.time()

print("Starting LLM work...")

# Set up the env

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# CONDENSE DEPENDENCIES
gemini_flash_model = genai.GenerativeModel(
    model_name="gemini-1.5-flash")
print("Gemini Flash model loaded")
message = (
    f"You are a software dev. Condense the following package file only a list of dependency names and versions in a list that's follows the format: package_1,version;\npackage_2,version;\n ... {package_file_content}"
)

# llm = ChatVertexAI(model="gemini-1.5-flash")


print(f"Invoking message: {message}....")
res = gemini_flash_model.generate_content(message)
print(f"Response from Condensing_Package_File: {res}")
lap_time = time.time()
print(f"Package condensing : {lap_time - start_time} seconds")

# parse the response
condensed_package_file_str = res.text
# parser = StrOutputParser()
# condensed_package_file_str = parser.invoke(res)
print(f"Condensed package file: {condensed_package_file_str}")

# GET TECHNOLOGIES DESCRIPTION
chat = gemini_flash_model.start_chat()
message = (
    f"You are a software dev describing a code repository to your tech lead. Look at the list of packages dependencies and versions as well as the readme file. Write a summary describing the technologies used in the project including the coding languages, frameworks, important libraries, and any cloud based services used in this project. package list: {condensed_package_file_str} readme file: {readme_file_content}")
# res = gemini_flash_model.generate_content(message)
print(f"Invoking message: {message}....")
res = chat.send_message(message)
technologies_description = res.text
print('technologies_description', technologies_description)
print('full res', res)
# cache = genai.caching.CachedContent.create(
#     model="gemini-1.5-flash", system_instruction="You are a software engineer technical lead", contents=chat.history
# )
# model_with_cache = genai.GenerativeModel.from_cached_content(
#     cached_content=cache)
# chat = model_with_cache.start_chat()


message = (
    f"Look at the readme file, commit history, and pr history for this repository. Desribe who this project is for and what it solves including what industry it is in. Also summarize what this project does including some of the key technology used in the project. Return the summary and problem statement in a JSON object: {{\"problem_statement\": str, \"summary\": str}} readme file: {readme_file_content} commit history: {user_commits}"
)

response = chat.send_message(message)
summary_problem_statement = response.text
print('response', response)
print('summary_problem_statement', summary_problem_statement)
# parse the response


# GET THE TOP Y FILES TO LOOK AT
print("# GET THE TOP Y FILES TO LOOK AT")
message = f"Now that you have a good understanding of the project, here is the file structure of the project. Identify the most important files in the project a developer would need to look at to have a better understaning of how the project works. List the top 5 files and a confidence score (0-100) for each file that you think are the most important modules in the code base. Return the list of files and confidence scores in a JSON object: [{{\"file_path\": str, \"confidence_score\": str}}]. Here are the files: {file_paths}. Don't return anything else."
print(f"Invoking message: {message}....")
response = chat.send_message(
    message
)
important_files = response.text


print('response', response)
print('important_files', important_files)


def extract_json_from_text(text):
    # Regular expression to find the JSON within the text
    json_pattern = re.compile(r'\[\s*\{.*?\}\s*\]', re.DOTALL)

    # Find the JSON part in the text
    match = json_pattern.search(text)

    if match:
        json_str = match.group()
        try:
            # Parse the JSON string into a Python list
            data = json.loads(json_str)
            return data
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
            return None
    else:
        print("No JSON found in the text.")
        return None


print('importatnt file type: ', type(important_files))
extracted_json_objects = extract_json_from_text(important_files)
print('extracted_json_objects', extracted_json_objects)
# top 3 files to look at
top_x_files = extracted_json_objects[:3]
print('top_x_files', top_x_files)
# parse the response
# Get the content of the top x files

important_files_content = []

# file_paths = [file.path for file in files]
print("LOOKING AT TOP X FILES")
for file in top_x_files:
    # Look up file path in files and get the decoded_content for that file

    file_path = file["file_path"]

    # Find the file in the files list
    file_obj = next(
        (f for f in files if f.path == file_path), None)

    if file_obj is None:
        print(f"File not found: {file_path}")
        continue
    else:
        print(f"Found file: {file_path}")
    file_content = file_obj.decoded_content
    important_files_content.append(
        {"file_path": file_path, "content": file_content})


# ADD README FILE, COMMIT HISTORY, AND TECHNOLOGIES DESCRIPTION
# message = HumanMessage(
#     ""
# )

# RE-WRITE THE TOP X FILES
message = (
    f"Here is a summary of the project for context. Now look at these three important files and describe how you would re-write them to make them more efficient. Make sure to highlight where the good coding practices as well as criticize anti-patterns or bad coding practices found in these modules. List the points you would change and why you woulld change it. Return the analysis in a JSON OBJECT: [{{\"file_path\": str, \"analysis\": str}}]. Only give me the JSON object. Don't return suggested code. Only analyse the files if the file content is present. Here are the files: {important_files_content}"
)
response = chat.send_message(message)
analysis = response.text
print('response', response)
print('analysis', analysis)

# End the timer
end_time = time.time()
print(f"Time taken: {end_time - start_time} seconds")
