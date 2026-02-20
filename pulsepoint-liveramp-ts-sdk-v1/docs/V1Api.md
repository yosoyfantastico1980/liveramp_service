# V1Api

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**deliveriesV1LiverampDeliveriesGet**](V1Api.md#deliveriesv1liverampdeliveriesget) | **GET** /v1/liveramp/deliveries | Deliveries |
| [**healthV1HealthGet**](V1Api.md#healthv1healthget) | **GET** /v1/health | Health |
| [**listDestinationsV1LiverampDestinationsGet**](V1Api.md#listdestinationsv1liverampdestinationsget) | **GET** /v1/liveramp/destinations | List Destinations |
| [**listFirstPartySegmentsV1LiverampSegmentsGet**](V1Api.md#listfirstpartysegmentsv1liverampsegmentsget) | **GET** /v1/liveramp/segments | List First Party Segments |
| [**listMarketplaceSegmentsV1LiverampMarketplaceSegmentsGet**](V1Api.md#listmarketplacesegmentsv1liverampmarketplacesegmentsget) | **GET** /v1/liveramp/marketplace/segments | List Marketplace Segments |
| [**marketplaceSegmentsDetailV1LiverampMarketplaceSegmentsDetailGet**](V1Api.md#marketplacesegmentsdetailv1liverampmarketplacesegmentsdetailget) | **GET** /v1/liveramp/marketplace/segments/detail | Marketplace Segments Detail |
| [**requestSegmentsForActivationV1LiverampRequestedSegmentsPost**](V1Api.md#requestsegmentsforactivationv1liveramprequestedsegmentspost) | **POST** /v1/liveramp/requested-segments | Request Segments For Activation |
| [**segmentStatusesV1LiverampSegmentStatusesGet**](V1Api.md#segmentstatusesv1liverampsegmentstatusesget) | **GET** /v1/liveramp/segment-statuses | Segment Statuses |



## deliveriesV1LiverampDeliveriesGet

> any deliveriesV1LiverampDeliveriesGet(integrationConnectionID, xLROrgId, xPPAPIKey)

Deliveries

### Example

```ts
import {
  Configuration,
  V1Api,
} from '';
import type { DeliveriesV1LiverampDeliveriesGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new V1Api();

  const body = {
    // string
    integrationConnectionID: integrationConnectionID_example,
    // string (optional)
    xLROrgId: xLROrgId_example,
    // string (optional)
    xPPAPIKey: xPPAPIKey_example,
  } satisfies DeliveriesV1LiverampDeliveriesGetRequest;

  try {
    const data = await api.deliveriesV1LiverampDeliveriesGet(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **integrationConnectionID** | `string` |  | [Defaults to `undefined`] |
| **xLROrgId** | `string` |  | [Optional] [Defaults to `undefined`] |
| **xPPAPIKey** | `string` |  | [Optional] [Defaults to `undefined`] |

### Return type

**any**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## healthV1HealthGet

> any healthV1HealthGet(xPPAPIKey)

Health

### Example

```ts
import {
  Configuration,
  V1Api,
} from '';
import type { HealthV1HealthGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new V1Api();

  const body = {
    // string (optional)
    xPPAPIKey: xPPAPIKey_example,
  } satisfies HealthV1HealthGetRequest;

  try {
    const data = await api.healthV1HealthGet(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **xPPAPIKey** | `string` |  | [Optional] [Defaults to `undefined`] |

### Return type

**any**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## listDestinationsV1LiverampDestinationsGet

> any listDestinationsV1LiverampDestinationsGet(limit, xLROrgId, xPPAPIKey)

List Destinations

### Example

```ts
import {
  Configuration,
  V1Api,
} from '';
import type { ListDestinationsV1LiverampDestinationsGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new V1Api();

  const body = {
    // number (optional)
    limit: 56,
    // string (optional)
    xLROrgId: xLROrgId_example,
    // string (optional)
    xPPAPIKey: xPPAPIKey_example,
  } satisfies ListDestinationsV1LiverampDestinationsGetRequest;

  try {
    const data = await api.listDestinationsV1LiverampDestinationsGet(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **limit** | `number` |  | [Optional] [Defaults to `1`] |
| **xLROrgId** | `string` |  | [Optional] [Defaults to `undefined`] |
| **xPPAPIKey** | `string` |  | [Optional] [Defaults to `undefined`] |

### Return type

**any**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## listFirstPartySegmentsV1LiverampSegmentsGet

> any listFirstPartySegmentsV1LiverampSegmentsGet(limit, xLROrgId, xPPAPIKey)

List First Party Segments

### Example

```ts
import {
  Configuration,
  V1Api,
} from '';
import type { ListFirstPartySegmentsV1LiverampSegmentsGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new V1Api();

  const body = {
    // number (optional)
    limit: 56,
    // string (optional)
    xLROrgId: xLROrgId_example,
    // string (optional)
    xPPAPIKey: xPPAPIKey_example,
  } satisfies ListFirstPartySegmentsV1LiverampSegmentsGetRequest;

  try {
    const data = await api.listFirstPartySegmentsV1LiverampSegmentsGet(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **limit** | `number` |  | [Optional] [Defaults to `50`] |
| **xLROrgId** | `string` |  | [Optional] [Defaults to `undefined`] |
| **xPPAPIKey** | `string` |  | [Optional] [Defaults to `undefined`] |

### Return type

**any**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## listMarketplaceSegmentsV1LiverampMarketplaceSegmentsGet

> any listMarketplaceSegmentsV1LiverampMarketplaceSegmentsGet(limit, countryCodes, currencyCodes, identifierType, xLROrgId, xPPAPIKey)

List Marketplace Segments

### Example

```ts
import {
  Configuration,
  V1Api,
} from '';
import type { ListMarketplaceSegmentsV1LiverampMarketplaceSegmentsGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new V1Api();

  const body = {
    // number (optional)
    limit: 56,
    // Array<string> (optional)
    countryCodes: ...,
    // Array<string> (optional)
    currencyCodes: ...,
    // Array<string> (optional)
    identifierType: ...,
    // string (optional)
    xLROrgId: xLROrgId_example,
    // string (optional)
    xPPAPIKey: xPPAPIKey_example,
  } satisfies ListMarketplaceSegmentsV1LiverampMarketplaceSegmentsGetRequest;

  try {
    const data = await api.listMarketplaceSegmentsV1LiverampMarketplaceSegmentsGet(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **limit** | `number` |  | [Optional] [Defaults to `5`] |
| **countryCodes** | `Array<string>` |  | [Optional] |
| **currencyCodes** | `Array<string>` |  | [Optional] |
| **identifierType** | `Array<string>` |  | [Optional] |
| **xLROrgId** | `string` |  | [Optional] [Defaults to `undefined`] |
| **xPPAPIKey** | `string` |  | [Optional] [Defaults to `undefined`] |

### Return type

**any**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## marketplaceSegmentsDetailV1LiverampMarketplaceSegmentsDetailGet

> any marketplaceSegmentsDetailV1LiverampMarketplaceSegmentsDetailGet(ids, limit, xLROrgId, xPPAPIKey)

Marketplace Segments Detail

### Example

```ts
import {
  Configuration,
  V1Api,
} from '';
import type { MarketplaceSegmentsDetailV1LiverampMarketplaceSegmentsDetailGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new V1Api();

  const body = {
    // Array<number>
    ids: ...,
    // number (optional)
    limit: 56,
    // string (optional)
    xLROrgId: xLROrgId_example,
    // string (optional)
    xPPAPIKey: xPPAPIKey_example,
  } satisfies MarketplaceSegmentsDetailV1LiverampMarketplaceSegmentsDetailGetRequest;

  try {
    const data = await api.marketplaceSegmentsDetailV1LiverampMarketplaceSegmentsDetailGet(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **ids** | `Array<number>` |  | |
| **limit** | `number` |  | [Optional] [Defaults to `10`] |
| **xLROrgId** | `string` |  | [Optional] [Defaults to `undefined`] |
| **xPPAPIKey** | `string` |  | [Optional] [Defaults to `undefined`] |

### Return type

**any**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## requestSegmentsForActivationV1LiverampRequestedSegmentsPost

> any requestSegmentsForActivationV1LiverampRequestedSegmentsPost(requestBody, xLROrgId, xPPAPIKey)

Request Segments For Activation

### Example

```ts
import {
  Configuration,
  V1Api,
} from '';
import type { RequestSegmentsForActivationV1LiverampRequestedSegmentsPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new V1Api();

  const body = {
    // Array<{ [key: string]: any; }>
    requestBody: ...,
    // string (optional)
    xLROrgId: xLROrgId_example,
    // string (optional)
    xPPAPIKey: xPPAPIKey_example,
  } satisfies RequestSegmentsForActivationV1LiverampRequestedSegmentsPostRequest;

  try {
    const data = await api.requestSegmentsForActivationV1LiverampRequestedSegmentsPost(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **requestBody** | `Array<{ [key: string]: any; }>` |  | |
| **xLROrgId** | `string` |  | [Optional] [Defaults to `undefined`] |
| **xPPAPIKey** | `string` |  | [Optional] [Defaults to `undefined`] |

### Return type

**any**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## segmentStatusesV1LiverampSegmentStatusesGet

> any segmentStatusesV1LiverampSegmentStatusesGet(segmentIDs, segmentType, limit, xLROrgId, xPPAPIKey)

Segment Statuses

### Example

```ts
import {
  Configuration,
  V1Api,
} from '';
import type { SegmentStatusesV1LiverampSegmentStatusesGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new V1Api();

  const body = {
    // Array<number>
    segmentIDs: ...,
    // string (optional)
    segmentType: segmentType_example,
    // number (optional)
    limit: 56,
    // string (optional)
    xLROrgId: xLROrgId_example,
    // string (optional)
    xPPAPIKey: xPPAPIKey_example,
  } satisfies SegmentStatusesV1LiverampSegmentStatusesGetRequest;

  try {
    const data = await api.segmentStatusesV1LiverampSegmentStatusesGet(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **segmentIDs** | `Array<number>` |  | |
| **segmentType** | `string` |  | [Optional] [Defaults to `&#39;DATA_MARKETPLACE&#39;`] |
| **limit** | `number` |  | [Optional] [Defaults to `1`] |
| **xLROrgId** | `string` |  | [Optional] [Defaults to `undefined`] |
| **xPPAPIKey** | `string` |  | [Optional] [Defaults to `undefined`] |

### Return type

**any**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

