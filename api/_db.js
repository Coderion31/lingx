// GitHub-backed JSON database with memory cache.
// Reads/writes data/users.json in the repo via GitHub API.
const https = require('https');

let cache = null;
let cacheTime = 0;
const CACHE_TTL = 3000; // 3s

function ghRequest(method, path, body) {
  return new Promise((resolve, reject) => {
    const token = process.env.GH_TOKEN;
    const repo = process.env.GH_REPO || 'Coderion31/lingx';
    const branch = process.env.GH_DB_BRANCH || 'master';
    const data = JSON.stringify(body || {});
    const isGet = method === 'GET';
    const options = {
      hostname: 'api.github.com',
      path: `/repos/${repo}/contents/${path}?ref=${branch}`,
      method: isGet ? 'GET' : method,
      headers: {
        'User-Agent': 'lingx',
        'Accept': 'application/vnd.github+json',
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    };
    if (!isGet) options.headers['Content-Length'] = Buffer.byteLength(data);
    const req = https.request(options, (res) => {
      let chunks = '';
      res.on('data', (c) => chunks += c);
      res.on('end', () => {
        try { resolve(JSON.parse(chunks)); }
        catch (e) { reject(new Error('GitHub bad response')); }
      });
    });
    req.on('error', reject);
    if (!isGet) req.write(data);
    req.end();
  });
}

async function readDb() {
  const now = Date.now();
  if (cache && now - cacheTime < CACHE_TTL) return cache;
  const res = await ghRequest('GET', process.env.GH_DB_PATH || 'data/users.json');
  if (res.content) {
    const raw = Buffer.from(res.content, 'base64').toString('utf8');
    try { cache = JSON.parse(raw); } catch (e) { cache = { users: {} }; }
  } else {
    cache = { users: {} };
  }
  cacheTime = now;
  return cache;
}

async function writeDb(db) {
  cache = db;
  cacheTime = Date.now();
  const path = process.env.GH_DB_PATH || 'data/users.json';
  const branch = process.env.GH_DB_BRANCH || 'master';
  const repo = process.env.GH_REPO || 'Coderion31/lingx';
  const content = Buffer.from(JSON.stringify(db, null, 2)).toString('base64');
  const existing = await ghRequest('GET', path);
  const sha = existing.sha;
  const res = await ghRequest('PUT', path, {
    message: `db update ${new Date().toISOString()}`,
    content,
    sha,
    branch
  });
  if (!res.content && !res.commit) throw new Error('DB write failed');
  return db;
}

function sanitize(u) {
  if (!u) return null;
  return {
    email: u.email,
    name: u.name,
    verified: !!u.verified,
    createdAt: u.createdAt,
    lastLogin: u.lastLogin
  };
}

module.exports = { readDb, writeDb, sanitize };