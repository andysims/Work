import os
import csv

directory = "C:/KMZ/DIR/Study Areas/StudyAreaKMZs"
processed_list = []
company_lookup_csv = "C:/KMZ/DIR/Study Areas/company_lookup.csv"

for filename in os.listdir(directory):
	sac_num = filename[:6]
	processed_list.append(sac_num)

with open(company_lookup_csv) as f:
	reader = csv.reader(f, delimiter='|')
	comp_lookup = list(reader)

for company in comp_lookup:
	sac = company[0]
	if sac not in processed_list:
		print("SAC:  " + str(sac))
