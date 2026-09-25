// POST /api/admin {token, action:'issue', role, email, code}
// Only the owner (bunseriy@gmail.com) can use this.
// Admin issues a registration/class code for a user:
//   role teacher  -> creates/reserves a unique teacher code (and class) for that email
//   role student  -> attaches the email to the class with the given class code
//   role personal -> just marks the role, no class
const { readDb, writeDb } = require('./_db');

const ADMIN = 'bunseriy@gmail.com';

module.exports = async function handler(req, res) {
  try {
    if (req.method !== 'POST') return res.status(405).json({ error: 'Method' });
    let body = {};
    try { body = typeof req.body === 'string' ? JSON.parse(req.body) : (req.body || {}); } catch (e) {}

    const token = String(body.token || '').trim();
    const db = await readDb();
    const adminEmail = findEmail(db, token);
    if (!adminEmail) return res.status(401).json({ error: 'Не авторизован' });
    if (adminEmail !== ADMIN) return res.status(403).json({ error: 'Нет прав администратора' });

    const action = String(body.action || '').trim();
    if (action !== 'issue') return res.status(400).json({ error: 'Неизвестное действие' });

    const role = String(body.role || '').trim().toLowerCase();
    const target = String(body.email || '').trim().toLowerCase();
    let code = String(body.code || '').trim().toUpperCase();

    if (!['teacher', 'student', 'personal'].includes(role)) return res.status(400).json({ error: 'Неизвестная роль' });
    if (role !== 'personal' && !target) return res.status(400).json({ error: 'Введи email пользователя' });
    if (target && !/^\S+@\S+\.\S+$/.test(target)) return res.status(400).json({ error: 'Некорректный email' });

    db.teacherCodes = db.teacherCodes || {};
    db.classes = db.classes || {};

    const gen = function () {
      let c;
      do { c = Math.random().toString(36).slice(2, 6).toUpperCase() + Math.random().toString(36).slice(2, 6).toUpperCase(); } while (db.teacherCodes[c]);
      return c;
    };

    if (role === 'teacher') {
      if (!code) code = gen();
      if (db.teacherCodes[code] && db.teacherCodes[code].teacherEmail && db.teacherCodes[code].teacherEmail !== target) {
        return res.status(400).json({ error: 'Код уже занят другим учителем' });
      }
      db.teacherCodes[code] = db.teacherCodes[code] || { teacherEmail: null };
      if (target) db.teacherCodes[code].teacherEmail = target;
      db.classes[code] = db.classes[code] || { code, teacher: target || null, name: '', students: [] };
      if (target && db.users[target]) {
        db.users[target].role = 'teacher'; db.users[target].classCode = code; db.users[target].className = db.classes[code].name || '';
      }
    } else if (role === 'student') {
      if (!code) return res.status(400).json({ error: 'Введи код класса (выдал учитель)' });
      const cls = db.classes[code];
      if (!cls || !cls.teacher) return res.status(400).json({ error: 'Нет класса с таким кодом' });
      if (target && !cls.students.includes(target)) cls.students.push(target);
      if (target && db.users[target]) {
        db.users[target].role = 'student'; db.users[target].classCode = code; db.users[target].className = cls.name || '';
      }
    } else {
      if (target && db.users[target]) { db.users[target].role = 'personal'; db.users[target].classCode = ''; db.users[target].className = ''; }
    }

    await writeDb(db);
    res.json({ ok: true, role, target: target || null, code: code || '' });
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