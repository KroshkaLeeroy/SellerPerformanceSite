from setup import app, db, User
from login.login_views import login_blueprint
from main.main_views import main_blueprint
from profile.profile_views import profile_blueprint
from login.reset_password_views import reset_blueprint
from feedback.feedback_views import feedback_blueprint
from admin_panel.admin_views import admin_blueprint



app.register_blueprint(main_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(profile_blueprint)
app.register_blueprint(feedback_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(reset_blueprint)
