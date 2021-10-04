/**
*  Discord Pybot Server
*  ~~~~~~~~~~~~~~~~~
* 
*  Discord Bot Server. Logs/Data
* 
*  :copyright: (c) 2021-2021 mariyt10
*  :license: MIT, see LICENSE for more details.
* 
*/


const express = require("express");
const http = require('http');
const https = require('https');

const bodyParser = require("body-parser");

const router = express.Router();
const app = express()

const yaml = require('js-yaml');
const fs = require('fs');
const publicIp = require('public-ip');

const privateKey = fs.readFileSync('/etc/letsencrypt/live/api.py-bot.m2rsho.cf/privkey.pem', 'utf8');
const certificate = fs.readFileSync('/etc/letsencrypt/live/api.py-bot.m2rsho.cf/cert.pem', 'utf8');
const ca = fs.readFileSync('/etc/letsencrypt/live/api.py-bot.m2rsho.cf/chain.pem', 'utf8');

const credentials = {
	key: privateKey,
	cert: certificate,
	ca: ca
};

try {
  var data = yaml.load(fs.readFileSync('config.yaml', 'utf8'));
} catch (e) {
  console.log(e);
}

const port = data['Server-Port']
const key = data['Server-Key']

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

logs = []
bot_status = {"last_update": "Null"}

const bgBlack = "\x1b[40m"
const reset = "\x1b[0m"
const yellow = "\x1b[33m"
const white = "\x1b[37m"
const green = "\x1b[32m"


app.get('/', (req, res) => {
  const d = new Date();
  const date = `${d.getHours()}:${d.getMinutes()}:${d.getSeconds()}.${d.getMilliseconds()}`
  var ip = req.headers['x-forwarded-for'] || req.socket.remoteAddress 
  console.log(`${bgBlack}${white}${date}${reset}: ${green}[SERVER][/] ${yellow}${ip} ${green}GET LOGS${reset}`)
  res.set('Access-Control-Allow-Origin', '*');
  res.json(logs)
})
app.get('/.well-known/acme-challenge/Lke6dOC_yllj1Vy36XYjKLIkLWx58iOQ2lUS_oIRook', (req, res) => {
  res.send("Lke6dOC_yllj1Vy36XYjKLIkLWx58iOQ2lUS_oIRook.2uLSL8KeFAI43OSUKDB4zK7u2fdAO0AP-K5tE5LtXMo")
})
router.post('/add:?', function (req, res) {
  const d = new Date();
  const date = `${d.getHours()}:${d.getMinutes()}:${d.getSeconds()}.${d.getMilliseconds()}`
  var ip = req.headers['x-forwarded-for'] || req.socket.remoteAddress
  if(ip == "::1"){
    ip = "Self"
  }
  if(req.query["key"]==key){
    try{
      logs.push(req.body)
    } catch(error){
      console.log(`${bgBlack}${white}${date}${reset}: ${green}[SERVER][/add] ${yellow}${ip} ${green}POST LOG${reset}, ${yellow}Succesfull${reset}: ${green}false${reset}`)
      res.json({"status": 400, "message": `${error}`})
      return
    }
    res.json({"status": 201, "message": `Added '${req.query["log"]}' to logs`})
    console.log(`${bgBlack}${white}${date}${reset}: ${green}[SERVER][/add] ${yellow}${ip} ${green}POST LOG${reset}, ${yellow}Succesfull${reset}: ${green}true${reset}`)
  } else {
    res.json({"status": 403, "message": "Forbidden."})
    console.log(`${bgBlack}${white}${date}${reset}: ${green}[SERVER][/add] ${yellow}${ip} ${green}POST LOG${reset}, ${yellow}Succesfull${reset}: ${green}false${reset}`)
  }
})
router.post('/set-status:?', function (req, res) {
  const d = new Date();
  const date = `${d.getHours()}:${d.getMinutes()}:${d.getSeconds()}.${d.getMilliseconds()}`
  var ip = req.headers['x-forwarded-for'] || req.socket.remoteAddress
  if(ip == "::1"){
    ip = "Self"
  }
  if(req.query["key"]==key){
    try{
      bot_status = (req.body)
    } catch(error){
      console.log(`${bgBlack}${white}${date}${reset}: ${green}[SERVER][/set-status] ${yellow}${ip} ${green}POST STATUS${reset}, ${yellow}Succesfull${reset}: ${green}false${reset}`)
      res.json({"status": 400, "message": `${error}`})
      return
    }
    res.json({"status": 201, "message": `Added '${req.query["log"]}' to logs`})
    console.log(`${bgBlack}${white}${date}${reset}: ${green}[SERVER][/set-status] ${yellow}${ip} ${green}POST STATUS${reset}, ${yellow}Succesfull${reset}: ${green}true${reset}`)
  } else {
    res.json({"status": 403, "message": "Forbidden."})
    console.log(`${bgBlack}${white}${date}${reset}: ${green}[SERVER][/set-status] ${yellow}${ip} ${green}POST STATUS${reset}, ${yellow}Succesfull${reset}: ${green}false${reset}`)
  }
})

app.get('/status', (req, res) => {
  const d = new Date();
  const date = `${d.getHours()}:${d.getMinutes()}:${d.getSeconds()}.${d.getMilliseconds()}`
  var ip = req.headers['x-forwarded-for'] || req.socket.remoteAddress 
  console.log(`${bgBlack}${white}${date}${reset}: ${green}[SERVER][/status] ${yellow}${ip} ${green}GET STATUS${reset}`)
  res.set('Access-Control-Allow-Origin', '*');
  res.json(bot_status)
})

app.use("/", router)

const httpServer = http.createServer(app);
const httpsServer = https.createServer(credentials, app);

//app.listen(port, () => {
//  publicIp.v4().then(ip => {
//    console.log(`${yellow}Running Server On${reset}: ${green}http://${ip}:${port}${reset} or ${green}http://localhost:${port}${reset}`);
//  });
//})


httpServer.listen(80, () => {
	console.log('HTTP Server running on port 80');
});

httpsServer.listen(443, () => {
	console.log('HTTPS Server running on port 80');
});
