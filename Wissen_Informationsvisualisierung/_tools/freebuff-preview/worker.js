import { createFreebuffAuth, isSameOriginRequest } from "@freebuff/auth";

import HTML from "./page.html";

const HTML_HEADERS = {
  "content-type": "text/html; charset=utf-8",
  "cache-control": "private, no-store",
  "x-content-type-options": "nosniff",
  "referrer-policy": "no-referrer",
};

const JSON_HEADERS = {
  "content-type": "application/json; charset=utf-8",
  "cache-control": "private, no-store",
};

let authKey = "";
let app = null;
let schemaPromise = null;

function json(value, status = 200) {
  return new Response(JSON.stringify(value), { status, headers: JSON_HEADERS });
}

function isLoopback(origin) {
  return /^http:\/\/(localhost|127\.0\.0\.1|\[::1\])(?::\d+)?$/.test(origin);
}

function setup(env) {
  const key = [env.FREEBUFF_CLIENT_ID, env.FREEBUFF_ISSUER || "", env.APP_ORIGIN].join("|");
  if (key !== authKey) {
    authKey = key;
    const auth = createFreebuffAuth({
      clientId: env.FREEBUFF_CLIENT_ID,
      issuer: env.FREEBUFF_ISSUER || undefined,
      baseUrl: env.APP_ORIGIN,
      allowInsecureLocalhost: isLoopback(env.APP_ORIGIN),
    });
    app = auth.wrap((request, env, ctx) => handle(request, env, ctx, auth));
  }
  return app;
}

function ensureSchema(env) {
  if (!schemaPromise) {
    schemaPromise = env.DB.batch([
      env.DB.prepare(
        "CREATE TABLE IF NOT EXISTS progress (" +
          "user_id TEXT PRIMARY KEY, " +
          "data TEXT NOT NULL, " +
          "updated_at TEXT NOT NULL" +
        ")"
      ),
      env.DB.prepare(
        "CREATE TABLE IF NOT EXISTS settings (" +
          "key TEXT PRIMARY KEY, " +
          "value TEXT NOT NULL" +
        ")"
      ),
    ]).catch((error) => {
      schemaPromise = null;
      throw error;
    });
  }
  return schemaPromise;
}

async function isOwner(env, user) {
  if (env.ALLOWED_SUB) return user.sub === env.ALLOWED_SUB;
  let row = await env.DB.prepare(
    "SELECT value FROM settings WHERE key = 'owner_sub'"
  ).first();
  if (!row) {
    await env.DB.prepare(
      "INSERT OR IGNORE INTO settings (key, value) VALUES ('owner_sub', ?)"
    ).bind(user.sub).run();
    row = await env.DB.prepare(
      "SELECT value FROM settings WHERE key = 'owner_sub'"
    ).first();
  }
  return !!row && row.value === user.sub;
}

async function getProgress(env, user) {
  const row = await env.DB.prepare(
    "SELECT data, updated_at FROM progress WHERE user_id = ?"
  ).bind(user.sub).first();
  let data = null;
  if (row) {
    try {
      data = JSON.parse(row.data);
    } catch (error) {
      data = null;
    }
  }
  return json({
    data,
    updatedAt: row ? row.updated_at : null,
  });
}

async function putProgress(request, env, user) {
  if (!isSameOriginRequest(request, env.APP_ORIGIN)) {
    return json({ error: "Forbidden" }, 403);
  }
  let body;
  try {
    body = await request.json();
  } catch (error) {
    return json({ error: "Invalid JSON" }, 400);
  }
  if (!body || typeof body.data !== "object" || body.data === null || Array.isArray(body.data)) {
    return json({ error: "Invalid progress data" }, 400);
  }
  const data = JSON.stringify(body.data);
  if (data.length > 100000) {
    return json({ error: "Progress data too large" }, 413);
  }
  const updatedAt = new Date().toISOString();
  await env.DB.prepare(
    "INSERT INTO progress (user_id, data, updated_at) VALUES (?, ?, ?) " +
      "ON CONFLICT(user_id) DO UPDATE SET data = excluded.data, updated_at = excluded.updated_at"
  ).bind(user.sub, data, updatedAt).run();
  return json({ ok: true, updatedAt });
}

function forbiddenPage() {
  return new Response(
    '<!doctype html><html lang="de"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' +
      "<title>Nicht freigegeben</title>" +
      '<body style="font-family:system-ui,sans-serif;background:#111318;color:#dcddde;display:grid;place-items:center;min-height:100vh;margin:0">' +
      '<main style="max-width:34rem;padding:2rem;text-align:center">' +
      "<h1>Dieses Konto ist nicht freigegeben</h1>" +
      "<p>Der Lernserver ist für dieses Freebuff-Konto gesperrt. Melde dich mit dem freigegebenen Konto an.</p>" +
      '<form method="post" action="/auth/freebuff/signout"><button type="submit" style="padding:.7rem 1rem;border:1px solid #5865f2;border-radius:.5rem;background:#5865f2;color:white;font:inherit;cursor:pointer">Abmelden</button></form>' +
      "</main></body></html>",
    { status: 403, headers: HTML_HEADERS }
  );
}

async function handle(request, env, ctx, auth) {
  const url = new URL(request.url);

  if (url.pathname === "/healthz") {
    return json({ ok: true, db: !!env.DB });
  }

  if (!env.DB) {
    return new Response("Datenbank nicht konfiguriert.", {
      status: 500,
      headers: { "content-type": "text/plain; charset=utf-8", "cache-control": "no-store" },
    });
  }

  let user;
  try {
    user = await auth.getUser(request);
  } catch (error) {
    // A stale or malformed session must not crash the Worker (502).
    if (url.pathname.startsWith("/api/")) return json({ error: "Sign in required" }, 401);
    const returnTo = url.pathname + url.search;
    return Response.redirect(
      new URL("/auth/freebuff/signin?returnTo=" + encodeURIComponent(returnTo), env.APP_ORIGIN).toString(),
      302
    );
  }

  if (!user) {
    if (url.pathname.startsWith("/api/")) return json({ error: "Sign in required" }, 401);
    const returnTo = url.pathname + url.search;
    return Response.redirect(
      new URL("/auth/freebuff/signin?returnTo=" + encodeURIComponent(returnTo), env.APP_ORIGIN).toString(),
      302
    );
  }

  await ensureSchema(env);

  if (!(await isOwner(env, user))) {
    if (url.pathname.startsWith("/api/")) return json({ error: "Forbidden" }, 403);
    return forbiddenPage();
  }

  if (url.pathname === "/api/me") {
    return json({
      user: {
        name: user.name || "",
        email: user.email || "",
        picture: user.picture || "",
      },
      owner: true,
    });
  }

  if (url.pathname === "/api/progress") {
    if (request.method === "GET") return getProgress(env, user);
    if (request.method === "PUT" || request.method === "POST") {
      return putProgress(request, env, user);
    }
    return json({ error: "Method not allowed" }, 405);
  }

  if (url.pathname === "/" || url.pathname === "/index.html") {
    return new Response(HTML, { headers: HTML_HEADERS });
  }

  return new Response("Nicht gefunden.", {
    status: 404,
    headers: { "content-type": "text/plain; charset=utf-8", "cache-control": "no-store" },
  });
}

export default {
  fetch(request, env, ctx) {
    try {
      return setup(env)(request, env, ctx);
    } catch (error) {
      return new Response("Serverkonfiguration fehlt.", {
        status: 500,
        headers: { "content-type": "text/plain; charset=utf-8", "cache-control": "no-store" },
      });
    }
  },
};
