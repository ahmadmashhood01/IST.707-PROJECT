import requests
import pandas as pd
import numpy as np
import time
from pathlib import Path


# ============================================================
# SETTINGS
# ============================================================

START_YEAR = 1960
END_YEAR = 2026

BASE_URL = "https://api.worldbank.org/v2"

SCRIPT_DIR = Path(__file__).resolve().parent

CSV_OUTPUT = SCRIPT_DIR / "wdi_selected_data_1960_2026.csv"
EXCEL_OUTPUT = SCRIPT_DIR / "wdi_selected_data_1960_2026.xlsx"
INDICATOR_REPORT = SCRIPT_DIR / "wdi_indicator_report.csv"

REQUEST_TIMEOUT = 120
MAX_RETRIES = 5


# ============================================================
# COUNTRIES
#
# Format:
# "Your desired country name": "World Bank / ISO3 code"
# ============================================================

COUNTRIES = {
    "Afghanistan": "AFG",
    "Albania": "ALB",
    "Algeria": "DZA",
    "Argentina": "ARG",
    "Armenia": "ARM",
    "Australia": "AUS",
    "Austria": "AUT",
    "Azerbaijan": "AZE",
    "Bahrain": "BHR",
    "Bahamas, The": "BHS",
    "Barbados": "BRB",
    "Belarus": "BLR",
    "Belgium": "BEL",
    "Bermuda": "BMU",
    "Botswana": "BWA",
    "Brazil": "BRA",
    "Bulgaria": "BGR",
    "Burkina Faso": "BFA",
    "Burundi": "BDI",
    "Cabo Verde": "CPV",
    "Cameroon": "CMR",
    "Canada": "CAN",
    "Chile": "CHL",
    "Colombia": "COL",
    "China": "CHN",
    "Costa Rica": "CRI",
    "Cote d'Ivoire": "CIV",
    "Croatia": "HRV",
    "Cuba": "CUB",
    "Cyprus": "CYP",
    "Czechia": "CZE",
    "Korea, Dem. People's Rep.": "PRK",
    "Denmark": "DNK",
    "Djibouti": "DJI",
    "Dominica": "DMA",
    "Dominican Republic": "DOM",
    "Ecuador": "ECU",
    "Egypt, Arab Rep.": "EGY",
    "Eritrea": "ERI",
    "Estonia": "EST",
    "Ethiopia": "ETH",
    "Fiji": "FJI",
    "Finland": "FIN",
    "France": "FRA",
    "Gabon": "GAB",
    "Georgia": "GEO",
    "Germany": "DEU",
    "Ghana": "GHA",
    "Greece": "GRC",
    "United Kingdom": "GBR",
    "Grenada": "GRD",
    "Guatemala": "GTM",
    "Guyana": "GUY",
    "Hong Kong SAR, China": "HKG",
    "Hungary": "HUN",
    "Iceland": "ISL",
    "India": "IND",
    "Indonesia": "IDN",
    "Iran, Islamic Rep.": "IRN",
    "Ireland": "IRL",
    "Iraq": "IRQ",
    "Israel": "ISR",
    "Italy": "ITA",
    "Jamaica": "JAM",
    "Japan": "JPN",
    "Jordan": "JOR",
    "Kazakhstan": "KAZ",
    "Kenya": "KEN",
    "Saudi Arabia": "SAU",
    "Kosovo": "XKX",
    "Kuwait": "KWT",
    "Kyrgyz Republic": "KGZ",
    "Latvia": "LVA",
    "Lebanon": "LBN",
    "Liechtenstein": "LIE",
    "Lithuania": "LTU",
    "Luxembourg": "LUX",
    "Malaysia": "MYS",
    "Mauritius": "MUS",
    "Mexico": "MEX",
    "Mongolia": "MNG",
    "Montenegro": "MNE",
    "Morocco": "MAR",
    "Mozambique": "MOZ",
    "Namibia": "NAM",
    "Netherlands": "NLD",
    "New Zealand": "NZL",
    "Niger": "NER",
    "Nigeria": "NGA",
    "North Macedonia": "MKD",
    "Norway": "NOR",
    "Pakistan": "PAK",
    "Panama": "PAN",
    "Paraguay": "PRY",
    "Peru": "PER",
    "Philippines": "PHL",
    "Poland": "POL",
    "Portugal": "PRT",
    "Puerto Rico (US)": "PRI",
    "Qatar": "QAT",
    "Korea, Rep.": "KOR",
    "Moldova": "MDA",
    "Russian Federation": "RUS",
    "Romania": "ROU",
    "Samoa": "WSM",
    "St. Lucia": "LCA",
    "San Marino": "SMR",
    "Senegal": "SEN",
    "Serbia": "SRB",
    "Singapore": "SGP",
    "Slovak Republic": "SVK",
    "Slovenia": "SVN",
    "South Africa": "ZAF",
    "Spain": "ESP",
    "Sri Lanka": "LKA",
    "Sudan": "SDN",
    "Suriname": "SUR",
    "Sweden": "SWE",
    "Switzerland": "CHE",
    "Syrian Arab Republic": "SYR",
    "Tajikistan": "TJK",
    "Thailand": "THA",
    "Togo": "TGO",
    "Trinidad and Tobago": "TTO",
    "Tonga": "TON",
    "Tunisia": "TUN",
    "Turkiye": "TUR",
    "Turkmenistan": "TKM",
    "Uganda": "UGA",
    "Ukraine": "UKR",
    "United Arab Emirates": "ARE",
    "Tanzania": "TZA",
    "United States": "USA",
    "Virgin Islands (U.S.)": "VIR",
    "Uruguay": "URY",
    "Uzbekistan": "UZB",
    "Venezuela, RB": "VEN",
    "Viet Nam": "VNM",
    "Zambia": "ZMB",
    "Zimbabwe": "ZWE",
}


