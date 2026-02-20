# DestinationsResponse

LiveRamp returns a top-level key literally named 'v2/Destinations'. We map that to a pythonic `destinations` field via alias.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**v2_destinations** | [**List[Destination]**](Destination.md) |  | [optional] 
**pagination** | [**Pagination**](Pagination.md) |  | [optional] 

## Example

```python
from pulsepoint_liveramp.models.destinations_response import DestinationsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of DestinationsResponse from a JSON string
destinations_response_instance = DestinationsResponse.from_json(json)
# print the JSON string representation of the object
print(DestinationsResponse.to_json())

# convert the object into a dict
destinations_response_dict = destinations_response_instance.to_dict()
# create an instance of DestinationsResponse from a dict
destinations_response_from_dict = DestinationsResponse.from_dict(destinations_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


