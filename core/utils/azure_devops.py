import requests
import json
import typing
from requests.exceptions import HTTPError
"TODO: if necessary, refactor this to use the Azure Devops libraries for python instead of direct API calls."
"TODO: optimize these api calls."


class AzureDevops:
    def __init__(self, token: str, project: str):
        """
        Builds a connection to an Azure Devops project with token security.
        :param token: (str) personal access token issued by project´s administrator.
        :param project: (str) project name that comes right after organization´s name.
        """
        self.token = token
        self.project = project
        self.host = 'dev.azure.com/onsvsts'
        self.api = 'api-version=5.0'

    def list_repos(self, forks=False) -> typing.List:
        """
        Returns a dictionary from a json string with repos that a project has from an Azure git repo.
        The repo must start with the project´s given name, otherwise it will not return.
        :param forks: (bool) return all projects, including factory forks. Default: False.
        :return: dict
        """
        url = f"https://user:{self.token}@{self.host}/{self.project}/_apis/git/repositories?{self.api}"
        response = requests.get(url)
        raw_git_repos = json.loads(response.content)

        # Get only repos that belong to the same project. (i.e., 'sager.migracao' contains 'sager' as project name)
        all_git_repos = [repo for repo in raw_git_repos['value'] if str(repo.get('name')).startswith(self.project)]

        # If the user wants all repos, set forks=True. Default is forks=False.
        if forks:
            return all_git_repos

        # Get only the repos that are not forks and are not empty
        repo_list = [repo for repo in all_git_repos if not repo.get('isFork') and repo.get('size') >= 512]

        return repo_list

    def get_app_name(self, repo_id: str, file='plataforma.json') -> typing.AnyStr:
        """
        Returns a string containing the app name inside the given configuration file. Default is plataforma.json.
        :param repo_id: this is the unique repository identification.
        :param file: (json) expects a json file in a standard format. Default is set to plataforma.json at root path.
        :return: full app name
        """
        url = f"https://user:{self.token}@{self.host}/{self.project}/_apis/git/repositories/{repo_id}" \
              f"/items?path={file}&{self.api}"
        try:
            response = requests.get(url)
            app_info = json.loads(response.content)
            return app_info['app']['name']
        except HTTPError as http_error:
            return f"Error has occurred: {http_error}"
        except Exception as error:
            return f"Something else happened: {error}"

    @staticmethod
    def list_repo_id(repo_list: list) -> typing.List:
        """
        Returns a list of IDs of the repos, necessary to access files
        :param repo_list: (list) expects a list of git repositories inside a project.
        :return: list of IDs extracted from the repository list.
        """
        return [item['id'] for item in repo_list]


"""
https://weo6dxvr6l6e557q3feya7ijqfxxxfmfyhnat4fnqxawouoydvdq@dev.azure.com/onsvsts/98eb6763-31af-4542-b1bf-36efe247bd5b/_apis/git/repositories/9c638fbe-34e9-4193-9b44-02f2e5c60797/blobs/8801b92e16baee07488211ef4e84f4daeecae3f2


https://user:weo6dxvr6l6e557q3feya7ijqfxxxfmfyhnat4fnqxawouoydvdq@dev.azure.com/onsvsts/98eb6763-31af-4542-b1bf-36efe247bd5b/_apis/git/repositories/9c638fbe-34e9-4193-9b44-02f2e5c60797/items?path=/Mapa&api-version=5.0

{
    "objectId": "57c1095d8097af10eff593fa70f18b15cef987cb",
    "gitObjectType": "tree",
    "commitId": "f7af50022a220dd89d49c11a53d4dd1dbc01e861",
    "path": "/Mapa",
    "isFolder": true,
    "url": "https://dev.azure.com/onsvsts/98eb6763-31af-4542-b1bf-36efe247bd5b/_apis/git/repositories/9c638fbe-34e9-4193-9b44-02f2e5c60797/items?path=%2FMapa&versionType=Branch&versionOptions=None",
    "_links": {
        "self": {
            "href": "https://dev.azure.com/onsvsts/98eb6763-31af-4542-b1bf-36efe247bd5b/_apis/git/repositories/9c638fbe-34e9-4193-9b44-02f2e5c60797/items?path=%2FMapa&versionType=Branch&versionOptions=None"
        },
        "repository": {
            "href": "https://dev.azure.com/onsvsts/98eb6763-31af-4542-b1bf-36efe247bd5b/_apis/git/repositories/9c638fbe-34e9-4193-9b44-02f2e5c60797"
        },
        "tree": {
            "href": "https://dev.azure.com/onsvsts/98eb6763-31af-4542-b1bf-36efe247bd5b/_apis/git/repositories/9c638fbe-34e9-4193-9b44-02f2e5c60797/trees/57c1095d8097af10eff593fa70f18b15cef987cb"
        }
    }
}



https://user:weo6dxvr6l6e557q3feya7ijqfxxxfmfyhnat4fnqxawouoydvdq@dev.azure.com/onsvsts/98eb6763-31af-4542-b1bf-36efe247bd5b/_apis/git/repositories/9c638fbe-34e9-4193-9b44-02f2e5c60797/trees/57c1095d8097af10eff593fa70f18b15cef987cb

{
    "objectId": "57c1095d8097af10eff593fa70f18b15cef987cb",
    "url": "https://dev.azure.com/onsvsts/98eb6763-31af-4542-b1bf-36efe247bd5b/_apis/git/repositories/9c638fbe-34e9-4193-9b44-02f2e5c60797/trees/57c1095d8097af10eff593fa70f18b15cef987cb",
    "treeEntries": [
        {
            "objectId": "8801b92e16baee07488211ef4e84f4daeecae3f2",
            "relativePath": "SAGER_Evento.map.yaml",
            "mode": "100644",
            "gitObjectType": "blob",
            "url": "https://dev.azure.com/onsvsts/98eb6763-31af-4542-b1bf-36efe247bd5b/_apis/git/repositories/9c638fbe-34e9-4193-9b44-02f2e5c60797/blobs/8801b92e16baee07488211ef4e84f4daeecae3f2",
            "size": 9572
        }
    ],
    "size": 49,
    "_links": {
        "self": {
            "href": "https://dev.azure.com/onsvsts/98eb6763-31af-4542-b1bf-36efe247bd5b/_apis/git/repositories/9c638fbe-34e9-4193-9b44-02f2e5c60797/trees/57c1095d8097af10eff593fa70f18b15cef987cb"
        },
        "repository": {
            "href": "https://dev.azure.com/onsvsts/98eb6763-31af-4542-b1bf-36efe247bd5b/_apis/git/repositories/9c638fbe-34e9-4193-9b44-02f2e5c60797"
        },
        "treeEntries": {
            "href": "https://dev.azure.com/onsvsts/98eb6763-31af-4542-b1bf-36efe247bd5b/_apis/git/repositories/9c638fbe-34e9-4193-9b44-02f2e5c60797/blobs/8801b92e16baee07488211ef4e84f4daeecae3f2"
        }
    }
}




"""