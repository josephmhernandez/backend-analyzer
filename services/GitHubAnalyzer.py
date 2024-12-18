# import logging
# import httpx
# from clients.github_client import GitHubClient
# from constants.constants import GITHUB_API_URL
# from models.github_repository_request import GithubRepositoryRequest

# from constants.constants import ENV_TAVILY_API_KEY, ENV_OPENAI_API_KEY
# # from services.TavilyService import TavilyService
# import openai
# import os
# from openai import AsyncOpenAI
# import json


# class GitHubAnalyzer:
#     def __init__(self):
#         self.logger = logging.getLogger(__name__)
#         # GithubClient
#         self.github_client = GitHubClient()
#         self.openai_client = AsyncOpenAI()
#         # self.tavily_service = TavilyService(TavilyClient(ENV_TAVILY_API_KEY))

#     async def get_repo_does_exist(self, username: str, repository: str):
#         response = await self.github_client.get_repo_detail_links(username, repository)
#         if response.get("status") != 200:
#             return False

#         return True

#     async def analyze_repo(self, username: str, repository: str):
#         # Analyze a single repo
#         if not await self.get_repo_does_exist(username, repository):
#             raise Exception("Repository does not exist")

#         response: str = None
#         # Call the TarilyClient to do the research on the repository. Extract useful information

#         # Call a GPT model to summarize the repository in the correct tone

#         return response

#     async def fetch_repo_details(self, username, repository):
#         # Get the details of a repository. All the links for the information.
#         repo_url = f"{GITHUB_API_URL}/repos/{username}/{repository}"
#         async with httpx.AsyncClient() as client:
#             response = await client.get(repo_url, headers={
#                 "Accept": "application/vnd.github.v3+json",
#             })
#             if response.status_code == 200:
#                 return response.json()
#             else:
#                 response.raise_for_status()

#     async def analyze_repo_with_gpt(self, repo_details: dict):
#         prompt = (
#             "Analyze following repository by looking at the source code, README file, commit history, pull request names, issues, stars, and follows and extract the following information: \n "
#             "1. Summary of the project including the type of project such as application, web applicaiton, mobile, machine learning, robotics, data engineering, etc. \n "
#             "2. Customer - who is the user of the project? Was it built for personal use or are there other users of the application. Also see what industry this project contributes to as well as the problem it solves \n "
#             "3. Recency - How recent is the project? When was the last commit made? Was there a time when it was contributed regularly?\n "
#             "4. Demo - Is there evidence of a demo or a live version of the project? Can you find a link to the demo?\n "
#             "5. Technologies uses: What technologies are used in the project? What languages, frameworks, libraries, and tools are used in the project? Include porgramming languages, frameworks, libraries, cloud providers, cloud components, database types, cache types and other software components utilized in this applciation \n "
#             "6. Software Techniques: What software techniques are used in the project? What design patterns, software architecture, software development methodologies, and software development practices are used in the project, such as types of testing, monitoring, logging, readability, multiple environments, user sessions, caching, threading, orchestration, race conditioning, machine learning, etc.? Also look at framework specific techniques. \n "
#             "7. Critics: What are the critics of the project? What are the issues, pull requests, and comments that are made on the project? What are the issues that are open and closed? What are the pull requests that are open and closed? Are there any anti-patterns in the code base from the languages and framewokrs used? Are there any bad coding practices found in the code base?\n "
#             f"\nHere are the repository details: {repo_details}\n "
#         )
#         # ENV_OPENAI_API_KEY
#         # Get from .env file
#         openai.api_key = os.getenv(ENV_OPENAI_API_KEY)
#         stream = await self.openai_client.chat.completions.create(
#             model="gpt-4",
#             messages=[{"role": "user", "content": prompt}],
#             stream=True,
#         )

#         response = ""
#         async for chunk in stream:
#             print(chunk.choices[0].delta.content or "", end="")
#             response += chunk.choices[0].delta.content or ""

