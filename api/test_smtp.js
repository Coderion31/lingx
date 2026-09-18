require('dotenv').config({ path: require('path').join(__dirname, '..', '.env') });
const nodemailer = require('nodemailer');

async function main() {
  const user = process.env.GMAIL_USER;
  const pass = process.env.GMAIL_APP_PASS;
  console.log('User:', user, 'Pass set:', !!pass);
  if (!pass) { console.error('NO PASSWORD'); return; }
  const t = nodemailer.createTransport({
    host: 'smtp.gmail.com', port: 465, secure: true,
    auth: { user, pass }
  });
  try {
    const info = await t.sendMail({
      from: `"LingX" <${user}>`,
      to: user,
      subject: 'SMTP тест LingX',
      text: 'Если ты видишь это — SMTP работает! Пароль приложения верный.'
    });
    console.log('OK, messageId:', info.messageId);
    console.log('Письмо отправлено на', user);
  } catch (e) {
    console.error('FAIL:', e.message);
  }
}
main();