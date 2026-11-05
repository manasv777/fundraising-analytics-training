import polars as pl
from statsmodels.tsa.statespace.sarimax import SARIMAX

from pathlib import Path


# Gets the folder containing the current script
SCRIPT_DIR = Path(__file__).parent

# Combines that folder path with your file name
csv_path = SCRIPT_DIR / "chestnut.csv"

print(csv_path)

df = pl.read_csv(csv_path, encoding="latin-1", columns=["Date", "Gift Amount"], try_parse_dates=True)


df = df.with_columns(
    pl.col("Date").str.to_date(format="%m/%d/%Y", strict=False)
)

df = df.with_columns(
    pl.col("Gift Amount").str.replace_all(r"[\$,]", "").str.replace_all(" ", "").cast(pl.Float64, strict=False))

df=df.sort("Date")

result = df.group_by_dynamic(index_column="Date",every="1mo").agg(pl.col("Gift Amount").sum().alias("monthly_avg"))
print(result)

y_series = result["monthly_avg"].to_numpy()

model = SARIMAX(
    y_series, 
    order=(1, 1, 1), 
    seasonal_order=(1, 1, 1, 12),
    enforce_stationarity=False,
    enforce_invertibility=False
)

results = model.fit()

# 4. Forecast the next 12 steps
forecast_steps = 12
forecast_array = results.forecast(steps=forecast_steps)

# 5. Bring the forecasts back into Polars for fast downstream processing
future_dates = pl.date_range(
    start=df["Date"].max() + pl.duration(days=1),  # Start right after the last date
    end=df["Date"].max() + pl.duration(days=365), 
    interval="1mo", 
    eager=True
)[:forecast_steps]

df_forecast = pl.DataFrame({
    "date": future_dates,
    "forecasted_value": forecast_array
})

print(df_forecast)
