# MarketplaceSegmentDetail


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**segment_id** | **int** |  | 
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**category** | **str** |  | [optional] 
**country_codes** | **List[str]** |  | [optional] 
**currency_codes** | **List[str]** |  | [optional] 
**identifier_types** | **List[str]** |  | [optional] 

## Example

```python
from pulsepoint_liveramp.models.marketplace_segment_detail import MarketplaceSegmentDetail

# TODO update the JSON string below
json = "{}"
# create an instance of MarketplaceSegmentDetail from a JSON string
marketplace_segment_detail_instance = MarketplaceSegmentDetail.from_json(json)
# print the JSON string representation of the object
print(MarketplaceSegmentDetail.to_json())

# convert the object into a dict
marketplace_segment_detail_dict = marketplace_segment_detail_instance.to_dict()
# create an instance of MarketplaceSegmentDetail from a dict
marketplace_segment_detail_from_dict = MarketplaceSegmentDetail.from_dict(marketplace_segment_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


