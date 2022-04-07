from datetime import timedelta
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_required
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

db = SQLAlchemy()

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://solomon:solomonpass@localhost:5432/gc_db"
# app.config['SECRET_KEY'] = "$2a$16$BV1lQz.1A11Qy3/rY3Ei4.vB4.chNJtN6xHg4Vij115UhFtFIW6mq"
# db = SQLAlchemy(app)

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://beauty:beautee@localhost:5432/job_finder"
    app.config['SECRET_KEY'] = "$2a$16$BV1lQz.1A11Qy3/rY3Ei4.vB4.chNJtN6xHg4Vij115UsolomonhFtFIW6mq"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.app_context().push()
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .jobs import jobs
    from .admin_view import admin_view, admin_required

    app.register_blueprint(views, url_prefix='/')           
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(jobs, url_prefix='/')
    # app.register_blueprint(admin_view, url_prefix='/')

    from .models import User, Admins, Job, Job_Category, Cv

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    app.permanent_session_lifetime = timedelta(seconds=5)  

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404


    class AdminView(ModelView):
        def is_accessible(self):
            if current_user.is_Admin(user=current_user):
                return True
            else:
                return False

    admin = Admin(app)


    admin.add_view(AdminView(Admins, db.session))
    admin.add_view(AdminView(User, db.session))
    admin.add_view(AdminView(Job, db.session))
    admin.add_view(AdminView(Cv, db.session))
    admin.add_view(AdminView(Job_Category, db.session))

    return app
