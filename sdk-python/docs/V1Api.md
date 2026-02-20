# pulsepoint_liveramp.V1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**deliveries_v1_liveramp_deliveries_get**](V1Api.md#deliveries_v1_liveramp_deliveries_get) | **GET** /v1/liveramp/deliveries | Deliveries
[**health_v1_health_get**](V1Api.md#health_v1_health_get) | **GET** /v1/health | Health
[**list_destinations_v1_liveramp_destinations_get**](V1Api.md#list_destinations_v1_liveramp_destinations_get) | **GET** /v1/liveramp/destinations | List Destinations
[**list_first_party_segments_v1_liveramp_segments_get**](V1Api.md#list_first_party_segments_v1_liveramp_segments_get) | **GET** /v1/liveramp/segments | List First Party Segments
[**list_marketplace_segments_v1_liveramp_marketplace_segments_get**](V1Api.md#list_marketplace_segments_v1_liveramp_marketplace_segments_get) | **GET** /v1/liveramp/marketplace/segments | List Marketplace Segments
[**marketplace_segments_detail_v1_liveramp_marketplace_segments_detail_get**](V1Api.md#marketplace_segments_detail_v1_liveramp_marketplace_segments_detail_get) | **GET** /v1/liveramp/marketplace/segments/detail | Marketplace Segments Detail
[**ready_v1_ready_get**](V1Api.md#ready_v1_ready_get) | **GET** /v1/ready | Ready
[**request_segments_for_activation_v1_liveramp_requested_segments_post**](V1Api.md#request_segments_for_activation_v1_liveramp_requested_segments_post) | **POST** /v1/liveramp/requested-segments | Request Segments For Activation
[**segment_statuses_v1_liveramp_segment_statuses_get**](V1Api.md#segment_statuses_v1_liveramp_segment_statuses_get) | **GET** /v1/liveramp/segment-statuses | Segment Statuses


# **deliveries_v1_liveramp_deliveries_get**
> object deliveries_v1_liveramp_deliveries_get(integration_connection_id, x_lr_org_id=x_lr_org_id)

Deliveries

### Example

* Api Key Authentication (APIKeyHeader):

```python
import pulsepoint_liveramp
from pulsepoint_liveramp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = pulsepoint_liveramp.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: APIKeyHeader
configuration.api_key['APIKeyHeader'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['APIKeyHeader'] = 'Bearer'

# Enter a context with an instance of the API client
with pulsepoint_liveramp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pulsepoint_liveramp.V1Api(api_client)
    integration_connection_id = 'integration_connection_id_example' # str | 
    x_lr_org_id = 'x_lr_org_id_example' # str |  (optional)

    try:
        # Deliveries
        api_response = api_instance.deliveries_v1_liveramp_deliveries_get(integration_connection_id, x_lr_org_id=x_lr_org_id)
        print("The response of V1Api->deliveries_v1_liveramp_deliveries_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling V1Api->deliveries_v1_liveramp_deliveries_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **integration_connection_id** | **str**|  | 
 **x_lr_org_id** | **str**|  | [optional] 

### Return type

**object**

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader)

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

# **list_destinations_v1_liveramp_destinations_get**
> DestinationsResponse list_destinations_v1_liveramp_destinations_get(limit=limit, after=after, x_lr_org_id=x_lr_org_id)

List Destinations

### Example

* Api Key Authentication (APIKeyHeader):

```python
import pulsepoint_liveramp
from pulsepoint_liveramp.models.destinations_response import DestinationsResponse
from pulsepoint_liveramp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = pulsepoint_liveramp.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: APIKeyHeader
configuration.api_key['APIKeyHeader'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['APIKeyHeader'] = 'Bearer'

# Enter a context with an instance of the API client
with pulsepoint_liveramp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pulsepoint_liveramp.V1Api(api_client)
    limit = 1 # int |  (optional) (default to 1)
    after = 'after_example' # str | Pagination cursor from prior response _pagination.after (optional)
    x_lr_org_id = 'x_lr_org_id_example' # str |  (optional)

    try:
        # List Destinations
        api_response = api_instance.list_destinations_v1_liveramp_destinations_get(limit=limit, after=after, x_lr_org_id=x_lr_org_id)
        print("The response of V1Api->list_destinations_v1_liveramp_destinations_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling V1Api->list_destinations_v1_liveramp_destinations_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**|  | [optional] [default to 1]
 **after** | **str**| Pagination cursor from prior response _pagination.after | [optional] 
 **x_lr_org_id** | **str**|  | [optional] 

### Return type

[**DestinationsResponse**](DestinationsResponse.md)

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**502** | Bad Gateway |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_first_party_segments_v1_liveramp_segments_get**
> SegmentsResponse list_first_party_segments_v1_liveramp_segments_get(limit=limit, after=after, x_lr_org_id=x_lr_org_id)

List First Party Segments

### Example

* Api Key Authentication (APIKeyHeader):

```python
import pulsepoint_liveramp
from pulsepoint_liveramp.models.segments_response import SegmentsResponse
from pulsepoint_liveramp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = pulsepoint_liveramp.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: APIKeyHeader
configuration.api_key['APIKeyHeader'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['APIKeyHeader'] = 'Bearer'

# Enter a context with an instance of the API client
with pulsepoint_liveramp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pulsepoint_liveramp.V1Api(api_client)
    limit = 50 # int |  (optional) (default to 50)
    after = 'after_example' # str | Pagination cursor from prior response _pagination.after (optional)
    x_lr_org_id = 'x_lr_org_id_example' # str |  (optional)

    try:
        # List First Party Segments
        api_response = api_instance.list_first_party_segments_v1_liveramp_segments_get(limit=limit, after=after, x_lr_org_id=x_lr_org_id)
        print("The response of V1Api->list_first_party_segments_v1_liveramp_segments_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling V1Api->list_first_party_segments_v1_liveramp_segments_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**|  | [optional] [default to 50]
 **after** | **str**| Pagination cursor from prior response _pagination.after | [optional] 
 **x_lr_org_id** | **str**|  | [optional] 

### Return type

[**SegmentsResponse**](SegmentsResponse.md)

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**502** | Bad Gateway |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_marketplace_segments_v1_liveramp_marketplace_segments_get**
> object list_marketplace_segments_v1_liveramp_marketplace_segments_get(limit=limit, country_codes=country_codes, currency_codes=currency_codes, identifier_type=identifier_type, x_lr_org_id=x_lr_org_id)

List Marketplace Segments

### Example

* Api Key Authentication (APIKeyHeader):

```python
import pulsepoint_liveramp
from pulsepoint_liveramp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = pulsepoint_liveramp.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: APIKeyHeader
configuration.api_key['APIKeyHeader'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['APIKeyHeader'] = 'Bearer'

# Enter a context with an instance of the API client
with pulsepoint_liveramp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pulsepoint_liveramp.V1Api(api_client)
    limit = 5 # int |  (optional) (default to 5)
    country_codes = ["USA"] # List[str] |  (optional) (default to ["USA"])
    currency_codes = ["USD"] # List[str] |  (optional) (default to ["USD"])
    identifier_type = ["COOKIE"] # List[str] |  (optional) (default to ["COOKIE"])
    x_lr_org_id = 'x_lr_org_id_example' # str |  (optional)

    try:
        # List Marketplace Segments
        api_response = api_instance.list_marketplace_segments_v1_liveramp_marketplace_segments_get(limit=limit, country_codes=country_codes, currency_codes=currency_codes, identifier_type=identifier_type, x_lr_org_id=x_lr_org_id)
        print("The response of V1Api->list_marketplace_segments_v1_liveramp_marketplace_segments_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling V1Api->list_marketplace_segments_v1_liveramp_marketplace_segments_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**|  | [optional] [default to 5]
 **country_codes** | [**List[str]**](str.md)|  | [optional] [default to [&quot;USA&quot;]]
 **currency_codes** | [**List[str]**](str.md)|  | [optional] [default to [&quot;USD&quot;]]
 **identifier_type** | [**List[str]**](str.md)|  | [optional] [default to [&quot;COOKIE&quot;]]
 **x_lr_org_id** | **str**|  | [optional] 

### Return type

**object**

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **marketplace_segments_detail_v1_liveramp_marketplace_segments_detail_get**
> object marketplace_segments_detail_v1_liveramp_marketplace_segments_detail_get(ids, limit=limit, x_lr_org_id=x_lr_org_id)

Marketplace Segments Detail

### Example

* Api Key Authentication (APIKeyHeader):

```python
import pulsepoint_liveramp
from pulsepoint_liveramp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = pulsepoint_liveramp.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: APIKeyHeader
configuration.api_key['APIKeyHeader'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['APIKeyHeader'] = 'Bearer'

# Enter a context with an instance of the API client
with pulsepoint_liveramp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pulsepoint_liveramp.V1Api(api_client)
    ids = [56] # List[int] | 
    limit = 10 # int |  (optional) (default to 10)
    x_lr_org_id = 'x_lr_org_id_example' # str |  (optional)

    try:
        # Marketplace Segments Detail
        api_response = api_instance.marketplace_segments_detail_v1_liveramp_marketplace_segments_detail_get(ids, limit=limit, x_lr_org_id=x_lr_org_id)
        print("The response of V1Api->marketplace_segments_detail_v1_liveramp_marketplace_segments_detail_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling V1Api->marketplace_segments_detail_v1_liveramp_marketplace_segments_detail_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ids** | [**List[int]**](int.md)|  | 
 **limit** | **int**|  | [optional] [default to 10]
 **x_lr_org_id** | **str**|  | [optional] 

### Return type

**object**

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader)

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

Dependency-aware readiness check. - Verifies required env/config is present - Verifies we can fetch a LiveRamp OAuth token - Verifies LiveRamp API connectivity with a lightweight call

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

# **request_segments_for_activation_v1_liveramp_requested_segments_post**
> object request_segments_for_activation_v1_liveramp_requested_segments_post(request_body, x_lr_org_id=x_lr_org_id)

Request Segments For Activation

### Example

* Api Key Authentication (APIKeyHeader):

```python
import pulsepoint_liveramp
from pulsepoint_liveramp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = pulsepoint_liveramp.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: APIKeyHeader
configuration.api_key['APIKeyHeader'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['APIKeyHeader'] = 'Bearer'

# Enter a context with an instance of the API client
with pulsepoint_liveramp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pulsepoint_liveramp.V1Api(api_client)
    request_body = None # List[Dict[str, object]] | 
    x_lr_org_id = 'x_lr_org_id_example' # str |  (optional)

    try:
        # Request Segments For Activation
        api_response = api_instance.request_segments_for_activation_v1_liveramp_requested_segments_post(request_body, x_lr_org_id=x_lr_org_id)
        print("The response of V1Api->request_segments_for_activation_v1_liveramp_requested_segments_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling V1Api->request_segments_for_activation_v1_liveramp_requested_segments_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **request_body** | [**List[Dict[str, object]]**](Dict.md)|  | 
 **x_lr_org_id** | **str**|  | [optional] 

### Return type

**object**

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **segment_statuses_v1_liveramp_segment_statuses_get**
> object segment_statuses_v1_liveramp_segment_statuses_get(segment_ids, segment_type=segment_type, limit=limit, x_lr_org_id=x_lr_org_id)

Segment Statuses

### Example

* Api Key Authentication (APIKeyHeader):

```python
import pulsepoint_liveramp
from pulsepoint_liveramp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = pulsepoint_liveramp.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: APIKeyHeader
configuration.api_key['APIKeyHeader'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['APIKeyHeader'] = 'Bearer'

# Enter a context with an instance of the API client
with pulsepoint_liveramp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pulsepoint_liveramp.V1Api(api_client)
    segment_ids = [56] # List[int] | 
    segment_type = 'DATA_MARKETPLACE' # str |  (optional) (default to 'DATA_MARKETPLACE')
    limit = 1 # int |  (optional) (default to 1)
    x_lr_org_id = 'x_lr_org_id_example' # str |  (optional)

    try:
        # Segment Statuses
        api_response = api_instance.segment_statuses_v1_liveramp_segment_statuses_get(segment_ids, segment_type=segment_type, limit=limit, x_lr_org_id=x_lr_org_id)
        print("The response of V1Api->segment_statuses_v1_liveramp_segment_statuses_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling V1Api->segment_statuses_v1_liveramp_segment_statuses_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **segment_ids** | [**List[int]**](int.md)|  | 
 **segment_type** | **str**|  | [optional] [default to &#39;DATA_MARKETPLACE&#39;]
 **limit** | **int**|  | [optional] [default to 1]
 **x_lr_org_id** | **str**|  | [optional] 

### Return type

**object**

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

