// POST /api/login {email, password} — password login (no code needed if verified)
const { readDb, writeDb, sanitize } = require('./_db');
const crypto = require('crypto');
function sha256(s) { return crypto.createHash('sha256').update(s).digest('hex'); }

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method' });
  try {
    let body = {};
    try { body = typeof req.body === 'string' ? JSON.parse(req.body) : (req.body || {}); } catch (e) {}
    const email = String(body.email || '').trim().toLowerCase();
    const password = String(body.password || '');
    const db = await readDb();
    const user = db.users[email];
    if (!user) return res.status(404).json({ error: 'Пользователь не найден. Зарегистрируйся' });
    if (user.passwordHash !== sha256(password)) return res.status(401).json({ error: 'Неверный пароль' });
    if (!user.verified) {
      return res.status(403).json({ needCode: true, error: 'Подтверди email' });
    }
    user.lastLogin = new Date().toISOString();
    const token = crypto.randomBytes(32).toString('hex');
    user.tokens = user.tokens || {};
    user.tokens[token] = Date.now() + 30*24*60*60*1000;
    await writeDb(db);
    res.json({ ok: true, token, user: sanitize(user) });
  } catch (e) {
    res.status(500).json({ error: 'Server error: ' + e.message });
  }
};