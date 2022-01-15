from core.graphs import get_graph_base, spiral_graph_with_fill, \
    spiral_graph_with_fill_single, spiral_graph_with_bars, spiral_graph, \
    spiral_graph_with_bars_2_sides, spiral_graph_with_fill_2_sides
from core.data_preprocessing import download_covid_data, preprocess_data

import pandas as pd


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

if __name__ == '__main__':
    isos = ["USA","IND"]
    # isos = ["IND", "BRA"]
    path = "/home/lenovo_e14/Documents/RKTN/spiral/data/Covid_Data.csv"
    
    download_covid_data(path)
    preprocess_data(path,isos)
    create_graph(isos)