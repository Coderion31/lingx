// POST /api/register {email, password, name}
const { readDb, writeDb, sanitize } = require('./_db');
const { sendVerification } = require('./_mail');
const crypto = require('crypto');

function sha256(s) { return crypto.createHash('sha256').update(s).digest('hex'); }

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method' });
  try {
    let body = {};
    try { body = typeof req.body === 'string' ? JSON.parse(req.body) : (req.body || {}); } catch (e) {}
    const email = String(body.email || '').trim().toLowerCase();
    const password = String(body.password || '');
    const name = String(body.name || '').trim();
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return res.status(400).json({ error: 'Некорректный email' });
    if (password.length < 6) return res.status(400).json({ error: 'Пароль минимум 6 символов' });

    const db = await readDb();
    if (db.users[email]) return res.status(409).json({ error: 'Email уже зарегистрирован' });

    const code = String(Math.floor(100000 + Math.random()*900000));
    const user = {
      email,
      name: name || email.split('@')[0],
      passwordHash: sha256(password),
      verified: false,
      code,
      codeExpires: Date.now() + 10*60*1000,
      createdAt: new Date().toISOString(),
      lastLogin: null,
      progress: {}
    };
    db.users[email] = user;
    await writeDb(db);

    try { await sendVerification(email, code); }
    catch (e) {
      // mail failed: keep user, allow resend
      delete db.users[email];
      await writeDb(db);
      return res.status(500).json({ error: 'Не удалось отправить письмо. Проверь GMAIL_APP_PASS' });
    }

    res.json({ ok: true, message: 'Код отправлен на почту', email });
  } catch (e) {
    res.status(500).json({ error: 'Server error: ' + e.message });
  }
};