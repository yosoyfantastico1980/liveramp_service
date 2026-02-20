# SegmentsResponse

Segment list key can vary by LiveRamp endpoint/version. We'll support the common patterns without you having to be perfect upfront.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**v2_segments** | [**List[Segment]**](Segment.md) |  | [optional] 
**pagination** | [**Pagination**](Pagination.md) |  | [optional] 

## Example

```python
from pulsepoint_liveramp.models.segments_response import SegmentsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SegmentsResponse from a JSON string
segments_response_instance = SegmentsResponse.from_json(json)
# print the JSON string representation of the object
print(SegmentsResponse.to_json())

# convert the object into a dict
segments_response_dict = segments_response_instance.to_dict()
# create an instance of SegmentsResponse from a dict
segments_response_from_dict = SegmentsResponse.from_dict(segments_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


