# MarketplaceSegment


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**name** | **str** |  | 
**provider** | **str** |  | [optional] 

## Example

```python
from pulsepoint_liveramp.models.marketplace_segment import MarketplaceSegment

# TODO update the JSON string below
json = "{}"
# create an instance of MarketplaceSegment from a JSON string
marketplace_segment_instance = MarketplaceSegment.from_json(json)
# print the JSON string representation of the object
print(MarketplaceSegment.to_json())

# convert the object into a dict
marketplace_segment_dict = marketplace_segment_instance.to_dict()
# create an instance of MarketplaceSegment from a dict
marketplace_segment_from_dict = MarketplaceSegment.from_dict(marketplace_segment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


