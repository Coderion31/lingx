// POST /api/verify-code {email, code} — verify login code, create session
const { readDb, writeDb, sanitize } = require('./_db');
const crypto = require('crypto');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method' });
  try {
    let body = {};
    try { body = typeof req.body === 'string' ? JSON.parse(req.body) : (req.body || {}); } catch (e) {}
    const email = String(body.email || '').trim().toLowerCase();
    const code = String(body.code || '').trim();
    const db = await readDb();
    const user = db.users[email];
    if (!user) return res.status(404).json({ error: 'Сначала запроси код' });
    if (String(user.code) !== code) return res.status(401).json({ error: 'Неверный код' });
    if (Date.now() > (user.codeExpires || 0)) return res.status(401).json({ error: 'Код истёк. Запроси новый' });

    // code is single-use
    delete user.code;
    delete user.codeExpires;

    user.lastLogin = new Date().toISOString();
    const sessionToken = crypto.randomBytes(32).toString('hex');
    user.tokens = user.tokens || {};
    user.tokens[sessionToken] = Date.now() + 30 * 24 * 60 * 60 * 1000;
    await writeDb(db);

    const safe = sanitize(user);
    safe.verified = !!user.verified;
    safe.needsConfirm = !user.verified;

    res.json({ ok: true, token: sessionToken, user: safe });
  } catch (e) {
    res.status(500).json({ error: 'Server error: ' + e.message });
  }
};