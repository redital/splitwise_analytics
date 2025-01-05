import requests
import msal
from config import CLIENT_ID,TENANT_ID, POWER_BI_EMAIL, POWER_BI_PASSWORD, SECRET_VALUE, DATASET_NAME
import json

authority_url = "https://login.microsoftonline.com/{tenant_id}".format(tenant_id = TENANT_ID)
get_groups_url = "https://api.powerbi.com/v1.0/myorg/groups"
get_datasets_url = "https://api.powerbi.com/v1.0/myorg/datasets"
get_datasource_url = "https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/datasources"
refresh_url = "https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/refreshes"
refresh_status_url = "https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/refreshes?$top={top_n}"
update_data_source_url = "https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/Default.UpdateDatasources"


def authenticate():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID, authority=authority_url, client_credential=SECRET_VALUE
    )
    result = app.acquire_token_by_username_password(
        POWER_BI_EMAIL,
        POWER_BI_PASSWORD,
        ["https://analysis.windows.net/powerbi/api/.default"]
        )
    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception("Could not obtain access token.")


def get_groups(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(get_groups_url, headers=headers)
    return response.text


def get_datasets(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(get_datasets_url, headers=headers)
    

    res_dict = json.loads(response.text)
    
    return res_dict


def get_dataset(access_token, my_dataset_name = DATASET_NAME):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(get_datasets_url, headers=headers)

    res_dict = json.loads(response.text)
    
    my_dataset = None
    for i in res_dict["value"]:
        if i["name"] == my_dataset_name:
            my_dataset = i
    return my_dataset


def refresh(access_token,my_dataset):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post(refresh_url.format(dataset_id=my_dataset["id"]), headers=headers)
    if response.status_code != 202:
        print("Error - ",response.status_code,"-",response.text)
        raise Exception(response.text) 
    return response.status_code

def get_datasource(access_token,my_dataset):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(get_datasource_url.format(dataset_id=my_dataset["id"]), headers=headers)
    if response.status_code != 200:
        print("Error - ",response.status_code,"-",response.text)
        raise Exception(response.text) 
    return response.json()

def get_datasource_connection_details(access_token,my_dataset):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(get_datasource_url.format(dataset_id=my_dataset["id"]), headers=headers)
    if response.status_code != 200:
        print("Error - ",response.status_code,"-",response.text)
        raise Exception(response.text) 
    return response.json()["value"][0]["connectionDetails"]

def update_datasource(access_token, my_dataset, datasource_connection_details, new_public_ip):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post(
        update_data_source_url.format(dataset_id=my_dataset["id"]), 
        headers=headers, 
        json=build_update_datasource_body(datasource_connection_details,new_public_ip)
        )    
    if response.status_code != 200:
        print("Error - ",response.status_code,"-",response.text)
        raise Exception(response.text) 
    return response.status_code

def build_update_datasource_body(datasource_connection_details, new_public_ip):
    old_connection_details = datasource_connection_details
    new_connection_details = datasource_connection_details
    new_connection_details["server"] = new_public_ip
    data = {
        "updateDetails": [
            {
                "datasourceSelector": {
                    'datasourceType': 'MySql', 
                    "connectionDetails": old_connection_details,
                },
                "connectionDetails": new_connection_details,
            }
        ]
    }
    return data


def check_refresh_status(access_token,my_dataset,top_n = 1):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(refresh_status_url.format(dataset_id=my_dataset["id"],top_n=top_n), headers=headers)
    if response.status_code !=200:
        print("Error - ",response.status_code,"-",response.text)
        raise Exception(response.text) 
    res_dict = json.loads(response.text)
    
    statuses = []
    for i in res_dict["value"]:
        statuses.append(i["status"])
    return statuses
