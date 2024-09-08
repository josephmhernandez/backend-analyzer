# Static helper methods

import re


def extract_github_info(url: str):
    # Regular expression to match GitHub URLs
    pattern = r"https?://(?:www\.)?github\.com/([^/]+)/([^/]+)(?:/|$)"

    match = re.match(pattern, url)

    if match:
        username = match.group(1)
        repo_name = match.group(2).rstrip('.git')  # Remove .git if present
        return username, repo_name
    else:
        return None, None  # Return None if the URL doesn't match

# # Example usage
# url = "https://github.com/username/repoName"
# username, repo_name = extract_github_info(url)
# print(f"Username: {username}, Repo Name: {repo_name}")
