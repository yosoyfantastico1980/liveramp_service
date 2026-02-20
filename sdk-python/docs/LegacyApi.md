# pulsepoint_liveramp.LegacyApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**deliveries_legacy_liveramp_deliveries_get**](LegacyApi.md#deliveries_legacy_liveramp_deliveries_get) | **GET** /liveramp/deliveries | Deliveries Legacy
[**destinations_legacy_liveramp_destinations_get**](LegacyApi.md#destinations_legacy_liveramp_destinations_get) | **GET** /liveramp/destinations | Destinations Legacy
[**health_legacy_health_get**](LegacyApi.md#health_legacy_health_get) | **GET** /health | Health Legacy
[**marketplace_detail_legacy_liveramp_marketplace_segments_detail_get**](LegacyApi.md#marketplace_detail_legacy_liveramp_marketplace_segments_detail_get) | **GET** /liveramp/marketplace/segments/detail | Marketplace Detail Legacy
[**marketplace_segments_legacy_liveramp_marketplace_segments_get**](LegacyApi.md#marketplace_segments_legacy_liveramp_marketplace_segments_get) | **GET** /liveramp/marketplace/segments | Marketplace Segments Legacy
[**requested_segments_legacy_liveramp_requested_segments_post**](LegacyApi.md#requested_segments_legacy_liveramp_requested_segments_post) | **POST** /liveramp/requested-segments | Requested Segments Legacy
[**segment_statuses_legacy_liveramp_segment_statuses_get**](LegacyApi.md#segment_statuses_legacy_liveramp_segment_statuses_get) | **GET** /liveramp/segment-statuses | Segment Statuses Legacy
[**segments_legacy_liveramp_segments_get**](LegacyApi.md#segments_legacy_liveramp_segments_get) | **GET** /liveramp/segments | Segments Legacy


# **deliveries_legacy_liveramp_deliveries_get**
> object deliveries_legacy_liveramp_deliveries_get(integration_connection_id, x_lr_org_id=x_lr_org_id)

Deliveries Legacy

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
    api_instance = pulsepoint_liveramp.LegacyApi(api_client)
    integration_connection_id = 'integration_connection_id_example' # str | 
    x_lr_org_id = 'x_lr_org_id_example' # str |  (optional)

    try:
        # Deliveries Legacy
        api_response = api_instance.deliveries_legacy_liveramp_deliveries_get(integration_connection_id, x_lr_org_id=x_lr_org_id)
        print("The response of LegacyApi->deliveries_legacy_liveramp_deliveries_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LegacyApi->deliveries_legacy_liveramp_deliveries_get: %s\n" % e)
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

# **destinations_legacy_liveramp_destinations_get**
> object destinations_legacy_liveramp_destinations_get(limit=limit, after=after, x_lr_org_id=x_lr_org_id)

Destinations Legacy

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
    api_instance = pulsepoint_liveramp.LegacyApi(api_client)
    limit = 1 # int |  (optional) (default to 1)
    after = 'after_example' # str |  (optional)
    x_lr_org_id = 'x_lr_org_id_example' # str |  (optional)

    try:
        # Destinations Legacy
        api_response = api_instance.destinations_legacy_liveramp_destinations_get(limit=limit, after=after, x_lr_org_id=x_lr_org_id)
        print("The response of LegacyApi->destinations_legacy_liveramp_destinations_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LegacyApi->destinations_legacy_liveramp_destinations_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**|  | [optional] [default to 1]
 **after** | **str**|  | [optional] 
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

# **health_legacy_health_get**
> object health_legacy_health_get()

Health Legacy

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
    api_instance = pulsepoint_liveramp.LegacyApi(api_client)

    try:
        # Health Legacy
        api_response = api_instance.health_legacy_health_get()
        print("The response of LegacyApi->health_legacy_health_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LegacyApi->health_legacy_health_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **marketplace_detail_legacy_liveramp_marketplace_segments_detail_get**
> object marketplace_detail_legacy_liveramp_marketplace_segments_detail_get(ids, limit=limit, x_lr_org_id=x_lr_org_id)

Marketplace Detail Legacy

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
    api_instance = pulsepoint_liveramp.LegacyApi(api_client)
    ids = [56] # List[int] | 
    limit = 10 # int |  (optional) (default to 10)
    x_lr_org_id = 'x_lr_org_id_example' # str |  (optional)

    try:
        # Marketplace Detail Legacy
        api_response = api_instance.marketplace_detail_legacy_liveramp_marketplace_segments_detail_get(ids, limit=limit, x_lr_org_id=x_lr_org_id)
        print("The response of LegacyApi->marketplace_detail_legacy_liveramp_marketplace_segments_detail_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LegacyApi->marketplace_detail_legacy_liveramp_marketplace_segments_detail_get: %s\n" % e)
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

# **marketplace_segments_legacy_liveramp_marketplace_segments_get**
> object marketplace_segments_legacy_liveramp_marketplace_segments_get(limit=limit, country_codes=country_codes, currency_codes=currency_codes, identifier_type=identifier_type, x_lr_org_id=x_lr_org_id)

Marketplace Segments Legacy

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
    api_instance = pulsepoint_liveramp.LegacyApi(api_client)
    limit = 5 # int |  (optional) (default to 5)
    country_codes = ["USA"] # List[str] |  (optional) (default to ["USA"])
    currency_codes = ["USD"] # List[str] |  (optional) (default to ["USD"])
    identifier_type = ["COOKIE"] # List[str] |  (optional) (default to ["COOKIE"])
    x_lr_org_id = 'x_lr_org_id_example' # str |  (optional)

    try:
        # Marketplace Segments Legacy
        api_response = api_instance.marketplace_segments_legacy_liveramp_marketplace_segments_get(limit=limit, country_codes=country_codes, currency_codes=currency_codes, identifier_type=identifier_type, x_lr_org_id=x_lr_org_id)
        print("The response of LegacyApi->marketplace_segments_legacy_liveramp_marketplace_segments_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LegacyApi->marketplace_segments_legacy_liveramp_marketplace_segments_get: %s\n" % e)
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

# **requested_segments_legacy_liveramp_requested_segments_post**
> object requested_segments_legacy_liveramp_requested_segments_post(request_body, x_lr_org_id=x_lr_org_id)

Requested Segments Legacy

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
    api_instance = pulsepoint_liveramp.LegacyApi(api_client)
    request_body = None # List[Dict[str, object]] | 
    x_lr_org_id = 'x_lr_org_id_example' # str |  (optional)

    try:
        # Requested Segments Legacy
        api_response = api_instance.requested_segments_legacy_liveramp_requested_segments_post(request_body, x_lr_org_id=x_lr_org_id)
        print("The response of LegacyApi->requested_segments_legacy_liveramp_requested_segments_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LegacyApi->requested_segments_legacy_liveramp_requested_segments_post: %s\n" % e)
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

# **segment_statuses_legacy_liveramp_segment_statuses_get**
> object segment_statuses_legacy_liveramp_segment_statuses_get(segment_ids, segment_type=segment_type, limit=limit, x_lr_org_id=x_lr_org_id)

Segment Statuses Legacy

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
    api_instance = pulsepoint_liveramp.LegacyApi(api_client)
    segment_ids = [56] # List[int] | 
    segment_type = 'DATA_MARKETPLACE' # str |  (optional) (default to 'DATA_MARKETPLACE')
    limit = 1 # int |  (optional) (default to 1)
    x_lr_org_id = 'x_lr_org_id_example' # str |  (optional)

    try:
        # Segment Statuses Legacy
        api_response = api_instance.segment_statuses_legacy_liveramp_segment_statuses_get(segment_ids, segment_type=segment_type, limit=limit, x_lr_org_id=x_lr_org_id)
        print("The response of LegacyApi->segment_statuses_legacy_liveramp_segment_statuses_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LegacyApi->segment_statuses_legacy_liveramp_segment_statuses_get: %s\n" % e)
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

# **segments_legacy_liveramp_segments_get**
> object segments_legacy_liveramp_segments_get(limit=limit, after=after, x_lr_org_id=x_lr_org_id)

Segments Legacy

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
    api_instance = pulsepoint_liveramp.LegacyApi(api_client)
    limit = 50 # int |  (optional) (default to 50)
    after = 'after_example' # str |  (optional)
    x_lr_org_id = 'x_lr_org_id_example' # str |  (optional)

    try:
        # Segments Legacy
        api_response = api_instance.segments_legacy_liveramp_segments_get(limit=limit, after=after, x_lr_org_id=x_lr_org_id)
        print("The response of LegacyApi->segments_legacy_liveramp_segments_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LegacyApi->segments_legacy_liveramp_segments_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**|  | [optional] [default to 50]
 **after** | **str**|  | [optional] 
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

