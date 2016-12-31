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
var idInputSearch = document.getElementById("input_search");
var idInputMatch = document.getElementById("input_match");
var idSeniorSearchPanel = document.getElementById("senior_search_panel");

window.addEventListener('load', function(){
    console.log('远看黄山黑黝黝,上面小来下面大,若将黄山倒过来,上面大来下面小');
    modeMatch();
});

function modeMatch() {
    divSearch.className = "linkTitle";
    divMatch.className = "currentLinkTitle";
    divSeniorSearch.style.display = "none";
    idInputSearch.style.display = "none";
    idInputMatch.style.display = "block";
    idSeniorSearchPanel.style.display = "none";
}