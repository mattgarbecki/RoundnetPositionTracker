// Modules
const express = require('express');
const bodyParser = require('body-parser');
const request = require('request');
const cors = require('cors');

var app = express();
app.use(cors());
app.use(bodyParser.json());
app.listen(3500);

var address_book = new Map();

app.post("/hostgame", (req, res) => {

    var content = req.body;

    if(content.name.length <= 0 || content.address.length <= 0) {
        res.send("INVALID");
        return;
    }
    if(address_book.has(content.name)) {
        res.send("USED");
        return;
    }

    address_book.set(content.name, content.address);
    res.send("OK");

});

app.get("/address", (req, res) => {

    var content = req.query;

    if(content.name.length <= 0) {
        res.send("INVALID");
        return;
    }
    if(!address_book.has(content.name)) {
        res.send("NONAME");
        return;
    }

    res.send(address_book.get(content.name));

});

app.get("/remove", (req, res) => {

    var content = req.query;

    if(!address_book.has(content.name)) {
        res.send("NONAME");
        return;
    }

    address_book.delete(content.name);
    res.send("OK");

});
