// Single line comment
/* Multi-
line
comment
*/
document.querySelector('img').onclick = function() {
    var text = document.querySelector('#header').textContent;
    if (text == "Ilya's Webpage") {
        document.querySelector('#header').textContent = "HI";
    } else {
        document.querySelector('#header').textContent = "Ilya's Webpage";
    }
}