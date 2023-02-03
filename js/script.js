const { Pool } = require("pg");
const pool = new Pool({
    connectionString: process.env.DB_URL || "postgresql://qjtgrmfm:Fa7_jQDLidMKezEMid4xaWlspAj75rOw@hattie.db.elephantsql.com/qjtgrmfm"
});

console.log("DB connection established")

module.exports = pool
