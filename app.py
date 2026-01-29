import joblib
import numpy as np
from config.path_config import * 
from flask import Flask, request, render_template


app = Flask(__name__)

model = joblib.load(MODEL_DIR)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # match EXACT form field names from HTML
        lead_time = int(request.form["lead_time"])
        no_of_special_request = int(request.form["no_of_special_request"])
        avg_price_per_room = float(request.form["avg_price_per_room"])
        arrival_month = int(request.form["arrival_month"])
        arrival_date = int(request.form["arrival_day"])
        arrival_year = int(request.form["arrival_year"])
        no_of_adults = int(request.form["no_of_adults"])
        market_segment_type = int(request.form["market_segment_type"])
        no_of_week_nights = int(request.form["no_of_week_nights"])
        no_of_weekend_nights = int(request.form["no_of_weekend_nights"])
        type_of_meal_plan = int(request.form["type_of_meal_plan"])
        room_type_reserved = int(request.form["room_type_reserved"])

        # IMPORTANT: pass numeric values, in the same order your model was trained on
        input_query = np.array([[
            lead_time,
            no_of_special_request,
            avg_price_per_room,
            arrival_date,
            arrival_month,
            no_of_week_nights,
            market_segment_type,
            no_of_weekend_nights,
            arrival_year,
            no_of_adults
        ]])
        prediction = model.predict(input_query)[0]
        

        # Make this match your HTML template variable: prediction
        return render_template("index.html", prediction=prediction)

    except Exception as e:
        return render_template("index.html", prediction=f"Error: {e}")


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", prediction=None)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
