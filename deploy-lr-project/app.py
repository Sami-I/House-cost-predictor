from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import ValidationError, DataRequired, NumberRange
import pickle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'
model = pickle.load(open('model.pkl', 'rb'))  # Load the model


class LRForm(FlaskForm):
    rooms = IntegerField('Rooms', validators=[DataRequired(), NumberRange(min=1, message='You must enter a positive whole number')])
    distance = IntegerField('Distance', validators=[DataRequired(), NumberRange(min=1, message='You must enter a positive whole number')])
    submit = SubmitField(label=('Submit'))


@app.route("/", methods=['GET', 'POST'])  # Decorator
def hello():
    prediction_text = ''
    form = LRForm()
    data = {'form': form, 'prediction_text': prediction_text}
    return render_template('index.html', data=data)  # Helps us render some html on the front-end


@app.route("/predict", methods=['GET', 'POST'])  # Predict section of web app
def predict():
    form = LRForm()
    # Get html input values from user
    if form.validate_on_submit:
        rooms = int(request.form['rooms'])
        distance = int(request.form['distance'])
        prediction = model.predict([[rooms, distance]])  # Use model to calculate the prediction
        result = round(prediction[0], 2)
        prediction_text = f'A house with {rooms} rooms and located {distance} km to employment centers has an estimated value of ${result}K'
        data = {'form': form, 'prediction_text': prediction_text}
        return render_template('index.html', data=data)



if __name__ == "__main__":
    app.run(debug=True)

