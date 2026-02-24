# MarketplacePricing


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**use_case** | **str** |  | 
**currency_code** | **str** |  | [optional] 
**amount** | **int** |  | [optional] 
**unit** | **str** |  | [optional] 

## Example

```python
from pulsepoint_liveramp.models.marketplace_pricing import MarketplacePricing

# TODO update the JSON string below
json = "{}"
# create an instance of MarketplacePricing from a JSON string
marketplace_pricing_instance = MarketplacePricing.from_json(json)
# print the JSON string representation of the object
print(MarketplacePricing.to_json())

# convert the object into a dict
marketplace_pricing_dict = marketplace_pricing_instance.to_dict()
# create an instance of MarketplacePricing from a dict
marketplace_pricing_from_dict = MarketplacePricing.from_dict(marketplace_pricing_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


