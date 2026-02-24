# MarketplaceSegmentListResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**segments** | [**List[MarketplaceSegment]**](MarketplaceSegment.md) |  | 
**pagination** | [**Pagination**](Pagination.md) |  | 

## Example

```python
from pulsepoint_liveramp.models.marketplace_segment_list_response import MarketplaceSegmentListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of MarketplaceSegmentListResponse from a JSON string
marketplace_segment_list_response_instance = MarketplaceSegmentListResponse.from_json(json)
# print the JSON string representation of the object
print(MarketplaceSegmentListResponse.to_json())

# convert the object into a dict
marketplace_segment_list_response_dict = marketplace_segment_list_response_instance.to_dict()
# create an instance of MarketplaceSegmentListResponse from a dict
marketplace_segment_list_response_from_dict = MarketplaceSegmentListResponse.from_dict(marketplace_segment_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


