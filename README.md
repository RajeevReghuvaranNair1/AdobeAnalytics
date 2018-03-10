# AdobeAnalytics Omniture

Omniture is a simple wrapper around Adbobe Analytics api which allows you to programatically administer the adobe.
It support basic api calls like "get_endpoint", "get_queue" & "get_result"
Omniture should be always cald with username and secret

## get_endpoint
Returns the valid endpoint where the data is stored

## get_queue 
Returns the Report ID

## get_result
Returns the report corresponding to the ReportID provided.
By defaults retries for 50 times; in case the report is not available. Retry count is customizable as an optional argument.


