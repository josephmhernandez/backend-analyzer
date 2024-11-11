
import pytest

from services.GitHubHelper import extract_github_info


@pytest.mark.parametrize("url, expected_username, expected_repo_name", [
    ("https://github.com/oweneldridge/blueprint", "oweneldridge", "blueprint"),
    ("https://github.com/oweneldridge/blueprint/", "oweneldridge", "blueprint"),
    ("https://github.com/josephmhernandez/lyfe-captures/",
     "josephmhernandez", "lyfe-captures"),
    ("https://github.com/josephmhernandez/tile-engine",
     "josephmhernandez", "tile-engine"),
    ("https://github.com/jamessteeleuf/phoenix_demo",
     "jamessteeleuf", "phoenix_demo"),
])
def test_extract_github_info_returns_correct_values(url, expected_username, expected_repo_name):
    username, repo_name = extract_github_info(url)
    assert username == expected_username
    assert repo_name == expected_repo_name
