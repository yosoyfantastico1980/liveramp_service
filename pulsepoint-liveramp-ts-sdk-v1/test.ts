import { Configuration } from "./runtime";
import { V1Api } from "./apis";

const basePath = "http://127.0.0.1:8000";

async function main() {
  const api = new V1Api(new Configuration({ basePath }));

  // v1 health
  const health = await api.healthV1HealthGet();
  console.log("v1 health:", health);

  // v1 destinations
  const dest = await api.listDestinationsV1LiverampDestinationsGet({ limit: 1 });
  console.log("v1 destinations:", JSON.stringify(dest, null, 2));

  // v1 first-party segments
  const segs = await api.listFirstPartySegmentsV1LiverampSegmentsGet({ limit: 50 });
  console.log("v1 first-party segments:", JSON.stringify(segs, null, 2));

  // v1 marketplace segments
  const mkt = await api.listMarketplaceSegmentsV1LiverampMarketplaceSegmentsGet({ limit: 5 });
  console.log("v1 marketplace segments:", JSON.stringify(mkt, null, 2));
}

main().catch((e) => {
  console.error("SDK call failed:", e);
  process.exit(1);
});
