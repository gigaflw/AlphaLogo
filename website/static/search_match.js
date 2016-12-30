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
var idBrowse = document.getElementById("browse");
var idLogo = document.getElementById("logo");
var idTextfield = document.getElementById("textfield");
var idTypeSearch = document.getElementById("type_search");
var idInputSearch = document.getElementById("input_search");
var idInputMatch = document.getElementById("input_match");
var idSeniorSearchPanel = document.getElementById("senior_search_panel");

divSearch.addEventListener("click", function(){
    modeSearch();
})

divMatch.addEventListener("click", function() {
    modeMatch();
})

divSeniorSearch.addEventListener("click", function() {
    switchSeniorSearch();
})

idBrowse.addEventListener("click", function() {
    idLogo.click();
})

function showTextField() {
    var fileName = idLogo.value;
    var reg = new RegExp("\\\\\.[^\\\\]*$");
    var regFileName = reg.exec(fileName);
    regFileName = JSON.stringify(regFileName);
    idTextfield.value = regFileName.substring(4, regFileName.length-2);
}

function modeSearch() {
    divSearch.className = "currentLinkTitle";
    divMatch.className = "linkTitle";
    divSeniorSearch.className = "passiveSeniorTitle";
    divSeniorSearch.style.display = "inline-block";
    idTypeSearch.value = "search";
    idInputSearch.style.display = "block";
    idInputMatch.style.display = "none";
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