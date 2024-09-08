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
from constants.constants import CODE_FILE_EXTENSIONS, PACKAGE_FILES, GITHUB_README_PATTERN, TOP_X_FILES, TOP_Y_FILES
from datetime import datetime, timezone
from utils import helpers


class Analyzer:

    '''
    This class is responsible for analyzing the code files in a repository.
    '''

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.g = Github(os.getenv("GH_API_PAT"))

    '''
    @input: username, repository_name
    @output: 
        files: List[File] 
        readme_file: File
        package_files: List[File]
        repo_url: str
    '''

    def get_repo_files(self, username, repository_name):
        self.logger.info(
            f"[Analyzer: get_repo_files] Getting repository files for {username}/{repository_name}")
        repo = self.g.get_repo(f"{username}/{repository_name}")
        contents = repo.get_contents("")
        files = []
        readme_file = None
        package_files = []
        # Get the url
        repo_url = repo.html_url
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

        return files, readme_file, package_files, repo_url

    '''
    Get the USER commits in this repository
    @input: username, repository_name
    @output: str_user_commits: str String of commit messages and dates but only 10 dates evenly spaced out over the commit history.
    '''

    def get_repo_commits(self, username, repository_name):
        self.logger.info(
            f"Getting repository commits for {username}/{repository_name}")
        repo = self.g.get_repo(f"{username}/{repository_name}")
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
        # How many commits were made by the user
        num_user_commits = len(user_commits)
        # How many commits were made in total
        num_total_commits = len(list(commits))
        # What percentage of the commits were made by the user
        percentage_user_commits = num_user_commits / num_total_commits * 100
        # Round to 2 decimal places
        self.logger.info(
            f"Percentage of commits made by user: {round(percentage_user_commits, 2)}%")

        self.logger.debug(f"User commits: {user_commits}")
        # return a string of the commit messages and the dates but only 10 dates evenly spaced
        # out over the commit history
        str_user_commits = ""
        for i, commit in enumerate(user_commits):
            str_user_commits += f"{commit['message']} ({commit['date']})\n"

        return str_user_commits

    '''
    Helper method to extract JSON from text sent back from the AI model. 
    @input: text: str
    @output: data: List[Dict]
    '''

    def extract_json_list_from_text(self, text):
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

    import json

    def extract_json_from_text(self, text):
        # Regular expression to find the JSON object within the text
        json_pattern = re.compile(r'\{.*\}', re.DOTALL)

        # Find the JSON part in the text
        match = json_pattern.search(text)

        if match:
            json_str = match.group()
            try:
                # Parse the JSON string into a Python dictionary
                data = json.loads(json_str)
                return data
            except json.JSONDecodeError as e:
                self.logger.warn(f"Failed to decode JSON: {e}")
                self.logger.warn(f"JSON string: {json_str}")
                return None
        else:
            self.logger.warn(f"No JSON object found in the text. {text}")
            return None

    '''
    meant to be called after POST api call to start the AI workflow
    Starts the AI workflow for the repository analysis.
    Publishes the results to the database.

    @input: username, repository_name
    @output: Analysis Results
    '''

    def start_repo_ai_workflow(self, username, repository_name):
        rtn_title = repository_name
        rtn_user = username
        rtn_summary = None
        rtn_repo_url = None
        rtn_problem_statement = None
        rtn_recency_description = None
        # rtn_demo_description = None # TODO: implement this
        rtn_technologies_description = None
        rtn_techniques_description = None
        rtn_critics_description = None

        files, readme_file, package_files, repo_url = self.get_repo_files(
            username, repository_name)
        rtn_repo_url = repo_url
        package_file = package_files[0] if len(package_files) > 0 else None
        # condense the package file to only a list of dependency names and versions
        package_file_content = ""
        if package_file is not None:
            package_file_content = package_file.decoded_content
        self.logger.info(f"Package file content: {package_file_content}")

        readme_file_content = ""
        try:
            readme_file_content = readme_file.decoded_content
        except:
            self.logger.warn("No README file found.")
            pass

        file_paths = [file.path for file in files]
        self.logger.info(f"All file paths: {file_paths}")

        user_commits = self.get_repo_commits(username, repository_name)

        # ANALYZE RECENCY
        gemini_flash_model = genai.GenerativeModel(
            model_name="gemini-1.5-flash")
        message = (
            f"You are a software developer analyzing and summarizing the commit history of a github project. Write a description of the project history including seemingly important features implemented. Also include when the project started and when the last commit was made. Return the answer in a JSON object: {{\"recency_description\": str}} commit history: {user_commits}"
        )
        self.logger.info(f"Invoking GenAi message: {message}")
        res = gemini_flash_model.generate_content(message)
        recency_description = res.text
        self.logger.info(f"Recency description: {recency_description}")
        # extract the JSON object from the text
        extracted_json_objects = self.extract_json_from_text(
            recency_description)
        self.logger.info(
            f"Extracted JSON object from recency description: {extracted_json_objects}")
        rtn_recency_description = extracted_json_objects["recency_description"]

        # CONDENSE DEPENDENCIES
        if package_file is None:
            self.logger.error(
                "No package file found for this repository. Not enough information to proceed.")
            raise Exception(
                "No package file found for this repository. Not enough information to proceed.")

        gemini_flash_model = genai.GenerativeModel(
            model_name="gemini-1.5-flash")
        message = (
            f"You are a software dev. Condense the following package file only a list of dependency names and versions in a list that's follows the format: package_1,version;\npackage_2,version;\n ... {package_file_content}"
        )
        self.logger.info(f"Invoking GenAi message: {message}")
        res = gemini_flash_model.generate_content(message)

        condensed_package_file_str = res.text
        self.logger.info(
            f"Condensed package file: {condensed_package_file_str}")

        # GET TECHNOLOGIES DESCRIPTION
        chat = gemini_flash_model.start_chat()
        message = (
            f"You are a software dev describing a code repository to your tech lead. Look at the list of packages dependencies and versions as well as the readme file. Write a summary describing the technologies used in the project including the coding languages, frameworks, important libraries, and any cloud based services used in this project. Return the answer as a JSON Object like {{\"technologies_description\": str}} package list: {condensed_package_file_str} readme file: {readme_file_content}")
        self.logger.info(f"Invoking GenAi chat(1) message: {message}....")
        res = chat.send_message(message)
        technologies_description = res.text
        self.logger.info(
            f"technologies_description: {technologies_description}")
        # extract the JSON object from the text
        extracted_json_objects = self.extract_json_from_text(
            technologies_description)
        self.logger.info(
            f"Extracted JSON object from technologies description: {extracted_json_objects}")
        rtn_technologies_description = extracted_json_objects["technologies_description"]

        # GET PROJECT SUMMARY AND PROBLEM STATEMENT
        message = (
            f"Look at the readme file, commit history, and pr history for this repository. Describe who this project is for and what it solves including what industry it is in. Also summarize what this project does including some of the key technology and software engineering techniques used in the project. Return in a JSON object: {{\"problem_statement\": str, \"technologies_description\": str, \"techniques_description\"}} readme file: {readme_file_content} commit history: {user_commits}"
        )
        self.logger.info(f"Invoking GenAi chat(1) message: {message}....")
        response = chat.send_message(message)
        summary_problem_statement = response.text
        self.logger.info(
            f"summary_problem_statement: {summary_problem_statement}")
        # extract the JSON object from the text
        extracted_json_objects = self.extract_json_from_text(
            summary_problem_statement)
        self.logger.info(
            f"Extracted JSON object from summary and problem statement: {extracted_json_objects}")
        rtn_problem_statement = extracted_json_objects["problem_statement"]
        tmp_technologies_description = extracted_json_objects["technologies_description"]
        rtn_techniques_description = extracted_json_objects["techniques_description"]
        self.logger.warn(
            f"COMPARE THESE TWO: first commit history technologies_description: {rtn_technologies_description} \n\n\nsecond commit history technologies_description: {tmp_technologies_description}")

        # GET THE TOP Y FILES TO LOOK AT
        message = f"Now that you have a good understanding of the project, here is the file structure of the project. Identify the most important files in the project a developer would need to look at to have a better understaning of how the project works. List the top 5 files and a confidence score (0-100) for each file that you think are the most important modules in the code base. Return the list of files and confidence scores in a JSON object: [{{\"file_path\": str, \"confidence_score\": str}}]. Here are the files: {file_paths}. Don't return anything else."
        print(f"Invoking GenAi chat(1) message: {message}....")
        response = chat.send_message(
            message
        )
        important_files = response.text
        self.logger.info(f"Important files list: {important_files}")

        extracted_json_objects = self.extract_json_list_from_text(
            important_files)
        self.logger.info(
            f"Extracted JSON objects from important files: {extracted_json_objects}")

        # GET THE TOP X FILES TO LOAD INTO THE AI MODEL TO ANALYZE (good practices & improvements)
        top_x_files = extracted_json_objects
        self.logger.info(f"Top X files: {top_x_files}")

        important_files_content = []
        added_files = 0
        for file in top_x_files:
            # Look up file path in files and get the decoded_content for that file
            if added_files >= TOP_X_FILES:
                break

            file_path = file["file_path"]

            # Find the file in the files list
            file_obj = next(
                (f for f in files if f.path == file_path), None)

            if file_obj is None:
                self.logger.warn(f"File not found: {file_path}")
                continue
            else:
                self.logger.info(f"Found file: {file_path}")

            # DECODE FILE CONTENT.
            file_content = helpers.extract_file_content(file_obj)
            if file_content is None:
                self.logger.warn(f"File content not found: {file_path}")
                # Skip this file
                continue

            important_files_content.append(
                {"file_path": file_path, "content": file_content})
            added_files += 1

        message = (
            f"Here is a summary of the project for context. Now look at these three important files and describe how you would re-write them to make them more efficient. Make sure to highlight where the good coding practices as well as criticize anti-patterns or bad coding practices found in these modules. List the points you would change and why you woulld change it. Return the analysis in a JSON OBJECT: [{{\"file_path\": str, \"analysis\": str}}]. Only give me the JSON object. Don't return suggested code. Only analyse the files if the file content is present. Here are the files: {important_files_content}"
        )
        self.logger.info(f"Invoking GenAi chat(1) message: {message}....")
        response = chat.send_message(message)
        analysis = response.text
        self.logger.info(f"Analysis code files: {analysis}")

        # USE ANALYSIS TO GET CRITICS AND ADD TO OTHER JSON OBJECTS
        message = (
            f"Look at the analysis of the important files. Write a summary of the critics and suggestions made in the analysis. Return the summary in a JSON object: {{\"critics_description\": \"description\"}}. Here is the analysis: {analysis}"
        )
        self.logger.info(f"Invoking GenAi chat(1) message: {message}")
        response = chat.send_message(message)
        critics_description = response.text
        self.logger.info(f"Critics description: {critics_description}")
        # extract the JSON object from the text
        extracted_json_objects = self.extract_json_from_text(
            critics_description)
        self.logger.info(
            f"Extracted JSON object from critics description: {extracted_json_objects}")
        rtn_critics_description = extracted_json_objects["critics_description"]

        # DOUBLE CHECK MOST UP TO DATE DESCRIPTIONS
        message = (
            f"Look the total analysis of this repository. Update the summary, problem statement, and techniques description. Return the updated JSON object: {{\"summary\": str, \"problem_statement\": str, \"techniques_description\": str}} analysis: {analysis}, techniques_description: {rtn_techniques_description}, summary: {rtn_summary}, problem_statement: {rtn_problem_statement}, another techniques_description: {tmp_technologies_description}"
        )
        self.logger.info(f"Invoking GenAi chat(1) message: {message}")
        response = chat.send_message(message)
        updated_descriptions = response.text
        self.logger.info(f"Updated descriptions: {updated_descriptions}")
        # extract the JSON object from the text
        extracted_json_objects = self.extract_json_from_text(
            updated_descriptions)
        self.logger.info(
            f"Extracted JSON object from updated descriptions: {extracted_json_objects}")
        rtn_summary = extracted_json_objects["summary"]
        rtn_problem_statement = extracted_json_objects["problem_statement"]
        rtn_techniques_description = extracted_json_objects["techniques_description"]

        # Time at UTC timezone
        timestamp_with_tz = datetime.now(
            timezone.utc).strftime('%Y-%m-%d %H:%M:%S%z')
        return {
            "recency_description": rtn_recency_description,
            "technologies_description": rtn_technologies_description,
            "summary": rtn_summary,
            "problem_statement": rtn_problem_statement,
            "critics_description": rtn_critics_description,
            "techniques_description": rtn_techniques_description,
            "repo_url": rtn_repo_url,
            "user": rtn_user,
            "title": rtn_title,
            "repo_url": rtn_repo_url,
            "created_at": timestamp_with_tz,
            "demo_description": "",
        }
