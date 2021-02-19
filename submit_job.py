import requests

datasets = {"TTM202101","TTM202007"}

Rochester = [43.27894,-77.675089,43.104461,-77.542219]
Oslo = [59.914285,10.651343,59.96908,10.79229]
CT = [41.804952,-72.727084,41.74035,-72.66723]
Nice = [43.75919,7.17061,43.69367,7.28185]
Marseille = [43.21052,5.36987,43.39024,5.51403]
Nebraska = [40.6766,-98.7238,40.4341,-98.2631]
Richmond = [37.2173,-77.8592,36.8797,-78.4140]
Knoxville = [36.1151,-84.0207,35.9857,-83.7927]
Helsinki = [60.2773,24.7769,60.2071,24.9381]
Athens = [37.9229,23.9103,38.1598,23.6089]
Rotterdam = [52.0179,4.5971,51.9002,4.3602]
Toulouse = [43.6623,1.5337,43.5238,1.3906]
Guad = [20.8004,-103.5258,20.5794,-103.2786]
Melbourne = [-37.6300,-215.2290,-37.8407,-145.7360]
Brazil = [-19.8765,-44.0119,-19.9533,-43.8842]

url = 'http://mapmetrics-frontend.innovation.maps.az.tt3.com/api/jobs/'

jobs = [Brazil,Melbourne]

for job in jobs:
    for map in datasets:
        source = job
        data = {"min": {"lat": source[0], "lon": source[1]}, "max": {"lat": source[2], "lon": source[3]},
                     "dataSet": {"dataSet": map}, "reference": {"reference": "James T - " + map}}
        x = requests.post(url, json= data)

        print(x.text)