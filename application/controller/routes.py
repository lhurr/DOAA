from flask import Blueprint, render_template, abort, redirect, flash, request, session, url_for
from flask_login.utils import login_required, current_user, login_user,logout_user
from werkzeug.exceptions import BadRequest
from werkzeug.security import generate_password_hash, check_password_hash
from .. import APP_TITLE
from ..forms import LoginForm, RegisterForm, PredictionForm
from ..model.user import User, add_new_user
from ..model.pred_history import PredictionHistory
import datetime,json

routes = Blueprint("routes", __name__)

@routes.route('/')
@routes.route('/index')
@routes.route('/home')
def index():
    return render_template('index.html', title=APP_TITLE, page='home')
# Home page


# Login
@routes.route('/login', methods= ['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                email = form.email.data
                password = form.password.data
                user = User.query.filter_by(email=email).all()
                print(user)
                if len(user) == 0:
                    flash("The email you entered does not exist!", "danger")
                    abort(400)
                if not check_password_hash(user[0].password, password):
                    flash("Password is incorrect!", "danger")
                    abort(400)
                login_user(user=user[0], remember=True)
                return redirect(url_for('routes.index'))
        except:
            flash(f"Unable to login", "danger")
    return render_template('login.html', title=APP_TITLE, page='login', form=form)

# Sign up
@routes.route('/signup', methods=['GET', 'POST'] )
def signup():
    register_form = RegisterForm()
    if request.method == 'POST':
        if register_form.validate_on_submit():
            try:
                email = register_form.email.data
                password_hash = generate_password_hash(register_form.password.data)
                new_user = User(email = email, password=password_hash, created_time = datetime.datetime.utcnow())
                # Add user to database and login the user
                add_new_user(new_user)
                login_user(user=new_user)
                flash('Account registered! You may login','success')
                return redirect(url_for("routes.prediction"))
            except BadRequest:
                flash('Failed to register account', 'danger')
    return render_template('signup.html', title = APP_TITLE, page = 'signup', form=register_form)



# HISTORY PAGE
def get_all_predictions(user_ID):
    try:
        return PredictionHistory.query.filter_by(user_ID=user_ID).order_by(PredictionHistory.id.asc())
    except Exception as e:
        flash(str(e), 'error')


@routes.route('/history', methods=['GET'])
@login_required
def history():
    past_predictions = get_all_predictions(current_user.id)
    # price_preds = [round(r.prediction,2) for r in past_predictions]
    # try:
    #     if len(price_preds) >=1:
    #         fig = px.bar(y=price_preds, x=[str(x+1) for x in range(len(price_preds))], barmode='group', title="Past predictions")
    #         fig.update_layout(xaxis_title="Number of Predictions",yaxis_title="Price")
    #         graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    #         return render_template('history.html', title=APP_TITLE,page='history', past_pred = past_predictions, graphJSON=graphJSON)
    # except Exception as e:
    #     print(e)
    return render_template('history.html', title=APP_TITLE,page='history', past_pred = past_predictions)


# LOGOUT
@routes.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    flash("Logged Out", "info")
    return redirect(url_for("routes.login"))

# Prediction page
@routes.route("/predict", methods= ["GET"])
@login_required
def predict():
    predict_form = PredictionForm()
    return render_template('predict.html', title=APP_TITLE, page='predict', form = predict_form)