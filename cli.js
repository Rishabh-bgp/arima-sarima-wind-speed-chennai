// node demo/cli.js model.json cases.json  (cases: [{hist:[...], h:n}])
const fs = require("fs"); const A = require("./arma.js");
const m = JSON.parse(fs.readFileSync(process.argv[2])); const C = JSON.parse(fs.readFileSync(process.argv[3]));
console.log(JSON.stringify(C.map(c => A.forecast(m, c.hist, c.h))));