# ============================================================
# WDI INDICATORS
#
# Format:
# "Desired final column name": "World Bank indicator code"
# ============================================================

INDICATORS = {

    # --------------------------------------------------------
    # CAPITAL / INVESTMENT
    # --------------------------------------------------------

    "Gross capital formation (% of GDP)":
        "NE.GDI.TOTL.ZS",

    "Gross fixed capital formation (% of GDP)":
        "NE.GDI.FTOT.ZS",

    # --------------------------------------------------------
    # POVERTY
    # --------------------------------------------------------

    "Multidimensional poverty headcount ratio (World Bank) (% of population)":
        "SI.POV.MPWB",

    # --------------------------------------------------------
    # LABOR FORCE
    # --------------------------------------------------------

    "Labor force participation rate, male (% of male population ages 15+) (modeled ILO estimate)":
        "SL.TLF.CACT.MA.ZS",

    "Labor force participation rate, female (% of female population ages 15+) (modeled ILO estimate)":
        "SL.TLF.CACT.FE.ZS",

    # --------------------------------------------------------
    # INCOME / GDP
    # --------------------------------------------------------

    "GNI per capita (constant 2015 US$)":
        "NY.GNP.PCAP.KD",

    "Price level index (GDP)":
        "PA.NUS.PPPC.RF",

    "Inflation, consumer prices (annual %)":
        "FP.CPI.TOTL.ZG",

    "Inflation, GDP deflator (annual %)":
        "NY.GDP.DEFL.KD.ZG",

    # --------------------------------------------------------
    # TRADE
    # --------------------------------------------------------

    "Imports of goods and services (% of GDP)":
        "NE.IMP.GNFS.ZS",

    "Exports of goods and services (% of GDP)":
        "NE.EXP.GNFS.ZS",

    "Official exchange rate (LCU per US$, period average)":
        "PA.NUS.FCRF",

    # --------------------------------------------------------
    # GDP
    # --------------------------------------------------------

    "GDP growth (annual %)":
        "NY.GDP.MKTP.KD.ZG",

    "GDP per capita (current US$)":
        "NY.GDP.PCAP.CD",

    "GDP (current US$)":
        "NY.GDP.MKTP.CD",

    # --------------------------------------------------------
    # DISASTERS / WEATHER
    # --------------------------------------------------------

    "Droughts, floods, extreme temperatures (% of population, average 1990-2009)":
        "EN.CLC.MDAT.ZS",

    # --------------------------------------------------------
    # GOVERNMENT
    # --------------------------------------------------------

    "General government final consumption expenditure (% of GDP)":
        "NE.CON.GOVT.ZS",

    # --------------------------------------------------------
    # URBANIZATION
    # --------------------------------------------------------

    "Urban population (% of total population)":
        "SP.URB.TOTL.IN.ZS",

    # --------------------------------------------------------
    # FINANCE
    # --------------------------------------------------------

    "Domestic credit to private sector (% of GDP)":
        "FS.AST.PRVT.GD.ZS",

    "Account ownership at a financial institution or with a mobile-money-service provider (% of population ages 15+)":
        "FX.OWN.TOTL.ZS",

    # --------------------------------------------------------
    # FOREIGN DIRECT INVESTMENT
    # --------------------------------------------------------

    "Foreign direct investment, net inflows (% of GDP)":
        "BX.KLT.DINV.WD.GD.ZS",

    "Foreign direct investment, net outflows (% of GDP)":
        "BM.KLT.DINV.WD.GD.ZS",

    # --------------------------------------------------------
    # CRIME / GOVERNANCE
    # --------------------------------------------------------

    "Intentional homicides (per 100,000 people)":
        "VC.IHR.PSRC.P5",

    # WGI indicator: approximately -2.5 to +2.5
    "Control of Corruption - Governance estimate (approx. -2.5 to +2.5)":
        "CC.EST",

    # WGI percentile rank: 0-100
    "Control of Corruption - Governance score (0-100)":
        "CC.PER.RNK",

    "CPIA transparency, accountability, and corruption in the public sector rating (1=low to 6=high)":
        "IQ.CPA.TRAN.XQ",

    # --------------------------------------------------------
    # EDUCATION
    # --------------------------------------------------------

    "School enrollment, secondary (% gross)":
        "SE.SEC.ENRR",

    "School enrollment, primary (% gross)":
        "SE.PRM.ENRR",

    "School enrollment, tertiary (% gross)":
        "SE.TER.ENRR",

    "Government expenditure on education, total (% of GDP)":
        "SE.XPD.TOTL.GD.ZS",

    "Educational attainment, at least completed upper secondary, population 25+, total (%) (cumulative)":
        "SE.SEC.CUAT.UP.ZS",

    # --------------------------------------------------------
    # HEALTH
    # --------------------------------------------------------

    "Current health expenditure (% of GDP)":
        "SH.XPD.CHEX.GD.ZS",

    # --------------------------------------------------------
    # INEQUALITY
    # --------------------------------------------------------

    "Gini index":
        "SI.POV.GINI",

    # --------------------------------------------------------
    # CHILD LABOR
    # --------------------------------------------------------

    "Children in employment, total (% of children ages 7-14)":
        "SL.TLF.0714.ZS",

    # --------------------------------------------------------
    # EMPLOYMENT
    # --------------------------------------------------------

    "Employment to population ratio, 15+, total (%) (modeled ILO estimate)":
        "SL.EMP.TOTL.SP.ZS",

    # --------------------------------------------------------
    # AGRICULTURE
    # --------------------------------------------------------

    "Agriculture, forestry, and fishing, value added (% of GDP)":
        "NV.AGR.TOTL.ZS",

    # --------------------------------------------------------
    # IMPORT / EXPORT INDEXES
    # --------------------------------------------------------

    "Import value index (2015 = 100)":
        "TM.VAL.MRCH.XD.WD",

    "Export value index (2015 = 100)":
        "TX.VAL.MRCH.XD.WD",

    # --------------------------------------------------------
    # POPULATION
    # --------------------------------------------------------

    "Population, total":
        "SP.POP.TOTL",

    "Population growth (annual %)":
        "SP.POP.GROW",

    "Population density (people per sq. km of land area)":
        "EN.POP.DNST",

    # --------------------------------------------------------
    # LIFE EXPECTANCY
    # --------------------------------------------------------

    "Life expectancy at birth, total (years)":
        "SP.DYN.LE00.IN",

    # --------------------------------------------------------
    # DEBT
    # --------------------------------------------------------

    "Central government debt, total (% of GDP)":
        "GC.DOD.TOTL.GD.ZS",

    # --------------------------------------------------------
    # RESEARCH / TECHNOLOGY
    # --------------------------------------------------------

    "Research and development expenditure (% of GDP)":
        "GB.XPD.RSDV.GD.ZS",

    "Individuals using the Internet (% of population)":
        "IT.NET.USER.ZS",

    # --------------------------------------------------------
    # TAXES
    # --------------------------------------------------------

    "Tax revenue (% of GDP)":
        "GC.TAX.TOTL.GD.ZS",

    # --------------------------------------------------------
    # CPIA
    # --------------------------------------------------------

    "CPIA trade rating (1=low to 6=high)":
        "IQ.CPA.TRAD.XQ",

    "CPIA social protection rating (1=low to 6=high)":
        "IQ.CPA.PROT.XQ",

    "CPIA property rights and rule-based governance rating (1=low to 6=high)":
        "IQ.CPA.PROP.XQ",

    "CPIA policies for social inclusion/equity cluster average (1=low to 6=high)":
        "IQ.CPA.SOCI.XQ",

    "CPIA gender equality rating (1=low to 6=high)":
        "IQ.CPA.GNDR.XQ",

    "CPIA business regulatory environment rating (1=low to 6=high)":
        "IQ.CPA.BREG.XQ",

    # --------------------------------------------------------
    # WATER
    # --------------------------------------------------------

    "People using at least basic drinking water services (% of population)":
        "SH.H2O.BASW.ZS",

    # --------------------------------------------------------
    # FOOD SECURITY
    # --------------------------------------------------------

    "Prevalence of severe food insecurity in the population (%)":
        "SN.ITK.SVFI.ZS",

    # --------------------------------------------------------
    # CHILD MORTALITY / FERTILITY
    # --------------------------------------------------------

    "Mortality rate, under-5 (per 1,000 live births)":
        "SH.DYN.MORT",

    "Fertility rate, total (births per woman)":
        "SP.DYN.TFRT.IN",

    # --------------------------------------------------------
    # MORE CPIA
    # --------------------------------------------------------

    "CPIA equity of public resource use rating (1=low to 6=high)":
        "IQ.CPA.PRES.XQ",

    "CPIA building human resources rating (1=low to 6=high)":
        "IQ.CPA.HRES.XQ",

    # --------------------------------------------------------
    # TOURISM
    # --------------------------------------------------------

    "International tourism, receipts (% of total exports)":
        "ST.INT.RCPT.XP.ZS",

    "International tourism, number of arrivals":
        "ST.INT.ARVL",

    # --------------------------------------------------------
    # MILITARY
    # --------------------------------------------------------

    "Military expenditure (% of GDP)":
        "MS.MIL.XPND.GD.ZS",

    # --------------------------------------------------------
    # ELECTRICITY
    # --------------------------------------------------------

    "Access to electricity (% of population)":
        "EG.ELC.ACCS.ZS",
}


