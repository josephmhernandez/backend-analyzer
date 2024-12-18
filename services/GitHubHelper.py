# # Static helper methods

# import logging
# import re


# logger = logging.getLogger(__name__)


# def extract_github_info(url: str):
#     # Regular expression to match GitHub URLs
#     pattern = r"https?://(?:www\.)?github\.com/([^/]+)/([^/]+)(?:/|$)"

#     match = re.match(pattern, url)

#     logger.info(f"Match: {match}")
#     if match:
#         username = match.group(1)
#         repo_name = match.group(2)

#         # Check if the repository name ends with ".git" and remove it if so
#         if repo_name.endswith('.git'):
#             repo_name = repo_name[:-4]

#         return username, repo_name
#     else:
#         return None, None  # Return None if the URL doesn't match

# # # Example usage
# # url = "https://github.com/username/repoName"
# # username, repo_name = extract_github_info(url)
# # print(f"Username: {username}, Repo Name: {repo_name}")
