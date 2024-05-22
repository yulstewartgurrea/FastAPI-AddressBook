from ab_app.database import engine, Base

from user.database import User
from address.database import Address 

def build_models():
	Base.metadata.create_all(bind=engine)