# ============================================================
# HTTP SESSION
# ============================================================

session = requests.Session()

session.headers.update({
    "User-Agent": "WDI-Python-Downloader/1.0"
})


# ============================================================
# REQUEST FUNCTION WITH RETRIES
# ============================================================

def request_json(url, params=None):
    """
    Makes a World Bank API request with retry handling.
    """

    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):

        try:

            response = session.get(
                url,
                params=params,
                timeout=REQUEST_TIMEOUT
            )

            response.raise_for_status()

            return response.json()

        except (
            requests.exceptions.RequestException,
            ValueError
        ) as exc:

            last_error = exc

            print(
                f"Request failed "
                f"(attempt {attempt}/{MAX_RETRIES}): {exc}"
            )

            if attempt < MAX_RETRIES:
                wait_seconds = attempt * 2

                print(
                    f"Retrying in {wait_seconds} seconds..."
                )

                time.sleep(wait_seconds)

    raise RuntimeError(
        f"Request failed after {MAX_RETRIES} attempts."
    ) from last_error


# ============================================================
# VALIDATE INDICATOR
# ============================================================

def validate_indicator(indicator_code):
    """
    Retrieves World Bank metadata for an indicator code.

    Returns:
        dictionary containing indicator metadata
        or None if not found.
    """

    url = f"{BASE_URL}/indicator/{indicator_code}"

    params = {
        "format": "json",
        "per_page": 100
    }

    try:

        data = request_json(url, params=params)

        if (
            not isinstance(data, list)
            or len(data) < 2
            or data[1] is None
            or len(data[1]) == 0
        ):
            return None

        # Sometimes the same indicator may be listed under
        # more than one World Bank source.
        results = data[1]

        # Prefer World Development Indicators (source ID 2)
        for result in results:

            source = result.get("source", {})

            if str(source.get("id")) == "2":
                return result

        # Otherwise use the first available source.
        return results[0]

    except Exception as exc:

        print(
            f"Could not validate {indicator_code}: {exc}"
        )

        return None


