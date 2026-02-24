# Delivery


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**delivery_id** | **str** |  | [optional] 
**segment_id** | **int** |  | [optional] 
**destination_id** | **str** |  | [optional] 
**status** | **str** |  | [optional] 
**created_at** | **str** |  | [optional] 

## Example

```python
from pulsepoint_liveramp.models.delivery import Delivery

# TODO update the JSON string below
json = "{}"
# create an instance of Delivery from a JSON string
delivery_instance = Delivery.from_json(json)
# print the JSON string representation of the object
print(Delivery.to_json())

# convert the object into a dict
delivery_dict = delivery_instance.to_dict()
# create an instance of Delivery from a dict
delivery_from_dict = Delivery.from_dict(delivery_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


