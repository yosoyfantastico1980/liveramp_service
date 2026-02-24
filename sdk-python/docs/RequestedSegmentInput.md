# RequestedSegmentInput


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**segment_id** | **int** |  | 
**destination_id** | **int** |  | 
**identifier_type** | **str** |  | [optional] 

## Example

```python
from pulsepoint_liveramp.models.requested_segment_input import RequestedSegmentInput

# TODO update the JSON string below
json = "{}"
# create an instance of RequestedSegmentInput from a JSON string
requested_segment_input_instance = RequestedSegmentInput.from_json(json)
# print the JSON string representation of the object
print(RequestedSegmentInput.to_json())

# convert the object into a dict
requested_segment_input_dict = requested_segment_input_instance.to_dict()
# create an instance of RequestedSegmentInput from a dict
requested_segment_input_from_dict = RequestedSegmentInput.from_dict(requested_segment_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


