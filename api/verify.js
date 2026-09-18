// POST /api/verify {email, code} — confirm code, create session token
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
    if (!user) return res.status(404).json({ error: 'Пользователь не найден' });
    if (String(user.code) !== code) return res.status(401).json({ error: 'Неверный код' });
    if (user.codeExpires && Date.now() > user.codeExpires) return res.status(401).json({ error: 'Код истёк' });

    user.verified = true;
    delete user.code;
    delete user.codeExpires;
    user.lastLogin = new Date().toISOString();
    const token = crypto.randomBytes(32).toString('hex');
    user.tokens = user.tokens || {};
    user.tokens[token] = Date.now() + 30*24*60*60*1000; // 30 days
    await writeDb(db);

    res.json({ ok: true, token, user: sanitize(user) });
  } catch (e) {
    res.status(500).json({ error: 'Server error: ' + e.message });
  }
};