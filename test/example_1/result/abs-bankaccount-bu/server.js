const express = require('express');
const http = require('http');
const proxy = require('http-proxy-middleware');
const path = require('path');

const app = express();

const port = process.env.PORT || '8089';
app.set('port', port);

app.use(express.static(path.join(__dirname, 'dist')));
app.use(proxy('/api', { target: 'http://localhost:8666/' }));

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'dist/abs-bankaccount/index.html'));
});

const server = http.createServer(app);
server.listen(port, () => console.log('Running'));
