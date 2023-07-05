
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from utils.crypt import get_crypt_data, get_decrypt_data

from utils import Validator as valid




class Routes:

    

    def __init__(self, db):
        self.db = db
        

    
    

    def create_lead(self):
        from models import Lead

        data:dict = request.get_json()

        print(data)

        for arg in ['name', 'email', 'phone', 'ip_address']:
            if arg not in data:
                return jsonify({"error": "Expected '{}' arg".format(arg)}), 400
            
        name = data.get("name")
        email = data.get('email').strip()
        phone = data.get('phone').strip().replace("+", "")
        ip_address = data.get('ip_address').strip()


        if not valid.email(email):
            return jsonify({'error': 'Invalid email format'}), 400

        if not valid.phone(phone):
            return jsonify({'error': 'Invalid phone number format'}), 400

        if Lead.query.filter_by(ip_address=ip_address).first():
            return jsonify({'error': 'Lead with the same IP address already exists'}), 400

        if Lead.query.filter((Lead.email == email) | (Lead.phone == phone)).first():
            return jsonify({'error': 'Lead with the same email or phone number already exists'}), 400
        
        timestamp = datetime.now().timestamp()
        payload = {
            "name": name,

            "email": get_crypt_data(email).decode(),
            "phone": get_crypt_data(phone).decode(),

            "ip_address": ip_address,
            "timestamp": timestamp,
        }

        lead = Lead(**payload)
        self.db.session.add(lead)
        self.db.session.commit()

        new_lead = Lead.query.filter_by(timestamp=timestamp).first()

        payload = {
            'success': 'Lead created successfully',
            "lead_id": new_lead.id,
        }
        return jsonify(payload), 201
    

    def delete_lead(self):
        from models import Lead

        lead_id = request.args.get('lead_id')
        
        lead = Lead.query.get(lead_id)

        if not lead:
            return jsonify({'error': 'Lead with this id not found'}), 404

        self.db.session.delete(lead)
        self.db.session.commit()

        return jsonify({'success': 'Lead deleted successfully'})


    def get_lead(self):
        from models import Lead

        lead_id = request.args.get('lead_id')

        if not lead_id:
            return jsonify({'error': 'Not found lead_id arg'}), 404

        lead: Lead = Lead.query.get(lead_id)

        if not lead:
            return jsonify({'error': 'Lead with this id not found'}), 404

        lead_data = {
            'id': lead.id,
            'name': lead.name,
            'email': get_decrypt_data(lead.email.encode()),
            'phone': get_decrypt_data(lead.phone.encode()),
            'ip_address': lead.ip_address,
            'timestamp': lead.timestamp
        }

        return jsonify(lead_data)


    def update_lead(self):
        from models import Lead

        lead_id = request.args.get('lead_id')
        lead: Lead = Lead.query.get(lead_id)

        if not lead:
            return jsonify({'error': 'Lead with this id not found'}), 404

        data:dict = request.args

        email = data.get("email", '')
        phone = data.get("phone", "")
        ip_address = data.get("ip_address", "")

        if email and not valid.email(email):
            return jsonify({'error': 'Invalid email format'}), 400

        if phone and not valid.phone(phone):
            return jsonify({'error': 'Invalid phone number format'}), 400

        if ip_address and Lead.query.filter_by(ip_address=ip_address).first():
            return jsonify({'error': 'Lead with the same IP address already exists'}), 400

        if email or phone:
            existing_lead: Lead = Lead.query.filter(
                (Lead.email == get_crypt_data(email).decode()) |
                (Lead.phone == get_crypt_data(phone).decode())
            ).first()

            if existing_lead and existing_lead.id != lead.id:
                return jsonify({'error': 'Lead with the same email or phone number already exists'}), 400

        
        if email:
            lead.email = get_crypt_data(email).decode()
        if phone:
            lead.phone = get_crypt_data(phone).decode()

        lead.name = data.get('name', lead.name)
        lead.ip_address = data.get('ip_address', lead.ip_address)
        lead.timestamp = datetime.now().timestamp()

        self.db.session.commit()

        return jsonify({'success': 'Lead updated successfully'})
    