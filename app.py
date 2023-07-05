from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import ssl

from routes import Routes

from config import SSL_PATH, host, port, SQLALCHEMY_DATABASE_URI






class App(Routes):
    
    def __init__(self):
        self._app = Flask(__name__)
        self._app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        self.db = SQLAlchemy(self._app)

        super().__init__(self.db)

        self.init_routes()

    
    def init_routes(self):

        def index():
            from models import Lead

            with self._app.app_context():
                result: Lead = Lead.query.first()

                name = None
                if result:
                    name = result.name

                return {"first_lead_name": f"{name}"}
        
        self._app.add_url_rule('/', view_func=index, methods=['GET'])
            
        self._app.add_url_rule('/lead/create', view_func=self.create_lead, methods=['POST'])
        self._app.add_url_rule('/lead/delete', view_func=self.delete_lead, methods=['POST'])
        self._app.add_url_rule('/lead/update', view_func=self.update_lead, methods=['POST'])
        self._app.add_url_rule('/lead/read', view_func=self.get_lead, methods=['GET'])


    def run(self):
        payload = {
            "host": host,
            "port": port,
        }

        if not SSL_PATH.local:
            ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            ssl_context.load_cert_chain(SSL_PATH.cert, SSL_PATH.key)
            payload["ssl_context"] = ssl_context

        self._app.run(**payload)
