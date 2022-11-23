import numpy as np

class Anomaly():
    
    def __init__(self, df, DateTime_Name, ID_Name, Value_Name, Group_Name=None, z_score=4, return_data_type='float32'):
        '''Classify anomalies on multiple time series at once, by group, using normalization.
        Input is Pandas DF with multi-index DateTime and ID columns.
        Time series should be decomposed first, and anomaly classification should be done on the residuals.

        df: input Pandas dataframe
        DateTime_Name: TimeStamp index column name
        ID_Name: ID index column name (identifies particular entity, like a road segment, traffic light, or store or whatever)
        Value_Name: target data column that will be used to calculate anomalies
        Group_Name: Optional column by which to group/partition anomaly calculations (region/district/area)
        z_score: normalization/z_score absolute value threshold above which time periods will be classified as anomaly        
        '''
        self.df = df
        self.DateTime_Name = DateTime_Name
        self.ID_Name = ID_Name
        self.Value_Name = Value_Name
        self.Group_Name = Group_Name
        self.z_score = z_score
        self.return_data_type = return_data_type

        assert len(self.df.index.names) == 2, 'Required input is Pandas dataframe with multi-index including a datetime and ID fields'

    def normalize_by_group(self, group, column):
        '''Returns normalized values, using Vectorization for quick calculation
        Assumes an index already in place, resets the index and sets it to the group
        Takes a dataframe, a list of columns for which to group the data, and the column for which the normalization is based on
        adapted from https://stackoverflow.com/questions/26046208/normalize-dataframe-by-group'''
        df = self.df.reset_index().set_index(group)
        df = df[column]
        groups = df.groupby(level = group)
        # computes group-wise mean/std, then auto broadcasts to size of group chunk
        mean = groups.transform("mean")
        std = groups.transform("std")
        new_df = (df[mean.columns] - mean) / std
        return new_df.astype(self.return_data_type).values

    def find_anomalies(self):
        # Identify anomalies at the individual entity level, by normalizing over the ID group and classifying based on the Z-score threshold
        normalized_ID = self.normalize_by_group(group=[self.ID_Name], column=[self.Value_Name])
        entity_anomaly = np.where(abs(normalized_ID) > self.z_score, True, False)
        # Now if a group was supplied, classify anomalies based on deviation from the group in addition to above
        if self.Group_Name is not None:
            normalized_group = self.normalize_by_group(group=[self.DateTime_Name, self.Group_Name], column=[self.Value_Name])
            grouped_anomaly = np.where(abs(normalized_group) > self.z_score, True, False)
            self.df['Anomaly'] = np.where(entity_anomaly, np.where(grouped_anomaly, True, False), False)
        else:
            self.df['Anomaly'] = entity_anomaly
            
        return self.df   