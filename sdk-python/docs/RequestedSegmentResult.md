# RequestedSegmentResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**segment_id** | **int** |  | [optional] 
**request_id** | **str** |  | [optional] 
**status** | **str** |  | [optional] 

## Example

```python
from pulsepoint_liveramp.models.requested_segment_result import RequestedSegmentResult

# TODO update the JSON string below
json = "{}"
# create an instance of RequestedSegmentResult from a JSON string
requested_segment_result_instance = RequestedSegmentResult.from_json(json)
# print the JSON string representation of the object
print(RequestedSegmentResult.to_json())

# convert the object into a dict
requested_segment_result_dict = requested_segment_result_instance.to_dict()
# create an instance of RequestedSegmentResult from a dict
requested_segment_result_from_dict = RequestedSegmentResult.from_dict(requested_segment_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


