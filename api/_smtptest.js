// Quick SMTP test — run once locally: node api/_smtptest.js
require('dotenv').config({ path: require('path').join(__dirname, '..', '.env') });
const nodemailer = require('nodemailer');

async function main() {
  const user = process.env.GMAIL_USER;
  const pass = process.env.GMAIL_APP_PASS;
  console.log('Testing SMTP with:', user, pass ? '(pass set)' : '(NO PASS!)');
  const t = nodemailer.createTransport({
    host: 'smtp.gmail.com', port: 465, secure: true,
    auth: { user, pass }
  });
  try {
    const info = await t.sendMail({
      from: `"LingX" <${user}>`,
      to: user,
      subject: 'SMTP тест LingX',
      text: 'Если ты видишь это письмо — SMTP работает!'
    });
    console.log('OK sent:', info.messageId);
  } catch (e) {
    console.error('FAIL:', e.message);
  }
}
main();