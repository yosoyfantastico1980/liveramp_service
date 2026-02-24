# SegmentStatusListResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**statuses** | [**List[SegmentStatus]**](SegmentStatus.md) |  | 
**pagination** | [**Pagination**](Pagination.md) |  | 

## Example

```python
from pulsepoint_liveramp.models.segment_status_list_response import SegmentStatusListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SegmentStatusListResponse from a JSON string
segment_status_list_response_instance = SegmentStatusListResponse.from_json(json)
# print the JSON string representation of the object
print(SegmentStatusListResponse.to_json())

# convert the object into a dict
segment_status_list_response_dict = segment_status_list_response_instance.to_dict()
# create an instance of SegmentStatusListResponse from a dict
segment_status_list_response_from_dict = SegmentStatusListResponse.from_dict(segment_status_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


