# ENV Variables
ENV_TAVILY_API_KEY = "TAVILY_API_KEY"
ENV_OPENAI_API_KEY = "OPENAI_API_KEY"
GITHUB_API_URL = "https://api.github.com"

GITHUB_GET_REPOSITORY_URL = GITHUB_API_URL + "users/{username}/repos"
GITHUB_GET_COMMITS_URL = GITHUB_API_URL + \
    "repos/{username}/{repositoryName}/commits"


GITHUB_SEARCH_QUERIES = [
    "Search the respository {repositoryName} for the user {username} and look at the commit history, names of pull requests, issues, stars, README file, followers, and the source code to extract the following information about the repository: 1. Summary of the project (including type of project such as app, tool, library, web application, mobile, machine learning model, robotics, etc.), 2. ",
]
