// POST /api/send-confirm {email, token}
// Creates confirm token and sends ONLY the confirmation link email.
const { readDb, writeDb } = require('./_db');
const { sendConfirmLink } = require('./_mail');
const crypto = require('crypto');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method' });
  try {
    let body = {};
    try { body = typeof req.body === 'string' ? JSON.parse(req.body) : (req.body || {}); } catch (e) {}
    const email = String(body.email || '').trim().toLowerCase();
    const token = String(body.token || ''); // auth token for security
    if (!email || !token) return res.status(400).json({ error: 'Нет данных' });

    const db = await readDb();
    const user = db.users[email];
    if (!user) return res.status(404).json({ error: 'Пользователь не найден' });

    // validate session token
    const ok = user.tokens && user.tokens[token] && user.tokens[token] > Date.now();
    if (!ok) return res.status(401).json({ error: 'Не авторизован' });
    if (user.verified) return res.status(400).json({ error: 'Email уже подтверждён' });

    const confirmToken = crypto.randomBytes(24).toString('hex');
    user.confirmToken = confirmToken;
    user.confirmExpires = Date.now() + 24 * 60 * 60 * 1000;
    await writeDb(db);

    const host = req.headers['x-forwarded-host'] || req.headers['host'] || 'lingx.vercel.app';
    const link = `https://${host}/api/confirm?email=${encodeURIComponent(email)}&t=${confirmToken}`;

    try {
      await sendConfirmLink(email, link);
    } catch (e) {
      return res.status(500).json({ error: 'Не удалось отправить письмо' });
    }

    res.json({ ok: true, message: 'Ссылка отправлена на почту' });
  } catch (e) {
    res.status(500).json({ error: 'Server error: ' + e.message });
  }
};