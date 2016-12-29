/*
* @Author: GigaFlower
* @Date:   2016-12-23 23:12:23
* @Last Modified by:   GigaFlower
* @Last Modified time: 2016-12-23 23:16:48
*/

'use strict';

var divSearch = document.getElementById("search");
var divMatch = document.getElementById("match");
var divSeniorSearch = document.getElementById("senior");
var idTypeSearch = document.getElementById("type_search");
var idInputSearch = document.getElementById("input_search");
var idSeniorSearchPanel = document.getElementById("senior_search_panel");

window.addEventListener('load', function(){
    console.log('远看黄山黑黝黝,上面小来下面大,若将黄山倒过来,上面大来下面小');
    modeSearch();
});

divSearch.addEventListener("click", function(){
    modeSearch();
})

divMatch.addEventListener("click", function() {
    //modeMatch();
})

divSeniorSearch.addEventListener("click", function() {
    switchSeniorSearch();
})

function modeSearch() {
    divSearch.className = "currentLinkTitle";
    divMatch.className = "linkTitle";
    divSeniorSearch.className = "passiveSeniorTitle";
    divSeniorSearch.style.display = "inline-block";
    idTypeSearch.value = "search";
    idInputSearch.style.display = "block";
    idSeniorSearchPanel.style.display = "none";
}

function modeMatch() {
    divSearch.className = "linkTitle";
    divMatch.className = "currentLinkTitle";
    divSeniorSearch.style.display = "none";
    idInputSearch.style.display = "none";
    idInputMatch.style.display = "block";
    idSeniorSearchPanel.style.display = "none";
}

function switchSeniorSearch() {
    if (divSeniorSearch.className == "passiveSeniorTitle") {
        idTypeSearch.value = "senior_search";
        idSeniorSearchPanel.style.display = "block";
        divSeniorSearch.className = "activeSeniorTitle";
    } else {
        idTypeSearch.value = "search";
        idSeniorSearchPanel.style.display = "none";
        divSeniorSearch.className = "passiveSeniorTitle";
    }
}

function getParameter(name){
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var matched = window.location.search.substr(1).match(reg);
    if (matched != null) {
        return unescape(matched[2])
    }
    return null;
}