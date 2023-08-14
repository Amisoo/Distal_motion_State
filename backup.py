import pandas as pd
from get_title_graph import get_title_graph
import plotly.express as px



def main(arg):
    df = pd.read_csv(arg)

    mask = df['Motion_State'] == 4
    mask = mask.astype(int).diff()

    # start, end protective stop
    timestamps_start = pd.to_datetime(df['timestamps'][mask == 1]).tolist()
    timestamps_stop = pd.to_datetime(df['timestamps'][mask == -1]).tolist()

    # finish record on state 4
    timestamps_first_row = pd.to_datetime(df['timestamps']).tolist()
    timestamps_first_row = pd.to_datetime(timestamps_first_row).tolist()
    timestamps_first_row = timestamps_first_row[0]

    timestamps_last_row = df['timestamps'].tolist()
    timestamps_last_row = pd.to_datetime(timestamps_last_row).tolist()
    timestamps_last_row = timestamps_last_row[-1]

    if len(timestamps_start) > len(timestamps_stop):
        timestamps_stop.append(timestamps_last_row)
    elif len(timestamps_start) < len(timestamps_stop):
        timestamps_start.append(timestamps_first_row)
    # duration of state 4
    durations = pd.to_datetime(timestamps_stop) - pd.to_datetime(timestamps_start)

    # plot

    fmt = '%H:%M:%S.%f'
    # variable and axis
    timedelta = durations.total_seconds()
    timedelta_plot = pd.Series(timedelta)

    timestamps_start = pd.to_datetime(timestamps_start).strftime(fmt)

    timestamps_start = [time[:-4] for time in timestamps_start]

    bar_color = []
    for time in timedelta_plot:
        if time >= 3:
            bar_color.append('red > 3 [s]')
        else:
            bar_color.append('blue < 3 [s]')

    data_tuples = list(zip(timestamps_start, timedelta_plot))
    df2 = pd.DataFrame(data_tuples, columns=['Date [H:M:S.f]', 'Time [s]'])


    fig = px.bar(df2, x="Date [H:M:S.f]", y="Time [s]",
                 color=bar_color,
                 title=get_title_graph(arg),
                 labels={'pop': 'Time [s]'},
                 )
    fig.show()


main(r'C:\Users\arthur.herbette\Box\Arthur\csv\DX11247-1_20230725_152651-20230725_154306.csv')
