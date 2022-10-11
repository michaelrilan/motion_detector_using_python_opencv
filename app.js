const express = require("express");
const mysql = require("mysql2");
const app = express();
const bodyParser = require("body-parser");
const port = 3100;

const connection = mysql.createConnection({
    host: "localhost",
    user: "root",
    password: "",
    database: "movement_detection",
  });
  app.use(bodyParser.json());

  
app.post("/tolongges", (req, res) => {
  const { date_and_time,image_path } = req.body;

  connection.query(
    "INSERT INTO movement (date_and_time,image_path) VALUES (?,?)",
    [date_and_time,image_path],
    (err, results) => {
      try {
        if (results.affectedRows > 0) {
          res.json({ message: "Motion Recorded" });
        } else {
          res.json({ message: "Something went wrong." });
        }
      } catch (err) {
        res.json({ message: err });
      }
    }
  );
});



app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});