import requests
import msal
import cose_segrete
import json

authority_url = "https://login.microsoftonline.com/{tenant_id}".format(tenant_id = cose_segrete.TENANT_ID)
get_groups_url = "https://api.powerbi.com/v1.0/myorg/groups"
get_datasets_url = "https://api.powerbi.com/v1.0/myorg/datasets"
refresh_url = "https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/refreshes"
refresh_status_url = "https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/refreshes?$top={top_n}"



def authenticate():
    app = msal.ConfidentialClientApplication(
        cose_segrete.CLIENT_ID, authority=authority_url, client_credential=cose_segrete.SECRET_VALUE
    )
    result = app.acquire_token_by_username_password(
        cose_segrete.POWER_BI_EMAIL,
        cose_segrete.POWER_BI_PASSWORD,
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


def get_dataset(access_token, my_dataset_name = "SplitWise_Report"):
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




