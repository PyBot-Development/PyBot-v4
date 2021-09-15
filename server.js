const express = require("express");
const bodyParser = require("body-parser");
const router = express.Router();
const app = express()

const port = 80
const publicIp = require('public-ip');

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

const key="C1EwnVfE0vwOaTnTQxzLo5Qp83vXmRvGX0YRZjirIwphLZqOWUx8RUOQKTihNrZo9Jl7JMxXF2IapK8"
logs = []

app.get('/', (req, res) => {
  var ip = req.headers['x-forwarded-for'] || req.socket.remoteAddress 
  console.log(`[/] from: ${ip}`)
  res.json(logs)
})

router.post('/add:?', function (req, res) {
  var ip = req.headers['x-forwarded-for'] || req.socket.remoteAddress
  if(req.query["key"]==key){
    try{
      logs.push(req.body)
    } catch(error){
      console.log(`[/add] From: ${ip}, Succesfull: false`)
      res.json({"status": 400, "message": `${error}`})
      return
    }
    res.json({"status": 201, "message": `Added '${req.query["log"]}' to logs`})
    console.log(`[/add] From: ${ip}, Succesfull: true`)
  } else {
    res.json({"status": 403, "message": "Forbidden."})
    console.log(`[/add] From: ${ip}, Succesfull: false`)
  }
})

app.use("/", router)
app.listen(port, () => {
  publicIp.v4().then(ip => {
    console.log(`Running on: http://${ip}:${port}`);
  });
})