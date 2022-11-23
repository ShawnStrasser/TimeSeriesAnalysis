# Median Time Series Decomposition
## Please see "Example.ipynb" in this repository for an example use case
## Contributions welcome!

A Python class to perform robust time series decomposition on multiple time series at once. It decomposes the time series into the trend, daily, weekly, and residual components using medians (rather than means). Gaps in the time series are allowed.

Using medians ensures that severe outliers do not influence the trend and seasonal components. After decomposing a time series, additional analytics can be applied, like anomaly detection (see below) or change point detection (to be added soon).  

### Some Drawbacks
The rolling median calculation is slow, it still needs to be vectorized. 

The seasonal components are not allowed to change over time, therefore, it is important to limit the number of weeks included in the model, especially if there is yearly seasonality to consider. The recommended use for application over a long date range is to run the algorithm incrementally over a rolling window of dates.

If outliers in the time series always skew high, then forecasts made by this model would be systemically low because in a right tailed distribution the median will be lower than the mean. Not really a drawback, just an FYI.

### Future Plans/Support
Holidays and a yearly component will be included, might happen during Q2 2023, or sooner with help. 

# Anomaly Detection

A Python class to identify anomalies in multiple time series at once. Time series should be decomposed first (as above), and then anomaly classification should be done on the residuals. 

Sometimes when you have a group of related time series, like vehicle travel times within the same city, they will all be impacted by certain factors outside the regular seasonal components. For example, a snow storm would cause travel times across the city to drop. When looking at individual road segments, this would result in anomalies showing up at all of them. To account for system/group-wide events like this, an optional grouping column can be included. The result that this has is that only time series timestamps that have statistically significant residual components AND SIGNIFICANTLY DEVIATE FROM THE REST OF THE GROUP will be classified as an anomaly.