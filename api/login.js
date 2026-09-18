// POST /api/login {email} — alias for send-code (simplified)
// Redirects to send-code
module.exports = async function (req, res) {
  if (!req.url) req.url = '/api/send-code';
  delete require.cache[require.resolve('./send-code')];
  return require('./send-code')(req, res);
};