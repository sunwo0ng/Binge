from sys import platform
import numpy as np
import pandas as pd
from tqdm import tqdm
from itertools import product
import datetime
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

pd.set_option("display.max_columns", None)
tqdm.pandas()

if platform == "darwin": # OS X
    plt.rcParams["font.family"] = "AppleGothic"
elif platform == "win32":
    plt.rcParams["font.family"] = "NanumGothic"
plt.rcParams["axes.unicode_minus"] = False

# data directory: modify this location
data_dir = "../data_raw/" # Euro

# study period
window_sday = "2021-11-01"
window_eday = "2022-03-31"

# stage to number
map_stage = {"데메테르":1,"로부르":2,"우스터":3,"오마하":4,"카슨":5,
             "도버":6,"새크라멘토":7,"루인스":8,"네레우스":9,"라이칸의":10}

# simple preprocessing
def simple_preprocess(df):
	# drop developer accounts
	df = df.query("player_slug not in @l_dev_player").reset_index(drop=True)

	# convert UTC to Korea Standard Time (KST)
	df["event_datetime"] = pd.to_datetime(df["event_datetime"]) + datetime.timedelta(hours=9)
	
	# within study period
	df = df.query("@window_sday<=event_datetime<=@window_eday")
	df = df.drop_duplicates().sort_values(by="event_datetime").reset_index(drop=True)

	return df

# developer accounts
l_dev_player = [np.nan,
                "테스트","트래킹테스트3","트래킹테스트6","트래킹테스트18",
                "2022-01-24T04:00:26.286Z","2022-01-24T04:02:03.664Z","2022-01-24T10:42:58.176Z",
                "2022-02-14T06:06:32.718Z","2021-09-09T10:00:18.360Z","2021-09-09T11:05:34.577Z",
                "2021-09-16T03:12:53.041Z","2021-09-20T03:36:51.610Z","2021-10-15T02:51:03.576Z",
                "2021-10-15T02:53:21.810Z","2021-10-28T00:13:17.925Z","2021-11-19T14:19:04.927Z",
                "2021-11-19T14:43:04.477Z","2021-12-14T07:11:17.945Z","2021-12-15T15:37:44.019Z",
                "2021-12-22T14:28:33.769Z","2022-03-09T05:48:15.402Z","2022-03-09T18:00:39.806Z",
                
                # Windows 10
                "2021-10-15T02:04:26.232Z","2021-10-15T02:33:36.262Z","2021-11-15T12:05:28.083Z",
                "2021-11-24T08:32:07.697Z","2021-11-26T13:09:57.592Z","2021-11-26T13:19:37.731Z",
                "2021-12-01T03:01:05.114Z","2022-01-11T06:01:26.467Z","2021-11-24T08:31:41.535Z",
                "2022-03-24T06:55:35.929Z","2022-03-24T09:00:52.751Z",

                # login issues
                "2021-11-22T01:27:09.057Z","2021-11-28T16:27:16.427Z","2021-12-21T11:11:45.093Z",
                "2022-01-13T03:38:43.104Z","2022-01-26T10:27:14.888Z","2022-02-06T01:43:53.254Z",
                "2022-02-26T03:50:24.003Z","2022-03-16T05:30:48.865Z","2022-03-18T03:27:11.240Z",
                "2022-03-20T02:24:53.779Z",

                # extreme purchase
                "2021-12-19T12:31:58.436Z",
                ]