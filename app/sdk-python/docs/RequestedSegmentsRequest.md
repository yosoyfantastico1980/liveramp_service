# RequestedSegmentsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**segments** | [**List[RequestedSegmentInput]**](RequestedSegmentInput.md) |  | 

## Example

```python
from pulsepoint_liveramp.models.requested_segments_request import RequestedSegmentsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RequestedSegmentsRequest from a JSON string
requested_segments_request_instance = RequestedSegmentsRequest.from_json(json)
# print the JSON string representation of the object
print(RequestedSegmentsRequest.to_json())

# convert the object into a dict
requested_segments_request_dict = requested_segments_request_instance.to_dict()
# create an instance of RequestedSegmentsRequest from a dict
requested_segments_request_from_dict = RequestedSegmentsRequest.from_dict(requested_segments_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