# ============================================================
# DOWNLOAD ONE INDICATOR
# ============================================================

def download_indicator(
    indicator_name,
    indicator_code,
    allowed_country_codes
):
    """
    Downloads all available World Bank observations
    between START_YEAR and END_YEAR for one indicator.

    We download all economies for the indicator and filter
    to the user's selected countries afterward.

    Pagination is handled automatically.
    """

    url = (
        f"{BASE_URL}/country/all/"
        f"indicator/{indicator_code}"
    )

    params = {
        "format": "json",
        "date": f"{START_YEAR}:{END_YEAR}",
        "per_page": 20000,
        "page": 1
    }

    records = []

    while True:

        params["page"] = params.get("page", 1)

        data = request_json(
            url,
            params=params
        )

        if (
            not isinstance(data, list)
            or len(data) < 2
            or data[1] is None
        ):
            break

        metadata = data[0]

        observations = data[1]

        for obs in observations:

            country_code = obs.get("countryiso3code")

            if country_code not in allowed_country_codes:
                continue

            year_value = obs.get("date")

            try:
                year_value = int(year_value)
            except (TypeError, ValueError):
                continue

            if not START_YEAR <= year_value <= END_YEAR:
                continue

            value = obs.get("value")

            records.append({
                "Country Code": country_code,
                "Year": year_value,
                "Indicator": indicator_name,
                "Indicator Code": indicator_code,
                "Value": value
            })

        current_page = int(
            metadata.get("page", 1)
        )

        total_pages = int(
            metadata.get("pages", 1)
        )

        if current_page >= total_pages:
            break

        params["page"] = current_page + 1

    return records


