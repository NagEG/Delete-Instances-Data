from distutils.log import debug
from email import header
import requests
import json
from flask import Flask, request

app = Flask(__name__)

error_msgs = 'Please check AccessToken & Environemnt both are in sync?'

def get_auth_headers(request):
    return {
        'x-auth-user': request.headers.get('x-auth-user', ''),
        'x-auth-permissions': request.headers.get('x-auth-permissions', ''),
        'Authorization': request.headers.get('Authorization', ''),
    }

@app.route('/delete/<path:index>', methods=['GET', 'POST'])
def delete_HugeData(index):
    headers = {'authorization': get_auth_headers(request)['Authorization']}
    if 'analysis' in index.lower():
        return analysis(request, index, headers=headers)
    elif 'sets' in index:
        return sets(request ,index, headers=headers)
    elif 'explorations' in index.lower():
       return explorations(request, index, headers=headers)
    elif 'comparisons' in index.lower():
        return comparisons(request, index, headers=headers)
    elif 'investigations' in index.lower():
        return investigations(request, index, headers=headers)
    elif 'pipeline' in index.lower():
        return pipeline(request, index, headers=headers)
    else:
        return 'BOSS'


def analysis(request, index, headers):
    offset = request.args.get('offset', 0)
    limit = request.args.get('limit', 10)
    analysisArgs ='analysis' 
    environMent = index[0]
    environMent = index.split('/')
    get_all_ids = f'https://ediscover-{environMent[0]}.edatascientist.com/{analysisArgs}/EDA??offset={offset}&limit={limit}'
    print('get_all_ids', get_all_ids)
    response = requests.get(get_all_ids, headers=headers)
    if response.status_code != 401 and response.status_code != 404:
        listExplorations = response.json()['_embedded']['analysis']
        print('listExplorations', listExplorations)
        for oneEXP in listExplorations:
            id = oneEXP['id']
            deletableUrl = f'https://ediscover-{environMent[0]}.edatascientist.com/{analysisArgs}/EDA/{id}'
            response = requests.delete(deletableUrl, headers=headers)
        if response.status_code == 200:
            return f'{analysisArgs.upper()} DELETED SUCESSFULLY'
    else:
        return f'FAILED TO DELETE {analysisArgs.upper()}, {error_msgs}'


def pipeline(request, index, headers):
    PipelineArgs ='epipeline/pipelinerun' 
    offset = request.args.get('offset', 0)
    limit = request.args.get('limit', 10)
    environMent = index[0]
    environMent = index.split('/')
    print('environMent', environMent)
    if environMent[2] == 'pipelinerun':
        view = environMent[1]
    elif environMent[2] == 'study':
        view = environMent[2]
    get_all_ids = f'https://ediscover-{environMent[0]}.edatascientist.com/{PipelineArgs}?view={view}&offset={offset}&limit={limit}'

    response = requests.get(get_all_ids, headers=headers)
    print('response.json()',response.json())
    if environMent[2] == 'pipelinerun': 
        listPipeLine = response.json()['_embedded']['pipelinerun']
    else:
        listPipeLine = response.json()['_embedded']['studies']
        PipelineArgs = 'epipeline/study'
    print('listPipeLine', listPipeLine)
    for oneEXP in listPipeLine:
        if environMent[2] == 'pipelinerun':
            id = oneEXP['pipelinerun_id']
        else:
            id = oneEXP['id']
        deletableUrl = f'https://ediscover-{environMent[0]}.edatascientist.com/{PipelineArgs}/{id}'
        response = requests.delete(deletableUrl, headers=headers)
    if response.status_code == 200:
        return f'{PipelineArgs.upper()} DELETED SUCESSFULLY'
    else:
        return f'FAILED TO DELETE {PipelineArgs.upper()}, {error_msgs}'


