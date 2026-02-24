# DestinationListResponse

Response model for: GET /v1/liveramp/destinations

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**destinations** | [**List[Destination]**](Destination.md) |  | 
**pagination** | [**Pagination**](Pagination.md) |  | 

## Example

```python
from pulsepoint_liveramp.models.destination_list_response import DestinationListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of DestinationListResponse from a JSON string
destination_list_response_instance = DestinationListResponse.from_json(json)
# print the JSON string representation of the object
print(DestinationListResponse.to_json())

# convert the object into a dict
destination_list_response_dict = destination_list_response_instance.to_dict()
# create an instance of DestinationListResponse from a dict
destination_list_response_from_dict = DestinationListResponse.from_dict(destination_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


