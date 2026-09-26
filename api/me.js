// GET /api/me?token=... — validate token, return user + progress
// POST /api/me {token, progress} — save progress
const { readDb, sanitize } = require('./_db');

module.exports = async function handler(req, res) {
  try {
    const db = await readDb();
    const method = req.method;
    if (method === 'GET') {
      const token = (req.query && req.query.token) || '';
      const email = findEmail(db, token);
      if (!email) return res.status(401).json({ error: 'Не авторизован' });
      const user = db.users[email];
      const safe = sanitize(user);
      safe.progress = user.progress || {};
      return res.json({ ok: true, user: safe });
    }
    if (method === 'POST') {
      let body = {};
      try { body = typeof req.body === 'string' ? JSON.parse(req.body) : (req.body || {}); } catch (e) {}
      const token = body.token || '';
      const email = findEmail(db, token);
      if (!email) return res.status(401).json({ error: 'Не авторизован' });
      const user = db.users[email];
      var np = body.progress || {};user.progress = user.progress || {};for(var k in np){user.progress[k]=np[k];}
      const { writeDb } = require('./_db');
      await writeDb(db);
      const safe = sanitize(user);
      safe.progress = user.progress;
      return res.json({ ok: true, user: safe });
    }
    res.status(405).json({ error: 'Method' });
  } catch (e) {
    res.status(500).json({ error: 'Server error: ' + e.message });
  }
};

function findEmail(db, token) {
  if (!token || !db.users) return null;
  const now = Date.now();
  for (const email in db.users) {
    const u = db.users[email];
    const exp = u.tokens && u.tokens[token];
    if (exp && exp > now) return email;
  }
  return null;
}