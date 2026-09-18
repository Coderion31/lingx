// POST /api/send-code {email}
// Creates/updates pending user, sends 6-digit code + confirmation link.
const { readDb, writeDb } = require('./_db');
const { sendVerification } = require('./_mail');
const crypto = require('crypto');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method' });
  try {
    let body = {};
    try { body = typeof req.body === 'string' ? JSON.parse(req.body) : (req.body || {}); } catch (e) {}
    const email = String(body.email || '').trim().toLowerCase();
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return res.status(400).json({ error: 'Некорректный email' });

    const db = await readDb();
    db.users = db.users || {};
    const now = Date.now();
    const code = String(Math.floor(100000 + Math.random() * 900000));
    const confirmToken = crypto.randomBytes(24).toString('hex');

    const existing = db.users[email];
    const user = existing || {
      email,
      name: email.split('@')[0],
      verified: false,
      createdAt: new Date().toISOString(),
      progress: {}
    };
    user.code = code;
    user.codeExpires = now + 10 * 60 * 1000;
    user.confirmToken = confirmToken;
    user.confirmExpires = now + 24 * 60 * 60 * 1000;
    db.users[email] = user;
    await writeDb(db);

    // Build confirm link based on request host (works on Vercel + local)
    const host = req.headers['x-forwarded-host'] || req.headers['host'] || 'lingx.vercel.app';
    const link = `${req.headers['x-forwarded-proto'] === 'https' ? 'https' : 'https'}://${host}/api/confirm?email=${encodeURIComponent(email)}&t=${confirmToken}`;

    try {
      await sendVerification(email, code, link);
    } catch (e) {
      delete db.users[email];
      await writeDb(db);
      return res.status(500).json({ error: 'Не удалось отправить письмо. Проверь SMTP-настройки' });
    }

    const isNew = !existing;
    res.json({ ok: true, message: 'Код отправлен на почту', email, isNew });
  } catch (e) {
    res.status(500).json({ error: 'Server error: ' + e.message });
  }
};