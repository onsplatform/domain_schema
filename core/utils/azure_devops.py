import requests
import json
import typing


def list_repos(user: str, token: str, project: str, forks=False) -> typing.Dict:
    """
    Returns a dictionary from a json string with repos that a project has from an Azure git repo.
    The repo must start with the project´s given name, otherwise it will not return.
    :param user: (str) username that has been authorized at Azure Devops (john.doe).
    :param token: (str) personal access token issued by project´s administrator.
    :param project: (str) project name that comes right after organization´s name.
    :param forks: (bool) return all projects, including factory forks. Default: False.
    :return: dict
    """
    url = f"https://{user}:{token}@dev.azure.com/onsvsts/{project}/_apis/git/repositories?api-version=5.0"
    response = requests.get(url)
    raw_git_repos = json.loads(response)

    # Get only repos that belong to the same project. (i.e., 'sager.migracao' contains 'sager' as project name)
    all_git_repos = [repo for repo in raw_git_repos['value'] if str(repo.get('name')).startswith(project)]

    # If the user wants all repos, Fork should be True. Default is False.
    if forks:
        return all_git_repos

    # Get only the repos that are not forks and are not empty
    git_repos = [repo for repo in all_git_repos['value'] if not repo.get('isFork') and repo.get('size') >= 512]

    return git_repos

