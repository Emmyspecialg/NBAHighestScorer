import requests
import pandas as pd
import json

date = "2022-10-18"

test = requests.get(
    f"https://www.balldontlie.io/api/v1/stats?dates[]={date}&per_page=100"
)
#print(test.json())


df = pd.DataFrame(test.json()["data"])
df.to_csv("testdata.csv")
ids = df.player.apply(lambda x: x["id"])
first_name = df.player.apply(lambda x: x["first_name"])
last_name = df.player.apply(lambda x: x["last_name"])
points = df.pts

nbascores = pd.DataFrame(
    columns=["id", "first_name", "last_name", "points"],
 data=zip(ids, first_name, last_name, points),
)

nbascores.to_csv(f"scores_{date}.csv")

