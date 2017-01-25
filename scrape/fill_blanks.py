import random as r, pandas as pd
FILES = [
"2001_pro.csv", \
"2002_pro.csv", \
"2003_pro.csv", \
"2004_pro.csv", \
"2005_pro.csv", \
"2006_pro.csv", \
"2007_pro.csv", \
"2008_pro.csv", \
"2009_pro.csv", \
"2010_pro.csv", \
"2011_pro.csv", \
"2012_pro.csv", \
"2013_pro.csv", \
"2014_pro.csv"
]

for file in FILES: 
    df = pd.read_csv(file)
    output_filename = file[:-4]
    output_file = open(output_filename + "_out.csv", "w")
    output_file.write("date,team_1,team_2,margin_of_victory\n")
    for ind, row in df.iterrows():
        date                = row['date']
        team_1              = str(row['team_1'])
        team_2              = str(row['team_2'])
        margin_of_victory   = str(row['margin_of_victory'])
        if team_1 == ' ' or team_1.startswith("#VALUE!"):
            team_1 = str(r.random())
        if team_2 == ' ' or team_2.startswith("#VALUE!"):
            team_2 = str(r.random())
        row = date + "," + team_1 + "," + team_2 + "," + margin_of_victory
        output_file.write(row + "\n")
    output_file.close()