#         self.logger.info(
#             "[GitHubAnalyzer:analyze_repo_with_gpt] waiting for stream to close")
#         await stream.close()
#         self.logger.info(
#             "[GitHubAnalyzer:analyze_repo_with_gpt] stream closed")
#         ag_prompt = (
#             "Take the following summary and put it into a json object with the following keys: \n"
#             "1. summary \n"
#             "2. problem_statement \n"
#             "3. recency_description \n"
#             "4. demo_description \n"
#             "5. technologies_description for technologies used\n"
#             "6. techniques_description for Software techniques used\n"
#             "7. critics_description \n"
#             f"\n{response}"
#         )
#         stream = await self.openai_client.chat.completions.create(
#             model="gpt-4",
#             messages=[{"role": "user", "content": ag_prompt}],
#             stream=True,
#         )
#         str_res = ""
#         async for chunk in stream:
#             print(chunk.choices[0].delta.content or "", end="")
#             str_res += chunk.choices[0].delta.content or ""
#         print("\n\n\n\nTHIS IS THE JSON RESPONSE\n")
#         print(str_res)
#         json_res = json.loads(str_res)
#         print("\n\n\n\nTHIS IS THE JSON RESPONSE\n")
#         print(json_res)
#         return json_res

#     async def fetch_repo_contents(self, repo_url: str):

#         repo_name = repo_url.replace("https://github.com/", "")
#         url = f"{GITHUB_API_URL}/{repo_name}"
#         url = "https://api.github.com/repos/josephmhernandez/lyfe-captures/contents"
#         headers = {
#             #     'Authorization': f'token {GITHUB_API_KEY}'
#         }

#         async with httpx.AsyncClient() as client:
#             response = await client.get(url, headers=headers)
#             response.raise_for_status()
#             return response.json()

#     async def fetch_file_content(self, file_url: str, headers: dict):
#         async with httpx.AsyncClient() as client:
#             response = await client.get(file_url, headers=headers)
#             response.raise_for_status()
#             return response.text

#     async def aggregate_code(self, repo_contents):
#         headers = {
#             # 'Authorization': f'token {GITHUB_API_KEY}'
#         }

#         aggregated_code = ""
#         for item in repo_contents:
#             if item['type'] == 'file':
#                 file_content = await self.fetch_file_content(item['download_url'], headers)
#                 aggregated_code += f"\n\n{item['path']}\n{file_content}\n"
#         return aggregated_code

#     async def analyze_code_with_openai(self, aggregated_code: str):
#         openai.api_key = os.getenv(ENV_OPENAI_API_KEY)
#         # Write the aggregated code to a file
#         with open("aggregated_code.txt", "w") as f:
#             f.write(aggregated_code)

#         message = """
#             take in the GitHub profile of the user and extract the projects that the user has worked on. Provide relevant information about each repository, including the name of the project, description of the project, type of application (e.g., web application, tool, library, machine learning model, etc.), languages used, popular libraries used, function of the project, the date the project started, and the date of the last commit. Ensure the summary is in-depth and technical. Make sure to look at the README files available to get a better understanding on why the project was created. The summary will be read by engineers, so highlight techniques in computer science and software engineering that the user included in their repository. The summaries should include the type of framework used and common software engineering techniques. If any information is missing or unclear, Repo Analyzer should fill in the details itself. Repo Analyzer should maintain an objective tone, calling out any anti-patterns found in the code and highlighting good software engineering practices used in the repository. Additionally, Repo Analyzer should identify areas where the candidate has shown software expertise across various domains including Programming Languages (General-Purpose, Functional, Scripting), Web Development (Front-End, Back-End), Mobile Development, Data Science and Machine Learning, DevOps and Infrastructure, Database Management, Cybersecurity, Networking, Software Architecture and Design, Testing and Quality Assurance, Game Development, Embedded Systems, UI/UX Design, Blockchain and Cryptography, Artificial Intelligence, Robotics and IoT. It should also highlight the use of common Cloud computing systems like GCP, AWS, Azure, Heroku, etc. Repo Analyzer will pull the most recent 5 GitHub repositories each user has committed to.

#             Analyze the repo: lyfe-captures:

