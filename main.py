# imports the createapp function from __init__.py
from app import create_app
from app.models import Admins, User
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash


# pass app as app since create_app will return app
app = create_app() # this then means app = app
db = SQLAlchemy(app)

adminExists = Admins.query.all()

if not adminExists:
    defualt_admin = User(first_name='Beauty', last_name='John', phone='090', email='beautyjohn986@gmail.com', cv=1, password=generate_password_hash('1234'), image='none')
    db.session.add(defualt_admin)
    db.session.commit()

    getAdmin = User.query.filter_by(email='beautyjohn986@gmail.com').first()
    new_admin = Admins(user_id=getAdmin.id, active=True)
    db.session.add(new_admin)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, port=8080) #set debug to true in development