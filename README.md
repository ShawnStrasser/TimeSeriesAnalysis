# Median Time Series Decomposition

This is a Python class to perfom robust time series decomposition on multiple time series at once. It decomposes the time series into the trend, daily, weekly, and residual components useing medians (rather than means). Gaps in the time series are allowed.

Using medians ensures that severe outliers do not influce the trend and seasonal components. The primary use case for this is for outlier detection, which can be performed by normalizing the residuals. 

## Please see "Example.ipynb" in this repository for an example use case