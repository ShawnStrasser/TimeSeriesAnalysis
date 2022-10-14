
import datetime

class MedianDecompose():
    
    def __init__(self, df, freq_minutes=15, window='7d', drop_days=7, min_periods=56*4, 
                DateTime_Name='TimeStamp', ID_Name='XD', Value_Name='travel_time_seconds', 
                return_data_type='float32'):

        self.df = df
        self.freq = f'{freq_minutes}min'
        self.freq_minutes = freq_minutes
        self.window = window
        self.drop_days = drop_days
        self.min_periods = min_periods
        self.DateTime_Name = DateTime_Name
        self.ID_Name = ID_Name
        self.Value_Name = Value_Name
        self.return_data_type = return_data_type
        

    def fit(self):
        '''Robust decomposition using median
        Input is Pandas DataFrame with three columns (DateTime, ID, and Value)
        The input could also have DateTime and ID in the index.
        Returns DataFrame with seasonal compnents indexed by the DateTime and ID columns'''
        # Set the frequency for the rolling window to work.
        # The frequency is being set on the ID index rather than DateTime index
        # This makes makes no sense to me but the rolling calculations are working
        try:
            df = self.df.set_index([self.DateTime_Name, self.ID_Name])
        except Exception as e:
            print(f'setting index failed, attempting to reset! error: {e}')
            df = self.df.set_index([self.DateTime_Name, self.ID_Name])
        try:
            df.index.levels[1].freq = self.freq
            print(f'Frequency set at {df.index.levels[1].freq}')
        except Exception as e:
            print(f'failed to set frequency, error: {e}')
            quit()
        # Group by ID
        group = df.reset_index(level=1).groupby(self.ID_Name)
        df = df.reset_index()
        # Calculate Rolling Median (trend)
        df['RollingMedian'] = group.transform(lambda x: x.rolling(window=self.window, min_periods=self.min_periods, closed='both').median()).reset_index()[self.Value_Name]
        df.dropna(inplace=True)
        # drop first 7 days because the rolling median needs a full week
        min_date = df[self.DateTime_Name].min() + datetime.timedelta(days = self.drop_days)
        df = df[df[self.DateTime_Name] > min_date]

        # Calculate Seasons
        df['Detrend'] = df[self.Value_Name] - df.RollingMedian
        df['DayPeriod'] = ((df[self.DateTime_Name].dt.hour * 60 + df[self.DateTime_Name].dt.minute)/self.freq_minutes + 1).astype(int)
        df['WeekPeriod'] = df[self.DateTime_Name].dt.isocalendar().day
        df['SeasonDay'] = df.groupby([self.ID_Name, 'DayPeriod'])['Detrend'].transform('median')
        df['DeSeason_temp_step'] = df.Detrend - df.SeasonDay
        df['SeasonWeek'] = df.groupby([self.ID_Name, 'WeekPeriod', 'DayPeriod'])['DeSeason_temp_step'].transform('median')
        df['Resid'] = df.DeSeason_temp_step - df.SeasonWeek
        df['SeasonAdjusted'] = df.RollingMedian + df.Resid
        df = df.set_index([self.DateTime_Name, self.ID_Name])[[self.Value_Name, 'RollingMedian', 'SeasonDay', 'SeasonWeek', 'Resid', 'SeasonAdjusted']]
        return df.dropna().astype(self.return_data_type)
       