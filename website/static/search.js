/*
* @Author: GigaFlower
* @Date:   2016-12-23 23:12:23
* @Last Modified by:   GigaFlower
* @Last Modified time: 2016-12-23 23:16:48
*/

'use strict';

var divSearch = document.getElementById("search");
var divMatch = document.getElementById("match");
var divAdvancedSearch = document.getElementById("advanced");
var idTypeSearch = document.getElementById("typeSearch");
var idInputSearch = document.getElementById("inputSearch");
var idInputMatch = document.getElementById("inputMatch");
var idAdvancedSearchPanel = document.getElementById("advancedSearchPanel");

window.addEventListener('load', function(){
    console.log('远看黄山黑黝黝,上面小来下面大,若将黄山倒过来,上面大来下面小');
    modeSearch();
});

function modeSearch() {
    divSearch.className = "currentLinkTitle";
    divMatch.className = "linkTitle";
    divAdvancedSearch.className = "passiveAdvancedTitle";
    divAdvancedSearch.style.display = "inline-block";
    idTypeSearch.value = "search";
    idInputSearch.style.display = "block";
    idInputMatch.style.display = "none";
    idAdvancedSearchPanel.style.display = "none";
}