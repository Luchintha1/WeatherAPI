from flask import Flask, render_template
import pandas as pd

app = Flask("Website")


@app.route("/")
def home():
    return render_template("home.html")

# here station and the date are parameters they can dynamically change.


@app.route("/api/v1/<station>/<date>")
def data(station, date):
    filepath = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filepath, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10

    return {"station": station,
            "date": date,
            "temperature": str(temperature)}


if __name__ == "__main__":
    app.run(debug=True)