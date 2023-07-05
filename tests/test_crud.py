import pytest
import requests
import time

from config import host, port


test_leads = []


@pytest.fixture(scope='session', autouse=True)
def url():
    return "http://{}:{}".format(host, port)


def test_lead_crud(url):
    data = {
        'name': 'Jane Doe',
        'email': 'janedoe@example.com',
        'phone': '9876543210',
        'ip_address': '127.0.0.1'
    }

    response = requests.post(f'{url}/lead/create', json=data)
    json_data = response.json()
    
    assert "success" in json_data
    assert response.status_code == 201

    lead_id = json_data['lead_id']
    
    time.sleep(1)

    response = requests.get(f'{url}/lead/read?lead_id={lead_id}')
    
    assert response.status_code == 200, f"{response.text} |||| {lead_id}"

    time.sleep(1)

    new_data = {
        'lead_id': lead_id,
        'name': 'Updated Name',
        'email': 'updatedemail@example.com',
        'phone': '9876543210',
        'ip_address': '127.0.0.2'
    }
    
    response = requests.post(f'{url}/lead/update', params=new_data)

    assert response.status_code == 200, f"{response.text} |||| {lead_id}"
    assert response.json() == {'success': 'Lead updated successfully'}, f"{response.text} |||| {lead_id}"

    time.sleep(1)

    response = requests.post(f'{url}/lead/delete?lead_id={lead_id}')

    assert response.status_code == 200, f"{response.text} |||| {lead_id}"
    assert response.json() == {'success': 'Lead deleted successfully'}, f"{response.text} |||| {lead_id}"
