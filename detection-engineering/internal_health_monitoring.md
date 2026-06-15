# Splunk Query: Splunk Internal Health Dashboard

## Objective
To visualize the operational health of the Splunk instance by categorizing internal logs into "Critical" vs. "Noise" trends over time.

## The SPL Query
```splunk
index=_internal 
| eval Status=case(log_level="INFO", "Noise", log_level="ERROR", "Critical", 1=1, "Other")
| timechart span=1h count by Status
```