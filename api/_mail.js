// SMTP mailer via Gmail App Password
const nodemailer = require('nodemailer');

let transporter = null;

function getTransporter() {
  if (transporter) return transporter;
  const user = process.env.GMAIL_USER;
  const pass = process.env.GMAIL_APP_PASS;
  transporter = nodemailer.createTransport({
    host: 'smtp.gmail.com',
    port: 465,
    secure: true,
    auth: { user, pass }
  });
  return transporter;
}

async function sendVerification(email, code) {
  const t = getTransporter();
  await t.sendMail({
    from: `"LingX" <${process.env.GMAIL_USER}>`,
    to: email,
    subject: 'Код подтверждения LingX',
    text: `Ваш код подтверждения: ${code}\n\nЕсли вы не регистрировались, просто проигнорируйте это письмо.`,
    html: `<div style="font-family:sans-serif;max-width:480px;margin:0 auto;background:#1e293b;padding:24px;border-radius:12px;color:#e2e8f0">
      <h2 style="color:#60a5fa;margin:0 0 12px">Код подтверждения</h2>
      <p style="color:#94a3b8;margin:0 0 16px">Ваш код для входа на LingX:</p>
      <div style="font-size:32px;font-weight:bold;letter-spacing:8px;text-align:center;padding:16px;background:#0f172a;border-radius:8px;color:#60a5fa">${code}</div>
      <p style="color:#64748b;font-size:12px;margin-top:16px">Никому не сообщайте этот код.</p>
    </div>`
  });
}

module.exports = { sendVerification };