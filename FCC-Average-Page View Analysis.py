#!/usr/bin/env python
# coding: utf-8

# In[17]:


import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import matplotlib.patches as mpatches


# importing data from local drive and setting 'date' column as index of DataFrame
df = pd.read_csv('fcc-forum-pageviews.csv', index_col = 'date')
df.index = pd.to_datetime(df.index)

# Selecting data between top 2.5% and bottom 2.5% of DataFrame
df = df[df['value'].between(np.percentile(df,2.5),np.percentile(df,97.5))]


# defining a function to create a matplotlib line-plot
def draw_line_plot():

    ticks = pd.date_range('2016-06-01', '2020-06-01', freq = '6M')
    labels = ['2016-07','2017-01','2017-07','2018-01',
              '2018-07','2019-01','2019-07', '2020-01']
    
    # creating canvas and grid
    fig, ax = plt.subplots(figsize = (20,6))
    res = plt.plot(df.index, df['value'], color = 'tab:red')
    
    # line-plot decorations
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019', size=14)
    plt.xticks(ticks = ticks, labels = labels)
    plt.xlabel('Date', size=14)
    plt.ylabel('Page Views', size=14)
    
    # save image
    fig.savefig('line_plot.png')
    
    # returning None to avoid duplicate plots
    return None


# defining a matplotlib bar plot

def draw_bar_plot():
    
    # creating two new columns named 'year' and 'month
    df['year'] = df.index.year
    df['month'] = df.index.month
    
    # creating a groupby object by grouping the DataFrame according to 'year'
    grp = df.groupby('year')
    
    
    #explicitly making groups
    first = grp.get_group(2016)
    second = grp.get_group(2017)
    third = grp.get_group(2018)
    fourth = grp.get_group(2019)

    # defining a function which returns a list of months for a group passed as the argument, to be plotted at y-axis of bar plot
    def months_list(data):
        x = []
        y = [0]*12
        for i in data['month']:
            if i not in x:
                x.append(i)
        for j in x:
            y[j-1] = j
        return y
    
    
    # defining a function which returns a list of monthly average page-views for a group as the argument, to be plotted at y-axis of bar plot
    def avg_monthly_view(data):
        x = months_list(data)
        z = []
        for i in x:
            if i == 0:
                z.append(0)
            else: z.append(data[data['month'] == i].aggregate(np.average)['value'])
        return z

    # creating a list of colors for each bar, representing each month of the year
    color = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red','tab:purple', 'tab:brown',
            'tab:pink','tab:gray', 'tab:olive','tab:cyan','tab:blue', 'tab:orange']

    # creating a list of month names  
    labels = (pd.date_range('2021-01-01',periods = 12,freq='M').month_name()).tolist()
    
    # drawing a canvas and grid
    fig, ax = plt.subplots(figsize = (10,8))
   
    # creaing a bar plot   
    i = 0
    while i < 12:
        plt.bar(months_list(first)[i]-7, avg_monthly_view(first)[i], width = 1, align = 'edge', color = color[i])
        plt.bar(months_list(second)[i]+13, avg_monthly_view(second)[i], width = 1, align = 'edge', color = color[i])
        plt.bar(months_list(third)[i]+33, avg_monthly_view(third)[i], width = 1, align = 'edge', color = color[i])
        plt.bar(months_list(fourth)[i]+53, avg_monthly_view(fourth)[i], width = 1, align = 'edge', color = color[i])
        i += 1

    # bar plot decorations 
    plt.xticks([0,20,40,60], labels = [2016,2017,2018,2019], rotation = 90)
    plt.xlabel('Years', fontsize = 14)
    plt.ylabel('Average Page Views', fontsize = 14)

    plt.legend(handles=[mpatches.Patch(color = color[i], label = labels[i]) for i in range(0,12)], 
              title = 'Months', loc='upper left',
              labelspacing = 1, columnspacing = 2,
              fontsize = 10)
    
    # saving canvas
    fig.savefig('bar_plot.png')
    return None

def draw_box_plot():

    # creating a duplicate DataFrame for inserting new columns
    
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    
    # inserting new columns
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.month for d in df_box.date]
    month_name = ['Jan','Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    years = [2016,2017,2018,2019]
    yticks = [20000*x for x in range(0, 11)]  

    # drawing a canvas
    fig = plt.figure(figsize = (25,9))
    
    # creating two subplots on canvas
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    
    # plotting Year-wise Box Plot (Trend) on ax1
    sns.boxplot(x = df_box['year'], y = list(df_box['value']), data = df_box, fliersize = 2,ax = ax1)
    
    # decorations
    plot1.set_ylim(0,200000)
    plot1.set_title('Year-wise Box Plot (Trend)',size = 15)
    plot1.set_yticks(yticks)
    plot1.set_xticklabels(years,size = 14)
    plot1.set_xlabel('Year', size = 17)
    plot1.set_ylabel('Page Views',size = 15)

    # plotting Month-wise Box Plot (Seasonality) on ax2
    sns.boxplot(x = df_box['month'], y = list(df_box['value']), data = df_box, fliersize = 2, ax = ax2)
    
    # decorations
    plot2.set_ylim(0, 200000)
    plot2.set_yticks(yticks)
    plot2.set_title('Month-wise Box Plot (Seasonality)',size = 15)
    plot2.set_xticklabels(month_name, size = 14)
    plot2.set_xlabel('Month', size = 15)
    plot2.set_ylabel('Page Views',size = 15)

    # save image
    fig.savefig('box_plot.png')
    return None

