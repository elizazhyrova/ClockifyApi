import json
import requests
from pprint import pprint
from typing import Dict, Any, List, Union
from config import data, BASE_ENDPOINT


def print_all_tasks(workspaces: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    workspace_projects = {}
    for each in workspaces:
        workspace_id = each['id']
        tasks_in_projects = get_projects_by_workspace(workspace_id)
        workspace_projects[each['name']] = tasks_in_projects
    return workspace_projects


def get_projects_by_workspace(workspace_id: str) -> Dict[str, Any]:
    projects = get_info_from_api(end_url=f'workspaces/{workspace_id}/projects')
    tasks_project = {}
    for each in projects:
        project_id = each['id']
        tasks = get_info_from_api(end_url=f'workspaces/{workspace_id}/projects/{project_id}/tasks')
        tasks_names = [task['name'] for task in tasks]
        tasks_project[each['name']] = tasks_names
    return tasks_project


def get_info_from_api(end_url: str) -> Union[List[Dict], Dict[str, Any]]:
    result_bytes = requests.get(BASE_ENDPOINT + end_url, headers=data)
    result = json.loads(result_bytes.content.decode("utf-8"))
    return result


if __name__ == "__main__":
    list_of_workspaces = get_info_from_api(end_url="workspaces")
    pprint(print_all_tasks(list_of_workspaces))
