# Median Time Series Decomposition
## Please see "Example.ipynb" in this repository for an example use case

This is a Python class to perform robust time series decomposition on multiple time series at once. It decomposes the time series into the trend, daily, weekly, and residual components using medians (rather than means). Gaps in the time series are allowed.

Using medians ensures that severe outliers do not influence the trend and seasonal components. The primary use case for this is for outlier detection, which can be performed by normalizing the residuals. 

# Other thoughts

A drawback of this method is that the seasonal components are not allowed to change over time. Therefore, it is important to limit the number of weeks included in the model, especially if there is yearly seasonality to consider. In the future, holidays and a yearly component will be added. 

If outliers in the time series always skew high, then forecasts made by this model would be systemically low. For example, in a right tailed distribution the median will be lower than the mean. 