import requests
import pandas as pd

df = pd.read_csv("coordinates.csv")
df = df.dropna(subset=["Lat", "Long"])

start_date = "2026-09-24"
end_date = "2026-10-07"
results = []

for index, row in df.iterrows():
    lat = row["Lat"]
    long = row["Long"]

    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={long}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_mean,temperature_2m_max,temperature_2m_min,precipitation_sum&temperature_unit=fahrenheit&precipitation_unit=inch&timezone=America/New_York"

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    daily = data["daily"]

    for i in range(len(daily["time"])):
        avg_temp = daily["temperature_2m_mean"][i]

        results.append({
            "Area": row["Area"],
            "Sample": row["Sample"],
            "Date": daily["time"][i],
            "Coordinate": row["Coordinate"],
            "Lat": lat,
            "Long": long,
            "Avg_Temp": avg_temp,
            "Max_Temp": daily["temperature_2m_max"][i],
            "Min_Temp": daily["temperature_2m_min"][i],
            "HDD": round(max(0, 65 - avg_temp), 1),
            "CDD": round(max(0, avg_temp - 65), 1),
            "Precipitation": daily["precipitation_sum"][i]
        })

result_df = pd.DataFrame(results)

result_df.to_csv("result.csv", index=False)
