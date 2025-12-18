// test_vulnerable.js
function run(input) {
  // VULNERABLE: uso de eval con entrada directa
  eval(input); 
  // VULNERABLE: innerHTML sin sanitizar
  document.getElementById('output').innerHTML = "<div>" + input + "</div>";
}
