// GET /api/visits -> {"visits": N}
// Whole-site visit count from Cloudflare Web Analytics, which every page
// already reports to through the approved beacon. No cookies, nothing per
// person, and nothing about the caller is stored or sent anywhere.
// Needs the Netlify env var CF_API_TOKEN or token1 (Account Analytics: Read), scoped to Functions, with a Production value.
//
// Cloudflare keeps about 6 months of Web Analytics, so visits before CUTOFF are
// frozen into BASELINE. Before CUTOFF is ~5 months old (around April 2027),
// move CUTOFF forward and add those months to BASELINE. scripts/cf-analytics.py gives the numbers.
const ACCOUNT = "28e452b024f049d90e3f4550d1881f6c";
const SITE_TAG = "ff30421a26984c98853ad4ed96b293c4";
const BASELINE = 750;          // visits 2026-08-14 .. 2026-10-31
const CUTOFF = "2026-11-01";

const QUERY = `query($a:String!,$f:AccountRumPageloadEventsAdaptiveGroupsFilter_InputObject){
  viewer{accounts(filter:{accountTag:$a}){t:rumPageloadEventsAdaptiveGroups(limit:1,filter:$f){sum{visits}}}}}`;

export default async () => {
  // the key may be saved as CF_API_TOKEN or token1 (the owner saved it as CF_API_TOKEN1 on 2026-11-21)
  const token = (Netlify.env.get("CF_API_TOKEN") || Netlify.env.get("CF_API_TOKEN1") || Netlify.env.get("token1") || "").trim();
  if (!token) return Response.json({ error: "not configured" }, { status: 503 });
  const today = new Date().toISOString().slice(0, 10);
  try {
    const res = await fetch("https://api.cloudflare.com/client/v4/graphql", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify({
        query: QUERY,
        variables: { a: ACCOUNT, f: { siteTag: SITE_TAG, date_geq: CUTOFF, date_leq: today } },
      }),
    });
    const data = await res.json();
    const recent = data?.data?.viewer?.accounts?.[0]?.t?.[0]?.sum?.visits;
    if (typeof recent !== "number") throw new Error(JSON.stringify(data?.errors ?? data).slice(0, 300));
    return Response.json({ visits: BASELINE + recent }, {
      headers: {
        "Cache-Control": "public, max-age=300",
        "Netlify-CDN-Cache-Control": "public, durable, s-maxage=900, stale-while-revalidate=86400",
      },
    });
  } catch (err) {
    console.error("visits:", err.message);
    return Response.json({ error: "unavailable" }, { status: 502, headers: { "Cache-Control": "no-store" } });
  }
};

export const config = { path: "/api/visits", method: "GET" };
