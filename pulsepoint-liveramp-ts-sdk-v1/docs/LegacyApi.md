# LegacyApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**deliveriesLegacyLiverampDeliveriesGet**](LegacyApi.md#deliverieslegacyliverampdeliveriesget) | **GET** /liveramp/deliveries | Deliveries Legacy |
| [**destinationsLegacyLiverampDestinationsGet**](LegacyApi.md#destinationslegacyliverampdestinationsget) | **GET** /liveramp/destinations | Destinations Legacy |
| [**healthLegacyHealthGet**](LegacyApi.md#healthlegacyhealthget) | **GET** /health | Health Legacy |
| [**marketplaceDetailLegacyLiverampMarketplaceSegmentsDetailGet**](LegacyApi.md#marketplacedetaillegacyliverampmarketplacesegmentsdetailget) | **GET** /liveramp/marketplace/segments/detail | Marketplace Detail Legacy |
| [**marketplaceSegmentsLegacyLiverampMarketplaceSegmentsGet**](LegacyApi.md#marketplacesegmentslegacyliverampmarketplacesegmentsget) | **GET** /liveramp/marketplace/segments | Marketplace Segments Legacy |
| [**requestedSegmentsLegacyLiverampRequestedSegmentsPost**](LegacyApi.md#requestedsegmentslegacyliveramprequestedsegmentspost) | **POST** /liveramp/requested-segments | Requested Segments Legacy |
| [**segmentStatusesLegacyLiverampSegmentStatusesGet**](LegacyApi.md#segmentstatuseslegacyliverampsegmentstatusesget) | **GET** /liveramp/segment-statuses | Segment Statuses Legacy |
| [**segmentsLegacyLiverampSegmentsGet**](LegacyApi.md#segmentslegacyliverampsegmentsget) | **GET** /liveramp/segments | Segments Legacy |



## deliveriesLegacyLiverampDeliveriesGet

> any deliveriesLegacyLiverampDeliveriesGet(integrationConnectionID, xLROrgId, xPPAPIKey)

Deliveries Legacy

### Example

```ts
import {
  Configuration,
  LegacyApi,
} from '';
import type { DeliveriesLegacyLiverampDeliveriesGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new LegacyApi();

  const body = {
    // string
    integrationConnectionID: integrationConnectionID_example,
    // string (optional)
    xLROrgId: xLROrgId_example,
    // string (optional)
    xPPAPIKey: xPPAPIKey_example,
  } satisfies DeliveriesLegacyLiverampDeliveriesGetRequest;

  try {
    const data = await api.deliveriesLegacyLiverampDeliveriesGet(body);
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


## destinationsLegacyLiverampDestinationsGet

> any destinationsLegacyLiverampDestinationsGet(limit, xLROrgId, xPPAPIKey)

Destinations Legacy

### Example

```ts
import {
  Configuration,
  LegacyApi,
} from '';
import type { DestinationsLegacyLiverampDestinationsGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new LegacyApi();

  const body = {
    // number (optional)
    limit: 56,
    // string (optional)
    xLROrgId: xLROrgId_example,
    // string (optional)
    xPPAPIKey: xPPAPIKey_example,
  } satisfies DestinationsLegacyLiverampDestinationsGetRequest;

  try {
    const data = await api.destinationsLegacyLiverampDestinationsGet(body);
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


## healthLegacyHealthGet

> any healthLegacyHealthGet(xPPAPIKey)

Health Legacy

### Example

```ts
import {
  Configuration,
  LegacyApi,
} from '';
import type { HealthLegacyHealthGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new LegacyApi();

  const body = {
    // string (optional)
    xPPAPIKey: xPPAPIKey_example,
  } satisfies HealthLegacyHealthGetRequest;

  try {
    const data = await api.healthLegacyHealthGet(body);
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


## marketplaceDetailLegacyLiverampMarketplaceSegmentsDetailGet

> any marketplaceDetailLegacyLiverampMarketplaceSegmentsDetailGet(ids, limit, xLROrgId, xPPAPIKey)

Marketplace Detail Legacy

### Example

```ts
import {
  Configuration,
  LegacyApi,
} from '';
import type { MarketplaceDetailLegacyLiverampMarketplaceSegmentsDetailGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new LegacyApi();

  const body = {
    // Array<number>
    ids: ...,
    // number (optional)
    limit: 56,
    // string (optional)
    xLROrgId: xLROrgId_example,
    // string (optional)
    xPPAPIKey: xPPAPIKey_example,
  } satisfies MarketplaceDetailLegacyLiverampMarketplaceSegmentsDetailGetRequest;

  try {
    const data = await api.marketplaceDetailLegacyLiverampMarketplaceSegmentsDetailGet(body);
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


## marketplaceSegmentsLegacyLiverampMarketplaceSegmentsGet

> any marketplaceSegmentsLegacyLiverampMarketplaceSegmentsGet(limit, countryCodes, currencyCodes, identifierType, xLROrgId, xPPAPIKey)

Marketplace Segments Legacy

### Example

```ts
import {
  Configuration,
  LegacyApi,
} from '';
import type { MarketplaceSegmentsLegacyLiverampMarketplaceSegmentsGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new LegacyApi();

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
  } satisfies MarketplaceSegmentsLegacyLiverampMarketplaceSegmentsGetRequest;

  try {
    const data = await api.marketplaceSegmentsLegacyLiverampMarketplaceSegmentsGet(body);
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


## requestedSegmentsLegacyLiverampRequestedSegmentsPost

> any requestedSegmentsLegacyLiverampRequestedSegmentsPost(requestBody, xLROrgId, xPPAPIKey)

Requested Segments Legacy

### Example

```ts
import {
  Configuration,
  LegacyApi,
} from '';
import type { RequestedSegmentsLegacyLiverampRequestedSegmentsPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new LegacyApi();

  const body = {
    // Array<{ [key: string]: any; }>
    requestBody: ...,
    // string (optional)
    xLROrgId: xLROrgId_example,
    // string (optional)
    xPPAPIKey: xPPAPIKey_example,
  } satisfies RequestedSegmentsLegacyLiverampRequestedSegmentsPostRequest;

  try {
    const data = await api.requestedSegmentsLegacyLiverampRequestedSegmentsPost(body);
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


## segmentStatusesLegacyLiverampSegmentStatusesGet

> any segmentStatusesLegacyLiverampSegmentStatusesGet(segmentIDs, segmentType, limit, xLROrgId, xPPAPIKey)

Segment Statuses Legacy

### Example

```ts
import {
  Configuration,
  LegacyApi,
} from '';
import type { SegmentStatusesLegacyLiverampSegmentStatusesGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new LegacyApi();

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
  } satisfies SegmentStatusesLegacyLiverampSegmentStatusesGetRequest;

  try {
    const data = await api.segmentStatusesLegacyLiverampSegmentStatusesGet(body);
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


## segmentsLegacyLiverampSegmentsGet

> any segmentsLegacyLiverampSegmentsGet(limit, xLROrgId, xPPAPIKey)

Segments Legacy

### Example

```ts
import {
  Configuration,
  LegacyApi,
} from '';
import type { SegmentsLegacyLiverampSegmentsGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new LegacyApi();

  const body = {
    // number (optional)
    limit: 56,
    // string (optional)
    xLROrgId: xLROrgId_example,
    // string (optional)
    xPPAPIKey: xPPAPIKey_example,
  } satisfies SegmentsLegacyLiverampSegmentsGetRequest;

  try {
    const data = await api.segmentsLegacyLiverampSegmentsGet(body);
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

