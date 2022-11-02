import json
import sys
import requests
from typing import Dict, Any, List, Union
from config import data, BASE_ENDPOINT


def print_all_tasks(workspaces: List[Dict[str, Any]]) -> str:
    workspace_projects = {}
    for each in workspaces:
        workspace_id = each['id']
        tasks_in_projects = get_projects_by_workspace(workspace_id)
        workspace_projects[each['name']] = tasks_in_projects
    return str(workspace_projects).replace('{', '\n').replace('}', '\n')


def get_projects_by_workspace(workspace_id: str) -> Dict[str, Any]:
    projects = get_info_from_api(end_url=f'workspaces/{workspace_id}/projects')
    tasks_project = {}
    for each in projects:
        project_id = each['id']
        tasks = get_info_from_api(end_url=f'workspaces/{workspace_id}/projects/{project_id}/tasks')
        tasks_names = [task['name'] for task in tasks]
        tasks_project[each['name']] = tasks_names
    return tasks_project


def get_info_from_api(end_url: str) -> Union[List[Dict[str, Union[Dict, Any]]], Dict[str, Any]]:
    result_bytes = requests.get(BASE_ENDPOINT + end_url, headers=data)
    result = json.loads(result_bytes.content.decode("utf-8"))
    return result


def sort_by_dates(time_entries_dict: Dict[str, Any]) -> Dict[str, Any]:
    workspaces_user_dict = {}
    for key_workspace, value_workspace in time_entries_dict.items():
        users_times_dict = {}
        for key_user, value_user in value_workspace.items():
            dates = []
            dates_dict = {}
            for each in value_user:
                date_task = each['date']
                if date_task in dates:
                    dates_dict[date_task].append({each['task_id']: {'duration': view_duration(each['duration'])}})
                else:
                    dates_dict[date_task] = [{each['task_id']: {'duration': view_duration(each['duration'])}}]
                    dates.append(date_task)

            users_times_dict[key_user] = dates_dict
        workspaces_user_dict[key_workspace] = users_times_dict
    return workspaces_user_dict


def get_sorted_time_entries(workspaces: List[Dict[str, Any]]) -> str:
    workspace_users = {}
    for each in workspaces:
        workspace_id = each['id']
        time_entries = get_users_time_entries_by_workspace(workspace_id)
        workspace_users[each['name']] = time_entries
    sorted_tasks = sort_by_dates(workspace_users)
    return str(sorted_tasks).replace('{', '\n').replace('}', '\n')


def get_users_time_entries_by_workspace(workspace_id: str) -> Dict[str, Any]:
    users = get_info_from_api(end_url=f'workspaces/{workspace_id}/users')
    times_users = {}
    for user in users:
        user_id = user['id']
        time_entries = get_info_from_api(end_url=f'workspaces/{workspace_id}/user/{user_id}/time-entries')
        times_users[user['name']] = [
            {
                'task_id': each['id'],
                'date': each['timeInterval']['start'].split('T')[0],
                'duration': each['timeInterval']['duration']
            }
            for each in time_entries
        ]
    return times_users


def view_duration(duration: str) -> str:
    return duration.replace('PT', '')\
        .replace('H', ' hours, ')\
        .replace('M', ' minutes, ')\
        .replace('S', ' seconds, ')


if __name__ == "__main__":
    list_of_workspaces = get_info_from_api(end_url="workspaces")
    sys.stdout.write('PART 1: Print all tasks:')
    sys.stdout.write(print_all_tasks(list_of_workspaces))
    sys.stdout.write('PART 2: Sort tasks by dates and add duration:')
    sys.stdout.write(get_sorted_time_entries(list_of_workspaces))


