# user_auth/services.py

import requests

PMC_API_BASE_URL = 'https://pmc.gov.pk/api/DRC'

def verify_pmdc_number(pmdc_no):
    try:
        # Step 1: Fetch basic doctor information
        response = requests.post(
            f"{PMC_API_BASE_URL}/GetData",
            headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
            data={'RegistrationNo': pmdc_no, 'Name': '', 'FatherName': ''}
        )
        response_data = response.json()

        if not response_data.get('status') or not response_data.get('data'):
            return {'status': False, 'message': 'Doctor not found'}

        doctor_data = response_data['data'][0]

        # Step 2: Fetch the doctor’s qualifications
        qualification_response = requests.post(
            f"{PMC_API_BASE_URL}/GetQualifications",
            headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
            data={'RegistrationNo': pmdc_no}
        )
        qualification_data = qualification_response.json()

        if qualification_data.get('status'):
            doctor_data['qualifications'] = qualification_data['data']['Qualifications']
        else:
            doctor_data['qualifications'] = []

        return {'status': True, 'doctor': doctor_data}
    except Exception as e:
        return {'status': False, 'message': 'API error', 'error': str(e)}
