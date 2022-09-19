# Median Time Series Decomposition

This is a Python class to perfom robust time series decomposition on multiple time series at once. It supports time series with daily and weekly seasonality, and uses medians to construct the trend and seasonal components to be very robust against outliers. 

### Primary Use Case: Outlier Detection

One method for outlier detection in seasonal time series is to decompose the time series (trend, seasonal, residual) and then look for outliers in the residual component. However, this may not work well tradditional methods like STL Decomposition when the outliers are really bad because they will influence both the trend and seasonal components and invalidate the model. Using medians ensures that the outliers will only influence the residual component. 

Once outliers are detected, then they could be removed/replaced and a traditional method like STL Decomposition could then be applied for further forecasting/analysis if needed. 
