import pandas as pd
import plotly.express as px
from get_title_graph import get_title_graph
from plotly.subplots import make_subplots
import os
import glob
import webbrowser

class Constant:
    PROTECTIVE_STATE = 4
    SAFE_STOP_TIME = 3

def main(path):
    csv_files = glob.glob(os.path.join(path, "*.csv"))

    # html page
    html = open('protective_state.html', 'w')
    html.write(
        '<html><head><title> State of protective stop   '
        '  </title> </head>  <center> <div>   <h1 style="font-family: Arial"> State Of Protective Stop</h1>  '
        '  </div>  </center>    </body></html>')

    html.close()

    # loop over the list of csv files
    for f in csv_files:
        df = pd.read_csv(f)

        mask = df['Motion_State'] == Constant.PROTECTIVE_STATE
        mask = mask.astype(int).diff()

        # start, end protective stop
        timestamps_start = pd.to_datetime(df['timestamps'][mask == 1]).tolist()
        timestamps_stop = pd.to_datetime(df['timestamps'][mask == -1]).tolist()

        # condition if finish is on state 4
        timestamps_row = pd.to_datetime(df['timestamps']).tolist()
        timestamps_row = pd.to_datetime(timestamps_row).tolist()
        timestamps_first_row = timestamps_row[0]

        timestamps_last_row = timestamps_row[-1]

        if len(timestamps_start) > len(timestamps_stop):
            timestamps_stop.append(timestamps_last_row)
        elif len(timestamps_start) < len(timestamps_stop):
            timestamps_start.append(timestamps_first_row)

        # duration of state 4
        durations = pd.to_datetime(timestamps_stop) - pd.to_datetime(timestamps_start)

        # plot
        # format of date
        fmt = '%H:%M:%S.%f'
        # variable and axis
        timedelta = durations.total_seconds()
        timedelta_plot = pd.Series(timedelta)

        timestamps_start = pd.to_datetime(timestamps_start).strftime(fmt)

        # round time to 0.00 [s]
        timestamps_start = [time[:-4] for time in timestamps_start]

        # legend + color
        bar_color = []
        for time in timedelta_plot:
            if time >= Constant.SAFE_STOP_TIME:
                bar_color.append('red > 3 [s]')
            else:
                bar_color.append('blue < 3 [s]')

        # creation of df for plot
        data_tuples = list(zip(timestamps_start, timedelta_plot))
        df2 = pd.DataFrame(data_tuples, columns=['Date [H:M:S.f]', 'Time [s]'])

        # plot
        fig = px.bar(df2, x="Date [H:M:S.f]", y="Time [s]",
                     color=bar_color,
                     title=get_title_graph(f),
                     labels={'pop': 'Time [s]'},
                     )

        # transfer of plot to html file
        with open('protective_state.html', 'a') as d:
            d.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))

    # launch of page
    webbrowser.open('protective_state.html')


main(r"Path of folder")
