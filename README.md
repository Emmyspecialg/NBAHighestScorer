# 2022-2023 NBA Highest Scorer
Using an open NBA stat API, I am creating an ETL pipeline to track the highest scoring player for the 2022-2023 NBA Season. 

API used: https://www.balldontlie.io/#introduction

The website provided free API to access NBA related data specifically games, player, and team statistics. We wrote a python script that extracts data from the BallDontLie API in JSON format using HTTP (ie, an HTTP request).

We parameterized the date so that we can add the date to the HTTP request dynamically with airflow.

We used pandas and lambda functions to convert the data from JSON to a dataframe

*We inspected the contents of the dataframe: all of the scorers and their scores for all NBA games played on a given date.
