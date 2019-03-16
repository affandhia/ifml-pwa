const express = require('express');
const proxy = require('express-http-proxy');
const http = require('http');
const path = require('path');

const app = express();

const port = process.env.PORT || '8089';
app.set('port', port);

app.use(express.static(path.join(__dirname, 'dist')));

app.get(
  '/api/*',
  proxy('localhost:8666', {
    proxyReqPathResolver: function(req) {
      return new Promise(function(resolve, reject) {
        setTimeout(function() {
          // simulate async
          var parts = req.url.split('?');
          var queryString = parts[1];
          var updatedPath = parts[0].replace(/test/, 'tent');
          var resolvedPathValue =
            updatedPath + (queryString ? '?' + queryString : '');
          resolve(resolvedPathValue);
        }, 200);
      });
    },
  })
);
app.get(
  '/google',
  proxy('www.google.com', {
    proxyReqPathResolver: function(req) {
      const requestedUrl = `${req.protocol}://${req.get('Host')}${req.url}`;
      const modifiedURL = modifyURL(requestedUrl);
      return require('url').parse(modifiedURL).path;
    },
  })
);

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'dist/abs-bankaccount/index.html'));
});

const server = http.createServer(app);
server.listen(port, () => console.log('Running'));
