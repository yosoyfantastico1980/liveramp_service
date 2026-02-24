# pulsepoint_liveramp.V1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_marketplace_segment_detail**](V1Api.md#get_marketplace_segment_detail) | **GET** /v1/liveramp/marketplace/segments/detail | Marketplace Segments Detail
[**get_segment_statuses**](V1Api.md#get_segment_statuses) | **GET** /v1/liveramp/segment-statuses | List Segment Statuses
[**health_v1_health_get**](V1Api.md#health_v1_health_get) | **GET** /v1/health | Health
[**list_deliveries**](V1Api.md#list_deliveries) | **GET** /v1/liveramp/deliveries | Deliveries
[**list_destinations**](V1Api.md#list_destinations) | **GET** /v1/liveramp/destinations | List Destinations
[**list_first_party_segments**](V1Api.md#list_first_party_segments) | **GET** /v1/liveramp/segments | List First Party Segments
[**list_marketplace_segments**](V1Api.md#list_marketplace_segments) | **GET** /v1/liveramp/marketplace/segments | List Marketplace Segments
[**ready_v1_ready_get**](V1Api.md#ready_v1_ready_get) | **GET** /v1/ready | Ready
[**request_segments**](V1Api.md#request_segments) | **POST** /v1/liveramp/requested-segments | Request Segments For Activation


# **get_marketplace_segment_detail**
> MarketplaceSegmentDetailResponse get_marketplace_segment_detail(ids, limit=limit, x_lr_org_id=x_lr_org_id)

Marketplace Segments Detail

### Example


```python
import pulsepoint_liveramp
from pulsepoint_liveramp.models.marketplace_segment_detail_response import MarketplaceSegmentDetailResponse
from pulsepoint_liveramp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = pulsepoint_liveramp.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with pulsepoint_liveramp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pulsepoint_liveramp.V1Api(api_client)
    ids = [[1012603801,1012603871]] # List[int] | One or more LiveRamp Marketplace segment IDs. Click 'Add integer item' and provide at least one ID. Multiple IDs may be supplied.
    limit = 10 # int |  (optional) (default to 10)
    x_lr_org_id = 'x_lr_org_id_example' # str |  (optional)

    try:
        # Marketplace Segments Detail
        api_response = api_instance.get_marketplace_segment_detail(ids, limit=limit, x_lr_org_id=x_lr_org_id)
        print("The response of V1Api->get_marketplace_segment_detail:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling V1Api->get_marketplace_segment_detail: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ids** | [**List[int]**](int.md)| One or more LiveRamp Marketplace segment IDs. Click &#39;Add integer item&#39; and provide at least one ID. Multiple IDs may be supplied. | 
 **limit** | **int**|  | [optional] [default to 10]
 **x_lr_org_id** | **str**|  | [optional] 

### Return type

[**MarketplaceSegmentDetailResponse**](MarketplaceSegmentDetailResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_segment_statuses**
> SegmentStatusListResponse get_segment_statuses(segment_ids, segment_type, limit=limit, x_lr_org_id=x_lr_org_id)

List Segment Statuses

### Example


```python
import pulsepoint_liveramp
from pulsepoint_liveramp.models.segment_status_list_response import SegmentStatusListResponse
from pulsepoint_liveramp.models.segment_type import SegmentType
from pulsepoint_liveramp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = pulsepoint_liveramp.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with pulsepoint_liveramp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pulsepoint_liveramp.V1Api(api_client)
    segment_ids = [56] # List[int] | One or more LiveRamp segment IDs
    segment_type = pulsepoint_liveramp.SegmentType() # SegmentType | Type of segment
    limit = 50 # int | Max number of records to return (optional) (default to 50)
    x_lr_org_id = 'x_lr_org_id_example' # str |  (optional)

    try:
        # List Segment Statuses
        api_response = api_instance.get_segment_statuses(segment_ids, segment_type, limit=limit, x_lr_org_id=x_lr_org_id)
        print("The response of V1Api->get_segment_statuses:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling V1Api->get_segment_statuses: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **segment_ids** | [**List[int]**](int.md)| One or more LiveRamp segment IDs | 
 **segment_type** | [**SegmentType**](.md)| Type of segment | 
 **limit** | **int**| Max number of records to return | [optional] [default to 50]
 **x_lr_org_id** | **str**|  | [optional] 

### Return type

[**SegmentStatusListResponse**](SegmentStatusListResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **health_v1_health_get**
> object health_v1_health_get()

Health

### Example


```python
import pulsepoint_liveramp
from pulsepoint_liveramp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = pulsepoint_liveramp.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with pulsepoint_liveramp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pulsepoint_liveramp.V1Api(api_client)

    try:
        # Health
        api_response = api_instance.health_v1_health_get()
        print("The response of V1Api->health_v1_health_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling V1Api->health_v1_health_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_deliveries**
> DeliveryListResponse list_deliveries(integration_connection_id, limit=limit, x_lr_org_id=x_lr_org_id)

Deliveries

### Example


```python
import pulsepoint_liveramp
from pulsepoint_liveramp.models.delivery_list_response import DeliveryListResponse
from pulsepoint_liveramp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = pulsepoint_liveramp.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with pulsepoint_liveramp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pulsepoint_liveramp.V1Api(api_client)
    integration_connection_id = 56 # int | LiveRamp integration connection ID
    limit = 50 # int | Max number of records to return (optional) (default to 50)
    x_lr_org_id = 'x_lr_org_id_example' # str |  (optional)

    try:
        # Deliveries
        api_response = api_instance.list_deliveries(integration_connection_id, limit=limit, x_lr_org_id=x_lr_org_id)
        print("The response of V1Api->list_deliveries:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling V1Api->list_deliveries: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **integration_connection_id** | **int**| LiveRamp integration connection ID | 
 **limit** | **int**| Max number of records to return | [optional] [default to 50]
 **x_lr_org_id** | **str**|  | [optional] 

### Return type

[**DeliveryListResponse**](DeliveryListResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_destinations**
> DestinationListResponse list_destinations(limit=limit, after=after, x_lr_org_id=x_lr_org_id)

List Destinations

### Example


```python
import pulsepoint_liveramp
from pulsepoint_liveramp.models.destination_list_response import DestinationListResponse
from pulsepoint_liveramp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = pulsepoint_liveramp.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with pulsepoint_liveramp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pulsepoint_liveramp.V1Api(api_client)
    limit = 10 # int |  (optional) (default to 10)
    after = 'after_example' # str |  (optional)
    x_lr_org_id = 'x_lr_org_id_example' # str |  (optional)

    try:
        # List Destinations
        api_response = api_instance.list_destinations(limit=limit, after=after, x_lr_org_id=x_lr_org_id)
        print("The response of V1Api->list_destinations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling V1Api->list_destinations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**|  | [optional] [default to 10]
 **after** | **str**|  | [optional] 
 **x_lr_org_id** | **str**|  | [optional] 

### Return type

[**DestinationListResponse**](DestinationListResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_first_party_segments**
> SegmentListResponse list_first_party_segments(limit=limit, after=after, x_lr_org_id=x_lr_org_id)

List First Party Segments

### Example


```python
import pulsepoint_liveramp
from pulsepoint_liveramp.models.segment_list_response import SegmentListResponse
from pulsepoint_liveramp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = pulsepoint_liveramp.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with pulsepoint_liveramp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pulsepoint_liveramp.V1Api(api_client)
    limit = 50 # int |  (optional) (default to 50)
    after = 'after_example' # str |  (optional)
    x_lr_org_id = 'x_lr_org_id_example' # str |  (optional)

    try:
        # List First Party Segments
        api_response = api_instance.list_first_party_segments(limit=limit, after=after, x_lr_org_id=x_lr_org_id)
        print("The response of V1Api->list_first_party_segments:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling V1Api->list_first_party_segments: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**|  | [optional] [default to 50]
 **after** | **str**|  | [optional] 
 **x_lr_org_id** | **str**|  | [optional] 

### Return type

[**SegmentListResponse**](SegmentListResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_marketplace_segments**
> MarketplaceSegmentListResponse list_marketplace_segments(limit=limit, country_codes=country_codes, currency_codes=currency_codes, identifier_type=identifier_type, x_lr_org_id=x_lr_org_id)

List Marketplace Segments

### Example


```python
import pulsepoint_liveramp
from pulsepoint_liveramp.models.country_code import CountryCode
from pulsepoint_liveramp.models.currency_code import CurrencyCode
from pulsepoint_liveramp.models.identifier_type import IdentifierType
from pulsepoint_liveramp.models.marketplace_segment_list_response import MarketplaceSegmentListResponse
from pulsepoint_liveramp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = pulsepoint_liveramp.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with pulsepoint_liveramp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pulsepoint_liveramp.V1Api(api_client)
    limit = 5 # int | Number of marketplace segments to return (optional) (default to 5)
    country_codes = ["USA"] # List[CountryCode] | Country filter (ISO alpha-3) (optional) (default to ["USA"])
    currency_codes = ["USD"] # List[CurrencyCode] | Currency filter (optional) (default to ["USD"])
    identifier_type = ["COOKIE"] # List[IdentifierType] | Identifier type used for activation (optional) (default to ["COOKIE"])
    x_lr_org_id = 'x_lr_org_id_example' # str |  (optional)

    try:
        # List Marketplace Segments
        api_response = api_instance.list_marketplace_segments(limit=limit, country_codes=country_codes, currency_codes=currency_codes, identifier_type=identifier_type, x_lr_org_id=x_lr_org_id)
        print("The response of V1Api->list_marketplace_segments:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling V1Api->list_marketplace_segments: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| Number of marketplace segments to return | [optional] [default to 5]
 **country_codes** | [**List[CountryCode]**](CountryCode.md)| Country filter (ISO alpha-3) | [optional] [default to [&quot;USA&quot;]]
 **currency_codes** | [**List[CurrencyCode]**](CurrencyCode.md)| Currency filter | [optional] [default to [&quot;USD&quot;]]
 **identifier_type** | [**List[IdentifierType]**](IdentifierType.md)| Identifier type used for activation | [optional] [default to [&quot;COOKIE&quot;]]
 **x_lr_org_id** | **str**|  | [optional] 

### Return type

[**MarketplaceSegmentListResponse**](MarketplaceSegmentListResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **ready_v1_ready_get**
> object ready_v1_ready_get(x_lr_org_id=x_lr_org_id)

Ready

Dependency-aware readiness check.
- Verifies required env/config is present
- Verifies we can fetch a LiveRamp OAuth token
- Verifies LiveRamp API connectivity with a lightweight call

### Example


```python
import pulsepoint_liveramp
from pulsepoint_liveramp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = pulsepoint_liveramp.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with pulsepoint_liveramp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pulsepoint_liveramp.V1Api(api_client)
    x_lr_org_id = 'x_lr_org_id_example' # str |  (optional)

    try:
        # Ready
        api_response = api_instance.ready_v1_ready_get(x_lr_org_id=x_lr_org_id)
        print("The response of V1Api->ready_v1_ready_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling V1Api->ready_v1_ready_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_lr_org_id** | **str**|  | [optional] 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **request_segments**
> RequestedSegmentsResponse request_segments(requested_segments_request, x_lr_org_id=x_lr_org_id)

Request Segments For Activation

### Example


```python
import pulsepoint_liveramp
from pulsepoint_liveramp.models.requested_segments_request import RequestedSegmentsRequest
from pulsepoint_liveramp.models.requested_segments_response import RequestedSegmentsResponse
from pulsepoint_liveramp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = pulsepoint_liveramp.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with pulsepoint_liveramp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pulsepoint_liveramp.V1Api(api_client)
    requested_segments_request = pulsepoint_liveramp.RequestedSegmentsRequest() # RequestedSegmentsRequest | 
    x_lr_org_id = 'x_lr_org_id_example' # str |  (optional)

    try:
        # Request Segments For Activation
        api_response = api_instance.request_segments(requested_segments_request, x_lr_org_id=x_lr_org_id)
        print("The response of V1Api->request_segments:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling V1Api->request_segments: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **requested_segments_request** | [**RequestedSegmentsRequest**](RequestedSegmentsRequest.md)|  | 
 **x_lr_org_id** | **str**|  | [optional] 

### Return type

[**RequestedSegmentsResponse**](RequestedSegmentsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

