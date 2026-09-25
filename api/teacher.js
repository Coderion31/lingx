// GET /api/teacher?token=... — teacher panel: their class + the students who joined by class code
const { readDb } = require('./_db');

module.exports = async function handler(req, res) {
  try {
    const db = await readDb();
    const token = (req.query && req.query.token) || '';
    const email = findEmail(db, token);
    if (!email) return res.status(401).json({ error: 'Не авторизован' });

    const u = db.users[email];
    if (!u) return res.status(404).json({ error: 'Пользователь не найден' });
    if (u.role !== 'teacher') return res.status(403).json({ error: 'Только для учителей' });

    const cc = u.classCode || '';
    const cls = (db.classes && db.classes[cc]) || null;
    const list = (cls && cls.students) || [];
    const students = list.map(function (e) {
      const s = db.users[e] || {};
      return { email: e, name: s.name || e };
    });

    res.json({ ok: true, classCode: cc, className: (cls && cls.name) || '', teacher: (cls && cls.teacher) || null, students });
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