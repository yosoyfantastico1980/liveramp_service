# RequestedSegmentsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**results** | [**List[RequestedSegmentResult]**](RequestedSegmentResult.md) |  | 

## Example

```python
from pulsepoint_liveramp.models.requested_segments_response import RequestedSegmentsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RequestedSegmentsResponse from a JSON string
requested_segments_response_instance = RequestedSegmentsResponse.from_json(json)
# print the JSON string representation of the object
print(RequestedSegmentsResponse.to_json())

# convert the object into a dict
requested_segments_response_dict = requested_segments_response_instance.to_dict()
# create an instance of RequestedSegmentsResponse from a dict
requested_segments_response_from_dict = RequestedSegmentsResponse.from_dict(requested_segments_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


