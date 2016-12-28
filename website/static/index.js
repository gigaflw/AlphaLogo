/*
* @Author: GigaFlower
* @Date:   2016-12-23 23:12:23
* @Last Modified by:   GigaFlower
* @Last Modified time: 2016-12-23 23:16:48
*/

'use strict';

var divSearch = document.getElementById("search");
var divMatch = document.getElementById("match");
var divSenior = document.getElementById("senior_search");
var idSearch = document.getElementById("search");
var idSeniorSearch = document.getElementById("senior_search");
var idMatch = document.getElementById("match");
var idTypeSearch = document.getElementById("type_search");
var idInputSearch = document.getElementById("input_search");
var idInputMatch = document.getElementById("input_match");
var idSeniorSearchPanel = document.getElementById("senior_search_panel");
var idIndexTitle = document.getElementById("index_title");

window.addEventListener('load', function(){
    console.log('远看黄山黑黝黝,上面小来下面大,若将黄山倒过来,上面大来下面小');
    modeSearch();
});

divSearch.addEventListener("click", function(){
    modeSearch();
})

divMatch.addEventListener("click", function() {
    modeMatch();
})

divSenior.addEventListener("click", function() {
    switchSeniorSearch();
})

function modeSearch() {
    idSearch.className = "currentLinkTitle";
    idMatch.className = "linkTitle";
    idSeniorSearch.className = "passiveSeniorTitle";
    idTypeSearch.value = "search";
    idInputSearch.style.display = "block";
    idInputMatch.style.display = "none";
    idSeniorSearchPanel.style.display = "none";
    idIndexTitle.style.marginTop = "100px";
}

function modeMatch() {
    idSearch.className = "linkTitle";
    idMatch.style.className = "currentLinkTitle";
    idSeniorSearch.style.display = "none";
    idInputSearch.style.display = "none";
    idInputMatch.style.display = "block";
    idIndexTitle.style.marginTop = "100px";
}

function switchSeniorSearch() {
    if (idSeniorSearch.className == "passiveSeniorTitle") {
        idSeniorSearch.className == "activeSeniorTitle";
        idTypeSearch.value = "senior_search";
        idSeniorSearchPanel.style.display = "block";
    } else {
        idSeniorSearch.className == "passiveSeniorTitle";
        idTypeSearch.value = "search";
        idSeniorSearchPanel.style.display = "none";
    }
}