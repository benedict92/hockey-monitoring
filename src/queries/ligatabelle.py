from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "https://www.del-2.org/tabelle/"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
print(soup)

table = soup.find("table", {"class": "table table-sm table-hover table-striped"})

header = [ele.text.strip() for ele in table.find_all("th")]
df = pd.DataFrame(columns=header)

rows = table.find_all("tr")
for row in rows[1:]:
    cols = row.find_all("td")
    cols = [ele.text.strip() for ele in cols]

    length = len(df)
    df.loc[length] = cols

df["Abfragedatum"] = pd.Timestamp.now().strftime("%Y-%m-%d")

# Save to CSV
date_of_request = pd.Timestamp.now().strftime("%Y-%m-%d")
filename = f"raw_ligatabelle_{date_of_request}.csv"
p = r"C:/Users/BenedictAltgassenDat/OneDrive - DatenPioniere/Data Repositories/hockey-monitoring/hockey-monitoring/data/raw/"
df.to_csv(p + filename, index=False)
