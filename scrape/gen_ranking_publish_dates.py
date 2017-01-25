from datetime import timedelta, date

"""teamrankings.com/ncb/rpi/?date=2002-03-12"""

BASE_URL        = "https://www.teamrankings.com/ncb/rpi/?date="

OUTPUT_FILE     = open("ranking_dates.txt", "w")

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

if __name__ == "__main__":
    start_date  = date(2000, 10, 16)
    end_date    = date(2016, 4, 5)
    for single_date in daterange(start_date, end_date):
        if ((single_date.month == 10 and single_date.day >= 15) or \
            (single_date.month >= 11 or single_date.month <= 3) or \
            (single_date.month == 4 and single_date.day <= 10)) and \
            (single_date.isoweekday() == 1):
            date = single_date.strftime("%Y-%m-%d")
            OUTPUT_FILE.write(BASE_URL + date + "\n")
    OUTPUT_FILE.close()