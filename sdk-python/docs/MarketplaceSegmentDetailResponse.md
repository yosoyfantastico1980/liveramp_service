# MarketplaceSegmentDetailResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**segments** | [**List[MarketplaceSegmentDetail]**](MarketplaceSegmentDetail.md) |  | 
**pagination** | [**Pagination**](Pagination.md) |  | 

## Example

```python
from pulsepoint_liveramp.models.marketplace_segment_detail_response import MarketplaceSegmentDetailResponse

# TODO update the JSON string below
json = "{}"
# create an instance of MarketplaceSegmentDetailResponse from a JSON string
marketplace_segment_detail_response_instance = MarketplaceSegmentDetailResponse.from_json(json)
# print the JSON string representation of the object
print(MarketplaceSegmentDetailResponse.to_json())

# convert the object into a dict
marketplace_segment_detail_response_dict = marketplace_segment_detail_response_instance.to_dict()
# create an instance of MarketplaceSegmentDetailResponse from a dict
marketplace_segment_detail_response_from_dict = MarketplaceSegmentDetailResponse.from_dict(marketplace_segment_detail_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


