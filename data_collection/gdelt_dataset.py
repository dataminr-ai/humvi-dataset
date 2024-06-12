import gdelt
from typing import Union
import pandas as pd
from countrycode import countrycode


def get_gdelt_data(
    table: str, start_date: Union[pd.Timestamp, str], end_date: Union[pd.Timestamp, str]
) -> pd.DataFrame:
    """
    Collect gdelt data from `table` (events/mentions)
    ranging from `start_date` to `end_date`

    Returns a Pandas dataframe of GDelt data with added columns:
    `is_english`: True/False
    `countries_involved`: list of countries extracted from GDelt country codes
    """
    gd2 = gdelt.gdelt(version=2)
    df_english = gd2.Search(
        [str(pd.Timestamp(start_date)), str(pd.Timestamp(end_date))],
        table=table,
        coverage=True,
        translation=False,  # English only
    )
    df_english["is_english"] = True
    df_non_english = gd2.Search(
        [str(pd.Timestamp(start_date)), str(pd.Timestamp(end_date))],
        table=table,
        coverage=True,
        translation=True,  # non-English only
    )
    df_non_english["is_english"] = False

    df_combined = pd.concat([df_english, df_non_english])

    df_combined["countries_involved"] = df_combined.apply(
        lambda x: sorted(
            [
                x
                for x in set(
                    [
                        convert_country_code(x.Actor1CountryCode, "iso3c"),
                        convert_country_code(x.Actor2CountryCode, "iso3c"),
                        convert_country_code(x.Actor1Geo_CountryCode, "fips"),
                        convert_country_code(x.Actor2Geo_CountryCode, "fips"),
                        convert_country_code(x.ActionGeo_CountryCode, "fips"),
                    ]
                )
                if x is not None
            ]
        ),
        axis=1,
    )

    return df_combined


# https://www.suny.edu/media/suny/content-assets/documents/international-student/InternationalCountryCodes.pdf
# https://nief.org/attribute-registry/codesets/FIPS10-4CountryCode/
FIPS_LOOKUP = {
    "OD": "South Sudan",
    "GZ": "Palestinian Territories",
    "RN": "Saint Martin (French part)",
    "RB": "Serbia",
    "OS": "Oceans",
    # extrapolated from data:
    "OC": "Indian Ocean",
    "PG": "Peru",
    "PF": "Peru",
    "PJ": "Peru",
    "YI": "Serbia",
    "WQ": "United States Minor Outlying Islands (the)",
    "JQ": "United States Minor Outlying Islands (the)",
    "HQ": "United States Minor Outlying Islands (the)",
    "FQ": "United States Minor Outlying Islands (the)",
    "DQ": "United States Minor Outlying Islands (the)",
    "BQ": "United States Minor Outlying Islands (the)",
    "KQ": "United States Minor Outlying Islands (the)",
    "LQ": "United States Minor Outlying Islands (the)",
    "MQ": "United States Minor Outlying Islands (the)",
    "MQ": "United States Minor Outlying Islands (the)",
    "JN": "Norway",
    "IP": "Clipperton Island",
}

# https://github.com/carrillo/Gdelt/blob/master/resources/staticTables/CAMEO.country.txt
GDELT_CAMEO_LOOKUP = {
    "BAG": "Baghdad",
    "GZS": "Gaza Strip",
    "AFR": "Africa",
    "ASA": "Asia",
    "BLK": "Balkans",
    "CRB": "Caribbean",
    "CAU": "Caucasus",
    "CFR": "Central Africa",
    "CAS": "Central Asia",
    "CEU": "Central Europe",
    "EIN": "East Indies",
    "EAF": "Eastern Africa",
    "EEU": "Eastern Europe",
    "EUR": "Europe",
    "LAM": "Latin America",
    "MEA": "Middle East",
    "MDT": "Mediterranean",
    "NAF": "North Africa",
    "NMR": "North America",
    "PGS": "Persian Gulf",
    "SCN": "Scandinavia",
    "SAM": "South America",
    "SAS": "South Asia",
    "SEA": "Southeast Asia",
    "SAF": "Southern Africa",
    "WAF": "West Africa",
    "WST": "The West",
    "TMP": "East Timor",
    "ROM": "Romania",
}


def convert_country_code(cc, origin):
    country = None
    if cc is None or pd.isna(cc):
        return None
    elif origin == "fips":
        country = countrycode(cc, origin="fips")
        if country is None and cc in FIPS_LOOKUP:
            country = FIPS_LOOKUP[cc]

    elif origin == "iso3c":
        country = countrycode(cc, origin="iso3c")
        if country is None and cc in GDELT_CAMEO_LOOKUP:
            country = GDELT_CAMEO_LOOKUP[cc]

    if country is None:
        print(f"warn: country code {cc} not found in {origin}")

    return country
