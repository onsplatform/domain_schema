import requests
import typing


class AzureDevops:
    def __init__(self, token: str, project: str):
        """
        Builds a connection to an Azure Devops project with token security.
        :param token: (str) personal access token issued by project´s administrator.
        :param project: (str) project name that comes right after organization´s name.
        """
        self.authentication = ('user', token)
        self.project = project
        self.host = f'https://dev.azure.com/onsvsts/{project}/_apis/git/repositories'

    def list_repos(self, forks=False) -> typing.List:
        """
        Returns a dictionary from a json string with repos that a project has from an Azure git repo.
        The repo must start with the project´s given name, otherwise it will not return.
        :param forks: (bool) return all projects, including factory forks. Default: False.
        :return: dict
        """
        parameters = {'api-version': '5.0'}
        response = requests.get(self.host, params=parameters, auth=self.authentication)

        if response.status_code == requests.codes.ok:
            raw_git_repos = response.json()

            # Get only repos that belong to the same project. (i.e., 'sager.migracao' contains 'sager' as project name)
            all_git_repos = [repo for repo in raw_git_repos['value'] if str(repo.get('name')).startswith(self.project)]

            # If the user wants all repos, set forks=True. Default is forks=False.
            if forks:
                return all_git_repos

            # Get only the repos that are not forks and are not empty
            repo_list = [repo for repo in all_git_repos if not repo.get('isFork') and repo.get('size') > 1024]

            return repo_list

    def get_app_name(self, repo_id: str, file='plataforma.json'):
        """
        Returns a string containing the app name inside the given configuration file. Default is plataforma.json.
        :param repo_id: this is the unique repository identification.
        :param file: (json) expects a json file in a standard format. Default is set to plataforma.json at root path.
        :return: full app name
        """
        url = f"{self.host}/{repo_id}/items"
        parameters = ({'path': f'{file}', 'api-version': '5.0'})

        response = requests.get(url, params=parameters, auth=self.authentication)
        if response.status_code == requests.codes.ok:
            app_info = response.json()
            if 'app' in app_info.keys():
                return app_info['app']['name']

        return None

    def get_app_name_from_yaml(self, repo_id: str):
        """
        Extracts app name from Yaml file name.
        :return:
        """
        url = f"{self.host}/{repo_id}/items"
        parameters = {'path': '/Mapa', 'api-version': '5.0'}
        response = requests.get(url, params=parameters, auth=self.authentication)

        if response.status_code == requests.codes.ok and response.json()['isFolder']:
            tree_id = response.json().get('objectId')
            file_list = self._list_tree_entries(repo_id, tree_id)
            # from the entries, get the filename, located at 'relativePath' (SAGER_Evento.map.yaml)
            file_name: str = file_list[0]['relativePath']
            return file_name.partition('.')[0]

    def get_map_content(self, repo_id: str):
        """
        Find Yaml File and return its contents.
        :param repo_id:
        :return:
        """
        url = f"{self.host}/{repo_id}/items"
        parameters = {'path': '/Mapa', 'api-version': '5.0'}
        response = requests.get(url, params=parameters, auth=self.authentication)

        if response.status_code == requests.codes.ok and response.json()['isFolder']:
            tree_id = response.json().get('objectId')
            file_list = self._list_tree_entries(repo_id, tree_id)

            # even if there is a list, get only the first file from it.
            yaml_file = requests.get(file_list[0]['url'], auth=self.authentication)
            return yaml_file.content

    def _list_tree_entries(self, repo_id: str, tree_id: str) -> typing.List:
        """
        List the contents of the given folder (tree) for a project.
        :param repo_id: repository id, which should be a universal id.
        :param tree_id: tree id, which is a sha1 unique identification.
        :return:
        """
        url = f"{self.host}/{repo_id}/trees/{tree_id}"
        response = requests.get(url, auth=self.authentication)

        if response.status_code == requests.codes.ok:
            return response.json().get('treeEntries')

    def list_repo_id(self) -> typing.List:
        """
        Returns a list of IDs of the repos, necessary to access files
        :return: list of IDs extracted from the repository list.
        """
        repo_list = self.list_repos()
        return [item['id'] for item in repo_list]
