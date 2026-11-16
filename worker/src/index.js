const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization"
};

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (request.method === "OPTIONS") return new Response(null, { headers: cors });
    if (request.method !== "POST") return json({ error: "Use POST /generate or POST /edit" }, 405);
    try {
      const body = await request.json();
      if (typeof body.prompt !== "string" || !body.prompt.trim()) return json({ error: "A prompt is required" }, 400);
      if (url.pathname === "/generate") {
        if (!env.AI) return json({ error: "Cloudflare Workers AI binding is not configured." }, 503);
        const image = await env.AI.run("@cf/black-forest-labs/flux-1-schnell", { prompt: body.prompt.trim() });
        const bytes = image instanceof ArrayBuffer ? image : image?.image ? Uint8Array.from(atob(image.image), c => c.charCodeAt(0)) : null;
        if (!bytes) return json({ error: "Unexpected model response format." }, 502);
        return new Response(bytes, { headers: { ...cors, "Content-Type": "image/png", "Cache-Control": "no-store" } });
      }
      if (url.pathname === "/edit") {
        if (!env.IMAGE_EDIT_URL || !env.IMAGE_EDIT_TOKEN) return json({ error: "Image-to-image provider is not configured. Set IMAGE_EDIT_URL and IMAGE_EDIT_TOKEN secrets to a compatible editing API." }, 503);
        if (typeof body.image_base64 !== "string") return json({ error: "image_base64 is required" }, 400);
        const upstream = await fetch(env.IMAGE_EDIT_URL, {
          method: "POST",
          headers: { "Authorization": `Bearer ${env.IMAGE_EDIT_TOKEN}`, "Content-Type": "application/json" },
          body: JSON.stringify({ prompt: body.prompt, image_base64: body.image_base64 })
        });
        if (!upstream.ok) return json({ error: `Image provider returned HTTP ${upstream.status}` }, 502);
        return new Response(await upstream.arrayBuffer(), { headers: { ...cors, "Content-Type": upstream.headers.get("Content-Type") || "image/png", "Cache-Control": "no-store" } });
      }
      return json({ error: "Unknown endpoint" }, 404);
    } catch (error) {
      return json({ error: error.message || "Unexpected server error" }, 500);
    }
  }
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data), { status, headers: { ...cors, "Content-Type": "application/json" } });
}