# ============================================================
# CREATE COMPLETE COUNTRY-YEAR PANEL
# ============================================================

def create_country_year_panel():
    """
    Creates every requested Country x Year combination,
    even when WDI has no data.

    This ensures that missing observations remain NaN
    instead of causing entire rows to disappear.
    """

    rows = []

    for country_name, country_code in COUNTRIES.items():

        for year in range(
            START_YEAR,
            END_YEAR + 1
        ):

            rows.append({
                "Country": country_name,
                "Country Code": country_code,
                "Year": year
            })

    return pd.DataFrame(rows)


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("WORLD DEVELOPMENT INDICATORS DOWNLOAD")
    print("=" * 70)

    print(
        f"\nYears: {START_YEAR}-{END_YEAR}"
    )

    print(
        f"Countries: {len(COUNTRIES)}"
    )

    print(
        f"Indicators: {len(INDICATORS)}"
    )

    print()

    # --------------------------------------------------------
    # COUNTRY CODE SET
    # --------------------------------------------------------

    allowed_country_codes = set(
        COUNTRIES.values()
    )

    # --------------------------------------------------------
    # VALIDATE INDICATORS
    # --------------------------------------------------------

    print("Validating indicator codes...\n")

    indicator_report = []

    valid_indicators = {}

    for number, (
        requested_name,
        indicator_code
    ) in enumerate(
        INDICATORS.items(),
        start=1
    ):

        print(
            f"[{number}/{len(INDICATORS)}] "
            f"{indicator_code}"
        )

        metadata = validate_indicator(
            indicator_code
        )

        if metadata is None:

            print(
                f"    WARNING: "
                f"{indicator_code} was not found."
            )

            indicator_report.append({
                "Requested Column": requested_name,
                "Indicator Code": indicator_code,
                "World Bank Name": "",
                "Source ID": "",
                "Source": "",
                "Status": "NOT FOUND"
            })

            continue

        wb_name = metadata.get(
            "name",
            ""
        )

        source = metadata.get(
            "source",
            {}
        )

        source_id = source.get(
            "id",
            ""
        )

        source_name = source.get(
            "value",
            ""
        )

        print(
            f"    World Bank: {wb_name}"
        )

        print(
            f"    Source: {source_name}"
        )

        valid_indicators[
            requested_name
        ] = indicator_code

        indicator_report.append({
            "Requested Column": requested_name,
            "Indicator Code": indicator_code,
            "World Bank Name": wb_name,
            "Source ID": source_id,
            "Source": source_name,
            "Status": "OK"
        })

    indicator_report_df = pd.DataFrame(
        indicator_report
    )

    indicator_report_df.to_csv(
        INDICATOR_REPORT,
        index=False
    )

    print()
    print(
        f"Indicator report saved to:"
        f"\n{INDICATOR_REPORT}"
    )

    print()
    print(
        f"Valid indicators: "
        f"{len(valid_indicators)} / "
        f"{len(INDICATORS)}"
    )

    if len(valid_indicators) == 0:

        raise RuntimeError(
            "No valid indicators were found."
        )

    # --------------------------------------------------------
    # DOWNLOAD DATA
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("DOWNLOADING DATA")
    print("=" * 70 + "\n")

    all_records = []

    for number, (
        indicator_name,
        indicator_code
    ) in enumerate(
        valid_indicators.items(),
        start=1
    ):

        print(
            f"[{number}/{len(valid_indicators)}] "
            f"{indicator_name}"
        )

        print(
            f"    Code: {indicator_code}"
        )

        try:

            records = download_indicator(
                indicator_name,
                indicator_code,
                allowed_country_codes
            )

            all_records.extend(records)

            non_null_count = sum(
                record["Value"] is not None
                for record in records
            )

            print(
                f"    Rows returned: "
                f"{len(records):,}"
            )

            print(
                f"    Non-null values: "
                f"{non_null_count:,}"
            )

        except Exception as exc:

            print(
                f"    ERROR downloading "
                f"{indicator_code}: {exc}"
            )

        # Small delay to be polite to the API.
        time.sleep(0.10)

    # --------------------------------------------------------
    # CREATE COMPLETE PANEL
    # --------------------------------------------------------

    print("\nCreating complete country-year panel...")

    panel = create_country_year_panel()

    print(
        f"Country-year rows: "
        f"{len(panel):,}"
    )

    # --------------------------------------------------------
    # CONVERT DOWNLOADED DATA TO WIDE FORMAT
    # --------------------------------------------------------

    if all_records:

        long_df = pd.DataFrame(
            all_records
        )

        # Remove accidental duplicates if the API
        # returns duplicate country/year observations.
        long_df = (
            long_df
            .sort_values(
                [
                    "Country Code",
                    "Year",
                    "Indicator"
                ]
            )
            .drop_duplicates(
                subset=[
                    "Country Code",
                    "Year",
                    "Indicator"
                ],
                keep="first"
            )
        )

        wide_df = (
            long_df
            .pivot(
                index=[
                    "Country Code",
                    "Year"
                ],
                columns="Indicator",
                values="Value"
            )
            .reset_index()
        )

        # Remove pandas columns name created by pivot.
        wide_df.columns.name = None

        # Join onto COMPLETE country-year grid.
        final_df = panel.merge(
            wide_df,
            on=[
                "Country Code",
                "Year"
            ],
            how="left"
        )

    else:

        print(
            "WARNING: No observations were downloaded."
        )

        final_df = panel.copy()

    # --------------------------------------------------------
    # MAKE SURE EVERY REQUESTED INDICATOR COLUMN EXISTS
    # --------------------------------------------------------

    for indicator_name in INDICATORS.keys():

        if indicator_name not in final_df.columns:

            final_df[
                indicator_name
            ] = np.nan

    # --------------------------------------------------------
    # CREATE ID
    #
    # Examples:
    # Afghanistan 1960 -> AFG60
    # Afghanistan 2020 -> AFG20
    # United States 2020 -> USA20
    # --------------------------------------------------------

    final_df["ID"] = (
        final_df["Country Code"].astype(str)
        +
        final_df["Year"]
        .astype(str)
        .str[-2:]
    )

    # --------------------------------------------------------
    # COLUMN ORDER
    # --------------------------------------------------------

    desired_columns = [
        "ID",
        "Country",
        "Country Code",
        "Year"
    ] + list(INDICATORS.keys())

    final_df = final_df[
        desired_columns
    ]

    # --------------------------------------------------------
    # SORT
    #
    # Uses order of countries in the original country list.
    # --------------------------------------------------------

    country_order = {
        code: position
        for position, code in enumerate(
            COUNTRIES.values()
        )
    }

    final_df["_country_order"] = (
        final_df["Country Code"]
        .map(country_order)
    )

    final_df = (
        final_df
        .sort_values(
            [
                "_country_order",
                "Year"
            ]
        )
        .drop(
            columns="_country_order"
        )
        .reset_index(drop=True)
    )

    # --------------------------------------------------------
    # DATA COVERAGE REPORT
    # --------------------------------------------------------

    coverage_rows = []

    total_possible = len(final_df)

    for indicator_name in INDICATORS.keys():

        count = (
            final_df[indicator_name]
            .notna()
            .sum()
        )

        percent = (
            count / total_possible * 100
            if total_possible
            else 0
        )

        coverage_rows.append({
            "Indicator": indicator_name,
            "Indicator Code":
                INDICATORS[indicator_name],
            "Non-Missing Observations":
                count,
            "Total Country-Year Rows":
                total_possible,
            "Coverage Percent":
                round(percent, 2)
        })

    coverage_df = pd.DataFrame(
        coverage_rows
    )

    # --------------------------------------------------------
    # EXPORT CSV
    # --------------------------------------------------------

    print("\nSaving CSV...")

    final_df.to_csv(
        CSV_OUTPUT,
        index=False
    )

    # --------------------------------------------------------
    # EXPORT EXCEL
    # --------------------------------------------------------

    print("Saving Excel...")

    with pd.ExcelWriter(
        EXCEL_OUTPUT,
        engine="openpyxl"
    ) as writer:

        final_df.to_excel(
            writer,
            sheet_name="WDI Data",
            index=False
        )

        indicator_report_df.to_excel(
            writer,
            sheet_name="Indicator Report",
            index=False
        )

        coverage_df.to_excel(
            writer,
            sheet_name="Coverage",
            index=False
        )

    # --------------------------------------------------------
    # FINAL INFORMATION
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("COMPLETE")
    print("=" * 70)

    print(
        f"\nCountries: "
        f"{final_df['Country Code'].nunique():,}"
    )

    print(
        f"Years: "
        f"{final_df['Year'].min()}-"
        f"{final_df['Year'].max()}"
    )

    print(
        f"Country-year rows: "
        f"{len(final_df):,}"
    )

    print(
        f"Requested indicators: "
        f"{len(INDICATORS)}"
    )

    print(
        f"Valid indicators: "
        f"{len(valid_indicators)}"
    )

    print(
        f"\nCSV:"
        f"\n{CSV_OUTPUT}"
    )

    print(
        f"\nExcel:"
        f"\n{EXCEL_OUTPUT}"
    )

    print(
        f"\nIndicator report:"
        f"\n{INDICATOR_REPORT}"
    )

    # --------------------------------------------------------
    # DISPLAY FIRST FEW ROWS
    # --------------------------------------------------------

    print("\nFirst 10 rows:\n")

    print(
        final_df[
            [
                "ID",
                "Country",
                "Country Code",
                "Year"
            ]
        ].head(10)
    )

    # --------------------------------------------------------
    # DISPLAY LOW-COVERAGE VARIABLES
    # --------------------------------------------------------

    print(
        "\nLowest coverage indicators:\n"
    )

    print(
        coverage_df
        .sort_values(
            "Coverage Percent"
        )
        .head(15)
        .to_string(index=False)
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()