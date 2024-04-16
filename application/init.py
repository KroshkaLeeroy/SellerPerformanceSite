from application.setup import app, db, User
from application.login.login_views import login_blueprint
from application.main.main_views import main_blueprint
from application.profile.profile_views import profile_blueprint
from application.login.reset_password_views import reset_blueprint
from application.feedback.feedback_views import feedback_blueprint
from application.admin_panel.admin_views import admin_blueprint
from application.payment.payment_views import payment_blueprint

app.register_blueprint(main_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(profile_blueprint)
app.register_blueprint(feedback_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(reset_blueprint)
app.register_blueprint(payment_blueprint)
