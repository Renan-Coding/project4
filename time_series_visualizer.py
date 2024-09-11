import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=True)

# Clean data (Filter out top 2.5% and bottom 2.5%)
lower_bound = df['value'].quantile(0.025)
upper_bound = df['value'].quantile(0.975)

df_cleaned = df[(df['value'] >= lower_bound) & (df['value'] <= upper_bound)]

# Verify the number of lines after cleaning
print(f"Numero de linhas depois da limpeza: {df_cleaned.shape[0]}")

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df_cleaned.index, df_cleaned['value'], color='r', linewidth=1)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save image and return fig (don't change this part)
    plt.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df_cleaned.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month
    
    # Draw bar plot
    df_bar_grouped = df_bar.groupby(['year', 'month'])['value'].mean().unstack()
    fig, ax = plt.subplots(figsize=(10, 6))
    df_bar_grouped.plot(kind='bar', ax=ax)
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.set_title('Average daily page views per month, grouped by year')
    ax.legend(title='Months', labels=[
        'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'
    ])
    plt.tight_layout()
    
    # Save image and return fig (don't change this part)
    plt.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df_cleaned.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    
    # Draw box plots (using Seaborn)
    df_box['month_num'] = pd.DatetimeIndex(df_box['date']).month
    df_box = df_box.sort_values('month_num')
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    plt.tight_layout()
    
    # Save image and return fig (don't change this part)
    plt.savefig('box_plot.png')
    return fig

draw_line_plot()
draw_bar_plot()
draw_box_plot()