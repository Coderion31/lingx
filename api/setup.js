// POST /api/setup {token, role, code}
// Assigns a role to a new user after login:
//   role 'teacher'  -> validates the unique teacher code (owner-issued), binds teacher to it, creates their class
//   role 'student'  -> validates the teacher's class code, attaches the student to that class
//   role 'personal' -> user studies just for themselves, no class
const { readDb, writeDb } = require('./_db');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method' });
  try {
    let body = {};
    try { body = typeof req.body === 'string' ? JSON.parse(req.body) : (req.body || {}); } catch (e) {}
    const token = String(body.token || '').trim();
    const role = String(body.role || '').trim().toLowerCase();
    const code = String(body.code || '').trim().toUpperCase();

    const db = await readDb();
    const email = findEmail(db, token);
    if (!email) return res.status(401).json({ error: 'Не авторизован' });

    const user = db.users[email];
    if (!user) return res.status(404).json({ error: 'Пользователь не найден' });
    if (user.role) return res.status(400).json({ error: 'Роль уже задана' });

    db.teacherCodes = db.teacherCodes || {};
    db.classes = db.classes || {};

    if (role === 'teacher') {
      if (!code) return res.status(400).json({ error: 'Введи код учителя' });
      const inv = db.teacherCodes[code];
      if (!inv) return res.status(400).json({ error: 'Нет такого кода учителя' });
      if (inv.teacherEmail && inv.teacherEmail !== email) return res.status(400).json({ error: 'Этот код уже занят другим учителем' });
      inv.teacherEmail = email;
      db.classes[code] = db.classes[code] || { code, teacher: email, name: '', students: [] };
      user.role = 'teacher';
      user.classCode = code;
      user.className = db.classes[code].name || '';
    } else if (role === 'student') {
      if (!code) return res.status(400).json({ error: 'Введи код класса' });
      const cls = db.classes[code];
      if (!cls || !cls.teacher) return res.status(400).json({ error: 'Нет такого класса. Проверь код у учителя' });
      if (!cls.students.includes(email)) cls.students.push(email);
      user.role = 'student';
      user.classCode = code;
      user.className = cls.name || '';
    } else if (role === 'personal') {
      user.role = 'personal';
      user.classCode = '';
      user.className = '';
    } else {
      return res.status(400).json({ error: 'Неизвестная роль' });
    }

    await writeDb(db);

    let classInfo = null;
    if (code && db.classes[code]) {
      const cls = db.classes[code];
      classInfo = { code: cls.code, name: cls.name, teacherEmail: cls.teacher, studentsCount: (cls.students || []).length };
    }

    res.json({ ok: true, user: safeUser(user), class: classInfo });
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

function safeUser(u) {
  return {
    email: u.email,
    name: u.name,
    verified: !!u.verified,
    createdAt: u.createdAt,
    lastLogin: u.lastLogin,
    role: u.role || null,
    classCode: u.classCode || null,
    className: u.className || null
  };
}