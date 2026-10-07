// Cloudflare Pages Function: GET /api/recenzije
// Reads rating and up to 5 reviews from Google Places API (New) and caches the answer for 12 hours,
// so the site stays well inside the free monthly quota. Needs two environment variables in Pages:
//   GOOGLE_PLACES_KEY  API key restricted to Places API (New)
//   GOOGLE_PLACE_ID    the place id of "Lidija Torte i Kolači"
const TTL = 12 * 60 * 60;

export async function onRequestGet({ request, env, waitUntil }) {
  const cache = caches.default;
  const key = new Request(new URL('/api/recenzije', request.url).toString());
  const hit = await cache.match(key);
  if (hit) return hit;

  if (!env.GOOGLE_PLACES_KEY || !env.GOOGLE_PLACE_ID) return json({ error: 'not-configured' }, 503, 60);

  const r = await fetch(`https://places.googleapis.com/v1/places/${encodeURIComponent(env.GOOGLE_PLACE_ID)}?languageCode=sr`, {
    headers: { 'X-Goog-Api-Key': env.GOOGLE_PLACES_KEY, 'X-Goog-FieldMask': 'id,rating,userRatingCount,googleMapsUri,reviews' },
  });
  if (!r.ok) return json({ error: 'upstream', status: r.status }, 502, 300);
  const p = await r.json();

  // Reviews are passed through unchanged and in Google's order; nothing is filtered or edited.
  const res = json({
    id: p.id,
    rating: p.rating,
    count: p.userRatingCount,
    url: p.googleMapsUri,
    fetchedAt: new Date().toISOString(),
    reviews: (p.reviews || []).map((v) => ({
      author: v.authorAttribution?.displayName,
      authorUrl: v.authorAttribution?.uri,
      rating: v.rating,
      when: v.relativePublishTimeDescription,
      text: v.text?.text || v.originalText?.text || '',
      url: v.googleMapsUri,
    })),
  }, 200, TTL);
  waitUntil(cache.put(key, res.clone()));
  return res;
}

function json(data, status, maxAge) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': `public, max-age=${maxAge}` },
  });
}
