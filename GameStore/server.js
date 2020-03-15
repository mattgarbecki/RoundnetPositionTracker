// Modules
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');

var app = express();
app.use(cors());
app.use(bodyParser.json());
app.listen(3500);

translateToCSV('a');

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

    address_book.set(content.name, [content.address, content.port]);
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


function translateToCSV(data) {
    const rows = [
        ["time", "x", "y", "z"],
        ["1", "0.1", "0.2", "-0.5"],
        ["2", "-0.5", "0.1", "-0.3"],
        ["3", "-0.3", "0.1", "0.5"]
    ];
    
    let csvContent = "";
    
    rows.forEach(function(rowArray) {
        let row = rowArray.join(",");
        csvContent += row + "\r\n";
    });

    var encodedUri = encodeURI(csvContent);
    console.log(csvContent);
}