// Modules
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
var fs = require('fs');


// SERVER SETTINGS
var app = express();
app.use(cors());
app.use(bodyParser.json());
app.listen(3500);


// GLOBAL VARIABLES
var gameDataStore = new Map();


// APIs
app.post("/createGame", (req, res) => {

    var content = req.body;

    var unique_id = Math.floor(Math.random() * (999999 - 100000 + 1)) + 100000;

    while(gameDataStore.has(unique_id)) {
        unique_id = Math.floor(Math.random() * (999999 - 100000 + 1)) + 100000;
    }

    gameDataStore.set(unique_id.toString(), new Map());
    gameDataStore.get(unique_id.toString()).set('max_player_count', parseInt(content.player_count));
    gameDataStore.get(unique_id.toString()).set('player_count', 0);

    console.log(gameDataStore);

    res.json(JSON.stringify({"id": unique_id.toString()}));
});

app.post("/sendToGame", (req, res) => {

    var content = req.body;

    if(!gameDataStore.has(content.id)) {
        res.send("No game found");
        return;
    }

    gameDataStore.get(content.id).set(content.name, content.data);
    gameDataStore.get(content.id).set('player_count', gameDataStore.get(content.id).get('player_count') + 1);

    console.log(gameDataStore);

    // if the all players have sent their information
    if(gameDataStore.get(content.id).get('player_count') === gameDataStore.get(content.id).get('max_player_count')) {

        // send data to textfile for now, but in future send to database
        var game_data = Object.fromEntries(gameDataStore.get(content.id));

        delete game_data['player_count'];
        delete game_data['max_player_count'];

        fs.writeFileSync("./logs/" + content.id + ".txt", JSON.stringify(game_data));
    }

    res.send(JSON.stringify(gameDataStore.get(content.id)));
});
