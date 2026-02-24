# SegmentStatus


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**segment_id** | **int** |  | 
**destination_id** | **int** |  | [optional] 
**status** | **str** |  | [optional] 
**last_updated** | **str** |  | [optional] 

## Example

```python
from pulsepoint_liveramp.models.segment_status import SegmentStatus

# TODO update the JSON string below
json = "{}"
# create an instance of SegmentStatus from a JSON string
segment_status_instance = SegmentStatus.from_json(json)
# print the JSON string representation of the object
print(SegmentStatus.to_json())

# convert the object into a dict
segment_status_dict = segment_status_instance.to_dict()
# create an instance of SegmentStatus from a dict
segment_status_from_dict = SegmentStatus.from_dict(segment_status_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


