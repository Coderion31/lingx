// POST /api/verify-code {email, code} — verify 6-digit code, login
// GET /api/confirm?email=...&t=... — confirm email link from email
const { readDb, writeDb, sanitize } = require('./_db');
const crypto = require('crypto');

module.exports = async function handler(req, res) {
  // GET = confirm link from email
  if (req.method === 'GET') {
    try {
      const email = String(req.query.email || '').trim().toLowerCase();
      const token = String(req.query.t || '');
      const db = await readDb();
      const user = db.users[email];
      if (!user) return sendConfirmPage(res, false, 'Пользователь не найден');
      if (user.confirmToken !== token || Date.now() > (user.confirmExpires || 0))
        return sendConfirmPage(res, false, 'Ссылка устарела или неверна');

      user.verified = true;
      delete user.confirmToken;
      delete user.confirmExpires;
      const sessionToken = crypto.randomBytes(32).toString('hex');
      user.tokens = user.tokens || {};
      user.tokens[sessionToken] = Date.now() + 30 * 24 * 60 * 60 * 1000;
      user.lastLogin = new Date().toISOString();
      await writeDb(db);

      // Check user-agent for mobile
      const ua = (req.headers['user-agent'] || '').toLowerCase();
      const isMobile = /mobile|android|iphone|ipad/i.test(ua);
      return sendConfirmPage(res, true, 'Email подтверждён!', isMobile);
    } catch (e) {
      return sendConfirmPage(res, false, 'Ошибка: ' + e.message);
    }
  }

  // POST = code verification
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

    // Mark as logged in, but still may need email confirm later
    user.lastLogin = new Date().toISOString();
    const sessionToken = crypto.randomBytes(32).toString('hex');
    user.tokens = user.tokens || {};
    user.tokens[sessionToken] = Date.now() + 30 * 24 * 60 * 60 * 1000;
    // Keep confirmToken: user can still click the link in email later
    await writeDb(db);

    const safe = sanitize(user);
    safe.verified = !!user.verified;
    safe.needsConfirm = !user.verified;

    res.json({ ok: true, token: sessionToken, user: safe });
  } catch (e) {
    res.status(500).json({ error: 'Server error: ' + e.message });
  }
};

function sendConfirmPage(res, ok, message, isMobile) {
  const title = ok ? 'Email подтверждён' : 'Ошибка подтверждения';
  const color = ok ? '#38a169' : '#e53e3e';
  const extra = isMobile ? '<p style="font-size:14px;color:#94a3b8;margin-top:8px">Можешь закрыть эту страницу и вернуться в приложение</p>' : '<p style="font-size:14px;color:#94a3b8;margin-top:8px">Подтверждение выполнено. Вернись в приложение.</p>';
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.end(`<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${title}</title><style>body{font-family:-apple-system,sans-serif;background:#0f172a;color:#e2e8f0;display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0}.card{background:#1e293b;border-radius:16px;padding:32px;max-width:360px;text-align:center;border:1px solid #334155}.icon{font-size:48px;margin-bottom:12px;color:${color}}h2{font-size:20px;margin:0 0 8px}p{font-size:14px;color:#94a3b8;margin:0}</style></head><body><div class="card"><div class="icon">${ok ? '✓' : '✗'}</div><h2>${title}</h2><p>${message}</p>${extra}</div></body></html>`);
}