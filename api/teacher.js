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
    const TOTALS = { sbj_algebra: 4, sbj_stats: 2, sbj_geometry: 2, sbj_russian: 2, sbj_lit: 2, sbj_physics: 2, sbj_bio: 2, sbj_geo: 2, sbj_history: 2, sbj_english: 2, sbj_python: 42, sbj_cpp: 18, sbj_go: 17, sbj_c: 11, sbj_csharp: 11, sbj_rust: 12 };
    const grandTotal = Object.keys(TOTALS).reduce(function (a, k) { return a + TOTALS[k]; }, 0);
    const students = list.map(function (e) {
      const s = db.users[e] || {};
      const pr = s.progress || {};
      let done = 0;
      Object.keys(pr).forEach(function (sk) {
        const pobj = pr[sk];
        if (pobj && typeof pobj === 'object') { Object.keys(pobj).forEach(function (t) { if (pobj[t]) done++; }); }
      });
      const pct = grandTotal ? Math.round(done / grandTotal * 100) : 0;
      return { email: e, name: s.name || e, done: done, total: grandTotal, pct: pct, progress: pr, registered: s.createdAt || null, lastLogin: s.lastLogin || null };
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