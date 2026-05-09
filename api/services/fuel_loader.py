import os

import pandas as pd
from django.conf import settings


class FuelDataService:
    _instance = None
    _df = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_fuel_data(self):
        if self._df is None:
            csv_path = os.path.join(
                settings.BASE_DIR, "fuel_data", "fuel-prices-for-be-assessment.csv"
            )
            fuel_df = pd.read_csv(csv_path)
            fuel_df["City"] = fuel_df["City"].astype(str).str.upper().str.strip()
            fuel_df["State"] = fuel_df["State"].astype(str).str.upper().str.strip()
            fuel_df["Retail Price"] = pd.to_numeric(
                fuel_df["Retail Price"], errors="coerce"
            )
            fuel_df = fuel_df.dropna(subset=["Retail Price"])

            cities_url = (
                "https://raw.githubusercontent.com/kelvins/US-Cities-Database/master/csv/us_cities.csv"
            )
            cities_df = pd.read_csv(cities_url)
            cities_df["CITY"] = cities_df["CITY"].astype(str).str.upper().str.strip()
            cities_df["STATE_CODE"] = cities_df["STATE_CODE"].astype(str).str.upper().str.strip()
            
            merged = pd.merge(
                fuel_df,
                cities_df[["CITY", "STATE_CODE", "LATITUDE", "LONGITUDE"]],
                left_on=["City", "State"],
                right_on=["CITY", "STATE_CODE"],
                how="inner",
            )
            self._df = merged.drop(columns=["CITY", "STATE_CODE"], errors="ignore")
            # Rename for consistency if needed, but the optimizer expects 'latitude'/'longitude' lowercase
            self._df = self._df.rename(columns={"LATITUDE": "latitude", "LONGITUDE": "longitude"})

        return self._df


fuel_service = FuelDataService()
