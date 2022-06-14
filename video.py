from core.graphs import get_graph_base, spiral_graph_with_fill, \
    spiral_graph_with_fill_single, spiral_graph_with_bars, spiral_graph, \
    spiral_graph_with_bars_2_sides, spiral_graph_with_fill_2_sides
from core.data_preprocessing import download_covid_data, preprocess_data

import pandas as pd
import matplotlib.pyplot as plt

def create_graph(isos: list,
                #  col: str = ["new_cases_smoothed", "new_deaths_smoothed"],
                 col: str = "new_cases_smoothed",
                #  refactor: float = [0.00065, 0.08],
                 refactor: float = 0.0005,
                #  colors: list = ["#f2665c"],
                 colors: list = ["#f2665c", "#6daa6b"],
                 line_color: str = "#2A363B"
                 ):
    dfs = []
    for iso in isos:
        dfs.append(pd.read_csv(f"data/{iso}_Data.csv"))
    
    fig = spiral_graph_with_bars_2_sides(dfs,col = col, refactor=refactor, isos=isos, colors = colors, line_color = line_color)
    fig.savefig("graphs/nystyle_2bar_usa_ind.jpg")

def create_video_images(iso: str = "IND",
                 col: str = "new_cases_smoothed",
                 refactor: float = 0.00065,
                 colors: list  = ["#f2665c"],
                 line_color: str = "#2A363B"
                 ):
    data = pd.read_csv(f"data/{iso}_Data.csv")
    
    for i, date in enumerate(data.date.values):
        # print(i,date)
        fig = spiral_graph_with_fill([data.iloc[:i+1]],col = col, \
                                        refactor=refactor, isos=[iso], \
                                        colors = colors, line_color = line_color, \
                                        date_today=date
                                        )
        fig.savefig(f"graphs/video_india/nystyle_2bar_india_{date}.jpg")
        plt.close("all")
        
    # ffmpeg -r 25 -pattern_type glob -i 'graphs/video_india/*.jpg' -vb 2M -vcodec mpeg4 -y movie_india.mp4
if __name__ == '__main__':
    isos = ["USA","IND"]
    # isos = ["IND", "BRA"]
    path = "/home/lenovo_e14/Documents/RKTN/spiral/data/Covid_Data.csv"
    
    download_covid_data(path)
    preprocess_data(path,isos)
    create_video_images()