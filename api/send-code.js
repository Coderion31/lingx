// POST /api/send-code {email}
// Sends only the 6-digit login code. No confirm link in this email.
const { readDb, writeDb } = require('./_db');
const { sendLoginCode } = require('./_mail');

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
    db.users[email] = user;
    await writeDb(db);

    try {
      await sendLoginCode(email, code);
    } catch (e) {
      delete db.users[email];
      await writeDb(db);
      return res.status(500).json({ error: 'Не удалось отправить письмо. Проверь SMTP-настройки' });
    }

    res.json({ ok: true, message: 'Код отправлен на почту', email, isNew: !existing });
  } catch (e) {
    res.status(500).json({ error: 'Server error: ' + e.message });
  }
};