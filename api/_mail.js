// SMTP mailer — sends code + confirmation link via Gmail App Password
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

async function sendVerification(email, code, confirmLink) {
  const t = getTransporter();
  await t.sendMail({
    from: `"LingX" <${process.env.GMAIL_USER}>`,
    to: email,
    subject: 'Код для входа в LingX',
    text: `Ваш код для входа: ${code}\n\nИли подтвердите email по ссылке:\n${confirmLink}\n\nЕсли вы не запрашивали вход, проигнорируйте это письмо.`,
    html: `<div style="font-family:sans-serif;max-width:480px;margin:0 auto;background:#1e293b;padding:24px;border-radius:12px;color:#e2e8f0">
      <h2 style="color:#60a5fa;margin:0 0 12px">Вход в LingX</h2>
      <p style="color:#94a3b8;margin:0 0 16px">Ваш код для входа:</p>
      <div style="font-size:32px;font-weight:bold;letter-spacing:8px;text-align:center;padding:16px;background:#0f172a;border-radius:8px;color:#60a5fa;margin-bottom:16px">${code}</div>
      <p style="color:#94a3b8;margin:0 0 12px;font-size:13px">Или нажмите кнопку, чтобы подтвердить email:</p>
      <a href="${confirmLink}" style="display:block;text-align:center;padding:12px;background:#60a5fa;color:#fff;border-radius:8px;text-decoration:none;font-weight:600;margin-bottom:12px">Подтвердить email</a>
      <p style="color:#64748b;font-size:11px;margin:0">Код действует 10 минут. Никому не сообщайте код.</p>
    </div>`
  });
}

module.exports = { sendVerification };