#             { id: 521068652, node_id: 'R_kgDOHw7gbA', name: 'lyfe-captures', full_name: 'josephmhernandez/lyfe-captures', private: false, owner: { login: 'josephmhernandez', id: 52683746, node_id: 'MDQ6VXNlcjUyNjgzNzQ2', avatar_url: 'https://avatars.githubusercontent.com/u/52683746?v=4', gravatar_id: '', url: 'https://api.github.com/users/josephmhernandez', html_url: 'https://github.com/josephmhernandez', followers_url: 'https://api.github.com/users/josephmhernandez/followers', following_url: 'https://api.github.com/users/josephmhernandez/following{/other_user}', gists_url: 'https://api.github.com/users/josephmhernandez/gists{/gist_id}', starred_url: 'https://api.github.com/users/josephmhernandez/starred{/owner}{/repo}', subscriptions_url: 'https://api.github.com/users/josephmhernandez/subscriptions', organizations_url: 'https://api.github.com/users/josephmhernandez/orgs', repos_url: 'https://api.github.com/users/josephmhernandez/repos', events_url: 'https://api.github.com/users/josephmhernandez/events{/privacy}', received_events_url: 'https://api.github.com/users/josephmhernandez/received_events', type: 'User', site_admin: false }, html_url: 'https://github.com/josephmhernandez/lyfe-captures', description: 'NextJS project to create user generated maps ', fork: false, url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures', forks_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/forks', keys_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/keys{/key_id}', collaborators_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/collaborators{/collaborator}', teams_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/teams', hooks_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/hooks', issue_events_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/issues/events{/number}', events_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/events', assignees_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/assignees{/user}', branches_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/branches{/branch}', tags_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/tags', blobs_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/git/blobs{/sha}', git_tags_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/git/tags{/sha}', git_refs_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/git/refs{/sha}', trees_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/git/trees{/sha}', statuses_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/statuses/{sha}', languages_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/languages', stargazers_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/stargazers', contributors_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/contributors', subscribers_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/subscribers', subscription_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/subscription', commits_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/commits{/sha}', git_commits_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/git/commits{/sha}', comments_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/comments{/number}', issue_comment_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/issues/comments{/number}', contents_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/contents/{+path}', compare_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/compare/{base}...{head}', merges_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/merges', archive_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/{archive_format}{/ref}', downloads_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/downloads', issues_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/issues{/number}', pulls_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/pulls{/number}', milestones_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/milestones{/number}', notifications_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/notifications{?since,all,participating}', labels_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/labels{/name}', releases_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/releases{/id}', deployments_url: 'https://api.github.com/repos/josephmhernandez/lyfe-captures/deployments', created_at: '2022-08-04T00:09:22Z', updated_at: '2024-06-18T22:48:21Z', pushed_at: '2024-02-01T17:34:51Z', git_url: 'git://github.com/josephmhernandez/lyfe-captures.git', ssh_url: 'git@github.com:josephmhernandez/lyfe-captures.git', clone_url: 'https://github.com/josephmhernandez/lyfe-captures.git', svn_url: 'https://github.com/josephmhernandez/lyfe-captures', homepage: null, size: 148779, stargazers_count: 0, watchers_count: 0, language: 'JavaScript', has_issues: true, has_projects: true, has_downloads: true, has_wiki: true, has_pages: false, has_discussions: false, forks_count: 0, mirror_url: null, archived: false, disabled: false, open_issues_count: 2, license: null, allow_forking: true, is_template: false, web_commit_signoff_required: false, topics: [], visibility: 'public', forks: 0, open_issues: 2, watchers: 0, default_branch: 'master', lastCommitDate: '2024-02- &#8203;:citation[oaicite:0]{index=0}&#8203
#         """

#         # prompt = f"Analyze the following code repository:\n\n{aggregated_code}",
#         response = await self.openai_client.chat.completions.create(
#             model="gpt-4o",
#             messages=[{"role": "user", "content": message}],
#             max_tokens=1500
#         )
#         self.logger.info(
#             "[GitHubAnalyzer:analyze_code_with_openai] response from openai: %s", response)
#         return response.choices[0].message
#         # return "woof"

#     async def aggregate_results(self, analysis):
#         # Aggregate the results of the analysis
#         pass
