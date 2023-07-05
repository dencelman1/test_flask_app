from sqlalchemy import Column, String, Integer, Float, Text
from routes import Routes
from main import app




class Lead(app.db.Model):
    __tablename__ = 'leads'
        
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(Text, unique=True, nullable=False)
    phone = Column(Text, nullable=False)
    ip_address = Column(String(45), unique=True, nullable=False)
    timestamp = Column(Float, nullable=False)

    def __repr__(self):
        return '<Lead id={} name={}>'.format(self.id, self.name)


with app._app.app_context():
    app.db.create_all()
    