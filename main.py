from flask import Flask, render_template
import pandas as pd

app = Flask("Website")

stations = pd.read_csv("data_small/stations.txt", skiprows=17)
stations = stations[["STAID", "STANAME                                 "]]


@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())

# here station and the date are parameters they can dynamically change.


@app.route("/api/v1/<station>/<date>")
def data(station, date):
    filepath = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filepath, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10

    return {"station": station,
            "date": date,
            "temperature": str(temperature)}


@app.route("/api/v1/<station>")
def station_data(station):
    filepath = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filepath, skiprows=20, parse_dates=["    DATE"])
    results = df.to_dict(orient="records")

    return results


@app.route("/api/v1/annual/<station>/<year>")
def annual_data(station, year):
    filepath = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filepath, skiprows=20)
    df["    DATE"] = df["    DATE"].astype(str)
    results = df[df["    DATE"].str.startswith(str(year))].to_dict(orient='records')

    return results


if __name__ == "__main__":
    app.run(debug=True)