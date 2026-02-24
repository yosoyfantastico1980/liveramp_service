# SegmentListResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**segments** | [**List[Segment]**](Segment.md) |  | 
**pagination** | [**Pagination**](Pagination.md) |  | 

## Example

```python
from pulsepoint_liveramp.models.segment_list_response import SegmentListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SegmentListResponse from a JSON string
segment_list_response_instance = SegmentListResponse.from_json(json)
# print the JSON string representation of the object
print(SegmentListResponse.to_json())

# convert the object into a dict
segment_list_response_dict = segment_list_response_instance.to_dict()
# create an instance of SegmentListResponse from a dict
segment_list_response_from_dict = SegmentListResponse.from_dict(segment_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


