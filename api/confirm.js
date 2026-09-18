// GET /api/confirm?email=...&t=... — confirm email by link (from email)
const { readDb, writeDb } = require('./_db');
const crypto = require('crypto');

module.exports = async function handler(req, res) {
  try {
    const email = String(req.query.email || '').trim().toLowerCase();
    const token = String(req.query.t || '');
    if (!email || !token) return sendPage(res, false, 'Неверная ссылка');

    const db = await readDb();
    const user = db.users[email];
    if (!user) return sendPage(res, false, 'Пользователь не найден');
    if (user.verified) return sendPage(res, true, 'Email уже был подтверждён');
    if (user.confirmToken !== token || Date.now() > (user.confirmExpires || 0))
      return sendPage(res, false, 'Ссылка устарела или неверна. Запроси новую в настройках');

    user.verified = true;
    delete user.confirmToken;
    delete user.confirmExpires;
    await writeDb(db);

    const ua = (req.headers['user-agent'] || '').toLowerCase();
    const isMobile = /mobile|android|iphone|ipad/i.test(ua);
    return sendPage(res, true, 'Email подтверждён!', isMobile);
  } catch (e) {
    return sendPage(res, false, 'Ошибка: ' + e.message);
  }
};

function sendPage(res, ok, message, isMobile) {
  const title = ok ? 'Email подтверждён' : 'Ошибка';
  const color = ok ? '#38a169' : '#e53e3e';
  const extra = isMobile
    ? '<p style="font-size:14px;color:#94a3b8;margin-top:8px">Можно закрыть эту страницу и вернуться в приложение</p>'
    : '<p style="font-size:14px;color:#94a3b8;margin-top:8px">Можно вернуться в приложение. Статус обновится автоматически.</p>';
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.end(`<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${title}</title><style>body{font-family:-apple-system,sans-serif;background:#0f172a;color:#e2e8f0;display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0}.card{background:#1e293b;border-radius:16px;padding:32px;max-width:360px;text-align:center;border:1px solid #334155}.icon{font-size:48px;margin-bottom:12px;color:${color}}h2{font-size:20px;margin:0 0 8px}p{font-size:14px;color:#94a3b8;margin:0}</style></head><body><div class="card"><div class="icon">${ok ? '✓' : '✗'}</div><h2>${title}</h2><p>${message}</p>${extra||''}</div></body></html>`);
}