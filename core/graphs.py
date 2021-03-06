from cProfile import label
import pandas as pd
import numpy as np
import os, json
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.pyplot import text
plt.style.use("ggplot")
import matplotlib.cm as cm 
from matplotlib.offsetbox import AnchoredText

def get_graph_base(max_n: int, 
                   line_color: str, 
                   offset_radius: int = 100,
                   ancor_text: str = "By: kaus98", 
                   date_today: str = None):
    months = pd.Series([31, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]).cumsum() #Calendar to set angles for each month
    angles = pd.Series(np.linspace(0, 2*np.pi*(max_n/365) , max_n))
    radius = pd.Series(list(range(max_n))) + offset_radius
    
    fig = plt.figure(figsize=(14,17.4), facecolor='white') 
    ax = fig.add_subplot(111, polar=True)
    ax.set_facecolor('white')
    ax.set_theta_direction(-1) # Make Graph go Clockwise 
    ax.set_theta_offset(np.pi/2.0) # Add Offset of 90 Deg
    ax.set_xticks(np.deg2rad(months/months.max()*360).values) 
    ax.set_xticklabels([ 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec','Jan']) # Setting the Labels for X Ticks
    ax.set_yticks([]) # Adding the Y-Ticks for Each Year
    ax.set_yticklabels([])   
    ax.set_yticks([0+offset_radius,365+offset_radius, 2*365+offset_radius]) # Adding the Y-Ticks for Each Year
    ax.set_yticklabels(["", "", ""])    
    ax.grid(True, color = "#000000", linewidth = "0.1", linestyle = "solid" )
    
    # Making the Base Spiral Line 
    ax.plot(angles, radius, color = line_color, linewidth = "1.5", label = "Days Since 2020/01/01")
    
    ancor_text = AnchoredText(ancor_text, loc = "lower right", prop=dict(alpha=0.4)) # Adding the Watermark Text
    ax.add_artist(ancor_text)
    if date_today is None: date_today = datetime.today().strftime("%Y/%m/%d")
    ax.set_title(f"COVID-19 Cases ({date_today})", y = 1.08, fontdict={"fontsize":26, "fontname": "impact"}) # Setting the Title
    return fig, ax, angles, radius

def spiral_graph_with_fill(dfs: list,
                           col: str, 
                           refactor: float,
                           colors: list,
                           isos: list, 
                           line_color: str,
                           date_today: str = None
                           ):
    
    assert len(dfs) == len(colors)
    max_n = dfs[0]["days_passed"].max()+1
    fig, ax, angles, radius = get_graph_base(max_n, line_color, date_today = date_today)
    
    for df, color, cc in zip(dfs, colors, isos):
        cases_factor = (df[col]/2)*refactor
        ax.fill_between(angles, radius-cases_factor, radius+cases_factor, alpha = 0.4, color = color, label = f"COVID'19 Cases \n{cc}")
        ax.plot(angles, radius-cases_factor, color = color, alpha = 0.8, linewidth = "0.9")
        ax.plot(angles, radius+cases_factor, color = color, alpha = 0.8, linewidth = "0.9")
    plt.tight_layout(pad=3.4)
    ax.legend(loc = "upper right")
    return fig

def spiral_graph_with_fill_2_sides(dfs: list,
                           cols: list , 
                           refactors: list,
                           colors: list,
                           isos: list, 
                           line_color: str
                           ):
    
    # assert len(dfs) == len(colors)
    max_n = dfs[0]["days_passed"].max()+1
    fig, ax, angles, radius = get_graph_base(max_n, line_color)
    
    if True:
        df, col, refactor, color, cc = dfs[0], cols[0], refactors[0], colors[0], isos[0]
        cases_factor = (df[col]/2)*refactor
        ax.fill_between(angles, radius, radius+cases_factor, alpha = 0.4, color = color, label = f"COVID'19 Cases \n{cc}")
        ax.plot(angles, radius+cases_factor, color = color, alpha = 0.8, linewidth = "0.9")
        
    if True:
        df, col, refactor, color, cc = dfs[0], cols[1], refactors[1], colors[1], isos[0]
        cases_factor = (df[col]/2)*refactor
        ax.fill_between(angles, radius-cases_factor, radius, alpha = 0.4, color = color, label = f"COVID'19 Deceased Cases \n{cc}")
        ax.plot(angles, radius-cases_factor, color = color, alpha = 0.8, linewidth = "0.9")
          
    plt.tight_layout(pad=3.4)
    ax.legend(loc = "upper right")
    return fig
        
def spiral_graph_with_fill_single(dfs: list,
                           col: str, 
                           refactor: float,
                           colors: list,
                           isos: list, 
                           line_color: str
                           ):
    
    assert len(dfs) == len(colors)
    max_n = dfs[0]["days_passed"].max()+1
    fig, ax, angles, radius = get_graph_base(max_n, line_color)
    
    for df, color, cc in zip(dfs, colors, isos):
        cases_factor = (df[col])*refactor
        ax.fill_between(angles, radius, radius+cases_factor, alpha = 0.4, color = color, label = f"New COVID-19 Cases\n{cc}")
        ax.plot(angles, radius+cases_factor, color = color, alpha = 0.8, linewidth = "0.9")
    plt.tight_layout(pad=3.4)
    ax.legend(loc = "upper right")
    return fig

def spiral_graph(dfs: list,
                           col: str, 
                           refactor: float,
                           colors: list,
                           isos: list, 
                           line_color: str
                           ):
    
    assert len(dfs) == len(colors)
    max_n = dfs[0]["days_passed"].max()+1
    fig, ax, angles, radius = get_graph_base(max_n, line_color)
    plt.tight_layout(pad=3.4)
    ax.legend(loc = "upper right")
    return fig
        
def spiral_graph_with_bars(dfs: list,
                           col: str, 
                           refactor: float,
                           colors: list,
                           isos: list, 
                           line_color: str
                           ):
    
    assert len(dfs) == len(colors)
    max_n = dfs[0]["days_passed"].max()+1
    fig, ax, angles, radius = get_graph_base(max_n, line_color)
    
    for df, color, cc in zip(dfs, colors, isos):
        cases_factor = (df[col])*refactor
        # ax.fill_between(angles, radius, radius+cases_factor, alpha = 0.4, color = color, label = f"New COVID-19 Cases\n{cc}")
        # ax.scatter(angles, radius+cases_factor, color = color, alpha = 0.8, linewidth = "0.9")
        ax.plot(angles, radius+cases_factor, ".", color = color, alpha = 0.8, linewidth = "0.9", label = f"COVID Cases \n{cc}")
        for ag, rd, cf  in zip(angles, radius, cases_factor):
            
            ax.plot([ag, ag], [rd, rd+cf],color = color, alpha = 0.8, linewidth = "0.9")
    plt.tight_layout(pad=3.4)
    ax.legend(loc = "upper right")
    return fig


def spiral_graph_with_bars_2_sides(dfs: list,
                           col: str, 
                           refactor: float,
                           colors: list,
                           isos: list, 
                           line_color: str
                           ):
    
    assert len(dfs) == len(colors)
    assert len(dfs) == 2
    
    max_n = dfs[0]["days_passed"].max()+1
    fig, ax, angles, radius = get_graph_base(max_n, line_color)
    
    df = dfs[0]
    color = colors[0]
    cc = isos[0]
    
    cases_factor = (df[col])*refactor
    ax.plot(angles, radius+cases_factor, ".", color = color, alpha = 0.8, linewidth = "0.9", label = f"COVID Cases \n{cc}")
    for ag, rd, cf  in zip(angles, radius, cases_factor):
        ax.plot([ag, ag], [rd, rd+cf],color = color, alpha = 0.8, linewidth = "0.9")
            
    df = dfs[1]
    color = colors[1]
    cc = isos[1]
    
    cases_factor = (df[col])*refactor
    ax.plot(angles, radius-cases_factor, ".", color = color, alpha = 0.8, linewidth = "0.9", label = f"COVID Cases \n{cc}")
    for ag, rd, cf  in zip(angles, radius, cases_factor):
        ax.plot([ag, ag], [rd, rd-cf],color = color, alpha = 0.8, linewidth = "0.9")
            
            
                  
    plt.tight_layout(pad=3.4)
    ax.legend(loc = "upper right")
    return fig

        