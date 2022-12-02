from .. import APP_TITLE, MODEL, INTRAPOLATION, db
from ..forms import PredictionForm
from ..model.pred_history import PredictionHistory, add_entry, delete_entry
from ..model.user import User,add_new_user

from flask import Blueprint, render_template, abort, redirect, flash, request, json,jsonify, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login.utils import login_required, current_user
import datetime
import pandas as pd
import numpy as np


api = Blueprint("api", __name__)

def get_pred(age, height, weight, diabetes, bloodpressure, anytransplant, chronic, allergies, cancer,surgery, bmi):
    X = pd.DataFrame(data = np.array([
            [age,
             height,
             weight,diabetes, bloodpressure, 
             anytransplant, chronic, allergies, 
             cancer,surgery, bmi]]),
        columns=['Age', 'Height', 'Weight', 'Diabetes', 
        'BloodPressureProblems', 'AnyTransplants', 'AnyChronicDiseases', 'KnownAllergies', 'HistoryOfCancerInFamily',
        'NumberOfMajorSurgeries', 'BMI']
    )
    return max(MODEL.predict(X)[0], INTRAPOLATION['price_min'])




# Prediction
@api.route('/predict', methods=['POST'] )
@login_required
def prediction():
    form = PredictionForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            age = form.age.data
            height = form.height.data
            weight = form.weight.data
            diabetes = int(form.diabetes.data)
            bloodpressure = int(form.bloodpressure.data)
            anytransplant = int(form.anytransplant.data)
            chronic = int(form.chronic.data)
            allergies = int(form.allergies.data)
            cancer = int(form.cancer.data)
            surgery = int(form.surgery.data)
            bmi = weight/ ((height/100 ) ** 2)

            created_time = datetime.datetime.utcnow()

            ml_pred = get_pred(age,height,weight,diabetes, bloodpressure, anytransplant, chronic, allergies, cancer,surgery, bmi)

            ml_pred = ml_pred*0.017
            # change from IDR to SGD
            try:
                hist = PredictionHistory(user_ID = int(current_user.id) ,age=age,height=height,
                weight=weight,diabetes=diabetes, bloodpressure=bloodpressure, 
                anytransplant=anytransplant, chronic=chronic, allergy=allergies, 
                cancer=cancer,surgery=surgery,bmi=bmi, prediction=float(ml_pred), created_time=created_time)
                add_entry(hist)
            except Exception as e:
                print(e)
            
            flash(f'Prediction Successful ${round(ml_pred,2)}', 'success')
        else:
            flash("Validation error, please try again!", "danger")
    return render_template('predict.html', title = APP_TITLE, page = 'predict', form=form)




@api.route('/delete_pred', methods=['POST'] )
@login_required
def delete_pred():
    id = request.form['id']
    result = PredictionHistory.query.filter_by(id=id, user_ID=current_user.id).first()
    if result is None:
        flash(f"Entry can't be found", 'danger')
    delete_entry(result)

    return redirect(url_for('routes.history'))




#  ======================================== API ============================================

# DELETE API
@api.route('/api/delete/<pred_id>', methods=['DELETE'])
@login_required
def remove_prediction_api(pred_id):
    try:
        record = PredictionHistory.query.get(id = int(pred_id))
        db.session.delete(record)
        db.session.commit()
        return jsonify({'result': 'ok'})
    except Exception as error:
        db.session.rollback()
        return jsonify({'result': 'fail'})


@api.route('/api/login', methods=['POST'])
def get_user():
    try:
        data = request.get_json()
        if type(data) is str:
            data = json.loads(data)
        email = data['email']   
        # password = data['password']
        record = User.query.filter_by(email =email).first()
        return jsonify({'result': record.id})
    except Exception as error:
        return jsonify({'result':'Error!'})



# ADD USER
@api.route('/api/user/add', methods=['POST'])
def add_new_user_api():
    try:
        data = request.get_json()
        if type(data) is str:
            data = json.loads(data)
        email = data['email']   
        pw = data['password']
        password = generate_password_hash(pw) 
        new_user = User(email=email, password=password, created_time = datetime.datetime.utcnow())
        assert new_user.email == email
        assert check_password_hash(new_user.password,pw)
        user_id = add_new_user(new_user)
        
        return jsonify({'result': user_id})
    except Exception as e:
        print(e)
        return jsonify({'result': 'Error!'})

# PREDICTION
@api.route('/api/predict', methods=['POST'])
def new_prediction_api():
    data = request.get_json()
    if type(data) is str:
        data = json.loads(data)
    age = data['age']
    height = data['height']
    weight = data['weight']
    diabetes = int(data['diabetes'])
    bloodpressure = int(data['bloodpressure'])
    anytransplant = int(data['anytransplant'])
    chronic = int(data['chronic'])
    allergies = int(data['allergies'])
    cancer = int(data['cancer'])
    surgery = int(data['surgery'])
    bmi = weight/ ((height/100 ) ** 2)
    price = get_pred(age,height,weight,diabetes, bloodpressure, anytransplant, chronic, allergies, cancer,surgery, bmi)

    return jsonify({'prediction': round(price,2) * 0.017})



# STORE PREDICTION API
@api.route('/api/predict/add', methods=['POST'])
def store_prediction_api():
    data = request.get_json()
    # print('api data' , data)
    if type(data) is str:
        data = json.loads(data)
    age = data['age']
    height = data['height']
    weight = data['weight']
    diabetes = int(data['diabetes'])
    bloodpressure = int(data['bloodpressure'])
    anytransplant = int(data['anytransplant'])
    chronic = int(data['chronic'])
    allergies = int(data['allergies'])
    user_ID = int(data['user_ID'])
    cancer = int(data['cancer'])
    surgery = int(data['surgery'])
    bmi = weight/ ((height/100 ) ** 2)
    ml_pred = float(data['prediction'])

    try:
        pred_hist = PredictionHistory(user_ID = user_ID ,age=age,height=height,
                    weight=weight,diabetes=diabetes, bloodpressure=bloodpressure, 
                    anytransplant=anytransplant, chronic=chronic, allergy=allergies, 
                    cancer=cancer,surgery=surgery,bmi=bmi, prediction=float(ml_pred), created_time=datetime.datetime.utcnow())
        add_entry(pred_hist)
        return jsonify({'result': pred_hist.user_ID})
    except:

        return jsonify({'result': 'Error'})
    