def sets(request, index, headers):
    offset = request.args.get('offset', 0)
    limit = request.args.get('limit', 10)
    SetArgs ='sets' 
    environMent = index[0]
    environMent = index.split('/')
    get_all_ids = f'https://ediscover-{environMent[0]}.edatascientist.com/{SetArgs}?offset={offset}&limit={limit}'

    response = requests.get(get_all_ids, headers=headers)
    if response.status_code == 404 or response.status_code == 401:
        return error_msgs
    else:
        listSets = response.json()['_embedded']['sets']
        print('LIST------>\n', len(listSets))
        for oneEXP in listSets:
            id = oneEXP['id']
            deletableUrl = f'https://ediscover-{environMent[0]}.edatascientist.com/{SetArgs}/{id}?type=comparisons'
            response = requests.delete(deletableUrl, headers=headers)
            abc = f'{SetArgs.upper()} --> {id} DELETED SUCESSFULLY'
            print(abc)
        if response.status_code == 200 or response.status_code == 204:
            return f'{SetArgs.upper()} --> {id} DELETED SUCESSFULLY'
        else:
            return f'FAILED TO DELETE {SetArgs.upper()} --> {id}, {error_msgs}'


def investigations(request, index, headers):
    offset = request.args.get('offset', 0)
    limit = request.args.get('limit', 10)
    investigationsArgs ='investigations' 
    environMent = index[0]
    environMent = index.split('/')
    get_all_ids = f'https://ediscover-{environMent[0]}.edatascientist.com/{investigationsArgs}?offset={offset}&limit={limit}'

    response = requests.get(get_all_ids, headers=headers)
    if response.status_code == 404 or response.status_code == 401:
        return error_msgs
    else:
        InvestigationList = response.json()['_embedded']['investigations']
        print('LIST------>\n', len(InvestigationList))
        for oneEXP in InvestigationList:
            id = oneEXP['id']
            deletableUrl = f'https://ediscover-{environMent[0]}.edatascientist.com/{investigationsArgs}/{id}'
            response = requests.delete(deletableUrl, headers=headers)
            abc = f'{investigationsArgs.upper()} --> {id} DELETED SUCESSFULLY'
            print(abc)
        if response.status_code == 200 or response.status_code == 204:
            return f'{investigationsArgs.upper()} --> {id} DELETED SUCESSFULLY'
        else:
            return f'FAILED TO DELETE {investigationsArgs.upper()} --> {id}, {error_msgs}'

def explorations(request, index, headers):
    offset = request.args.get('offset', 0)
    limit = request.args.get('limit', 10)
    exporationArgs ='explorations' 
    environMent = index[0]
    environMent = index.split('/')
    get_all_ids = f'https://ediscover-{environMent[0]}.edatascientist.com/{exporationArgs}?offset={offset}&limit={limit}&type=exploration'
    response = requests.get(get_all_ids, headers=headers)
    listExplorations = response.json()['_embedded']['explorations']
    for oneEXP in listExplorations:
        id = oneEXP['id']
        deletableUrl = f'https://ediscover-{environMent[0]}.edatascientist.com/explorations/{id}?type=exploration'
        response = requests.delete(deletableUrl, headers=headers)
        abc = f'Deleted -->{id},  {response.status_code}'
        print(abc)
    if response.status_code == 200 or response.status_code == 204:
        return f'{exporationArgs.upper()} DELETED SUCESSFULLY'
    else:
        return f'FAILED TO DELETE {exporationArgs.upper()},{error_msgs}'

def comparisons(request, index, headers):
    offset = request.args.get('offset', 0)
    limit = request.args.get('limit', 10)
    comparisonArgs ='comparisons' 
    environMent = index[0]
    environMent = index.split('/')
    get_all_ids = f'https://ediscover-{environMent[0]}.edatascientist.com/{comparisonArgs}?offset={offset}&limit={limit}'
    print('DELETE API--->\n', get_all_ids)
    response = requests.get(get_all_ids, headers=headers)
    if response.status_code == 404 or response.status_code == 401:
        return error_msgs
    else:
        listComparisons = response.json()['_embedded']['comparisons']
        for oneEXP in listComparisons:
            id = oneEXP['id']
            deletableUrl = f'https://ediscover-{environMent[0]}.edatascientist.com/{comparisonArgs}/{id}?type=comparisons'
            response = requests.delete(deletableUrl, headers=headers)
            abc = f'Deleted -->{id},  {response.status_code}'
            print(abc)
        if response.status_code == 200 or response.status_code == 204:
            return f'{comparisonArgs.upper()} DELETED SUCESSFULLY'
        else:
            return f'FAILED TO DELETE {comparisonArgs.upper()}, {error_msgs}'



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9999, debug=True)