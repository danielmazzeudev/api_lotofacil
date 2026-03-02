const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 4001;
const currentVersion = "1.0.0";

app.use(cors());

app.get('/', (req, res) => {
    const filePath = path.join(__dirname, 'python/lotofacil.json');

    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
            console.error("Error reading file:", err);
            return res.status(500).json({ error: "File lotofacil.json not found." });
        }
        try {
            res.json(JSON.parse(data));
        } catch (parseErr) {
            res.status(500).json({ error: "Error on JSON file format." });
        }
    });
});

app.get('/version', (req, res) => {
    res.json({ version: currentVersion });
});

app.listen(PORT, () => {
    console.log(`Lotofacil api running on port: ${PORT}`);
    console.log(`Current version: ${currentVersion}`);
});