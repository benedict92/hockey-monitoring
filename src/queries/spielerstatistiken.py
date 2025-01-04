from bs4 import BeautifulSoup
import requests
import pandas as pd

# Liste der Berichte, die abgerufen werden sollen
reports = ["", "bio", "timeonice", "shots", "penaltyshots", "penalty"]

# Schleife über die Berichte
for report in reports:
    url = f"https://www.del-2.org/stats/scorer/?round=142&club=&report={report}"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find(
        "table",
        {"class": "table table-bordered table-sm table-striped table-hover small"},
    )

    header = [ele.text.strip() for ele in table.find_all("th")]
    df = pd.DataFrame(columns=header)
    df = df.rename(columns={"#": "Rank"})

    rows = table.find_all("tr")
    for row in rows[1:]:
        cols = row.find_all("td")
        cols = [ele.text.strip() for ele in cols]
        length = len(df)
        df.loc[length] = cols

    df = df.drop(columns=["Rank"])
    df["Abfragedatum"] = pd.Timestamp.now().strftime("%Y-%m-%d")

    # Save to CSV
    date_of_request = pd.Timestamp.now().strftime("%Y-%m-%d")
    filename = f"raw_spielerstatistiken_{report}_{date_of_request}.csv"
    p = r"C:/Users/BenedictAltgassenDat/OneDrive - DatenPioniere/Data Repositories/hockey-monitoring/hockey-monitoring/data/raw/"
    df.to_csv(p + filename, index=False)
