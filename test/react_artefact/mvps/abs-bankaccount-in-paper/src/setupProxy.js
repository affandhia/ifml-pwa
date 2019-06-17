const proxy = require('http-proxy-middleware');

const BACKEND_PORT = 7776; // set backend port
const PATH = 'http://localhost:' + BACKEND_PORT + '/';

module.exports = function(app) {
  app.use(proxy('/api', { target: PATH }));
};
