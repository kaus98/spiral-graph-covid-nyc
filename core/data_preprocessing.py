import pandas as pd
import wget 
import json, os, sys

# try:
#     from core.log import MyLogger
# except:
#     currentdir = os.path.dirname(os.path.realpath(__file__))
#     parentdir = os.path.dirname(currentdir)
#     sys.path.append(parentdir)
#     from core.log import MyLogger
    

# log_path = "logs/{filename}.log".format(filename=__file__.split('/')[-1])
# logger = MyLogger(log_path)

def download_covid_data(path: str, force:bool = False):
    if os.path.exists(path):
        if force:
            os.remove(path)
            wget.download('https://covid.ourworldindata.org/data/owid-covid-data.csv', path)
            return 
        else:
            return
    else:
        wget.download('https://covid.ourworldindata.org/data/owid-covid-data.csv', path)
        return 
        
def preprocess_data(path: str, 
                    country_codes: list, 
                    start_date: str = "2020-01-01", 
                    save_path: str = "data/",
                    cols_: list = ["total_cases", "new_cases", "new_cases_smoothed", "total_deaths", "new_deaths", "new_deaths_smoothed", "positive_rate"]):
    World_ = pd.read_csv(path)
    World_.fillna(0, inplace = True)
    World_['date'] = World_['date'].astype(str)
    
    for cc in country_codes:
        country_data = World_[World_["iso_code"] == cc]
        end_date = country_data.date.min()
        
        temp = pd.DataFrame(pd.date_range(start_date, end_date)[:-1], columns = ["date"])
        for col_ in cols_:
            temp[col_] = 0
        
        country_data = pd.concat([temp, country_data[temp.columns]], axis = 0)
        country_data['date'] = pd.to_datetime(country_data['date'])
        country_data['days_passed'] = (country_data['date'] - pd.to_datetime(start_date))/86400000000000
        country_data['days_passed'] = country_data['days_passed'].astype(int)
        
        country_data.to_csv(os.path.join(save_path,f"{cc}_Data.csv"), index = False, header = True)
    

if __name__ == '__main__':
    path = "/home/lenovo_e14/Documents/RKTN/spiral/data/Covid_Data.csv"
    download_covid_data(path)
    preprocess_data(path, ["USA", "IND"])
        
        
