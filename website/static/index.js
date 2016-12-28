/*
* @Author: GigaFlower
* @Date:   2016-12-23 23:12:23
* @Last Modified by:   GigaFlower
* @Last Modified time: 2016-12-23 23:16:48
*/

'use strict';

window.addEventListener('load', function(){
    console.log('远看黄山黑黝黝,上面小来下面大,若将黄山倒过来,上面大来下面小');
    document.getElementById("search").className = "currentLinkTitle";
    document.getElementById("senior_search").className = "linkTitle";
    document.getElementById("match").className = "linkTitle";
    document.getElementById("type_search").value = "search";
    document.getElementById("input_search").style.display = "block";
    document.getElementById("input_match").style.display = "none";
    document.getElementById("senior_search_panel").style.display = "none";
    document.getElementById("index_title").style.marginTop = "100px";
});

var divSearch = document.getElementById("search");
divSearch.addEventListener("click", function(){
    document.getElementById("search").className = "currentLinkTitle";
    document.getElementById("senior_search").className = "linkTitle";
    document.getElementById("match").className = "linkTitle";
    document.getElementById("type_search").value = "search";
    document.getElementById("input_search").style.display = "block";
    document.getElementById("input_match").style.display = "none";
    document.getElementById("senior_search_panel").style.display = "none";
    document.getElementById("index_title").style.marginTop = "100px";
})

var divMatch = document.getElementById("match");
divMatch.addEventListener("click", function() {
    document.getElementById("search").className = "linkTitle";
    document.getElementById("match").className = "currentLinkTitle";
    document.getElementById("senior_search").className = "linkTitle";
    document.getElementById("input_search").style.display = "none";
    document.getElementById("input_match").style.display = "block";
    document.getElementById("senior_search_panel").style.display = "none";
    document.getElementById("index_title").style.marginTop = "100px";
})

var divSenior = document.getElementById("senior_search");
divSenior.addEventListener("click", function() {
    document.getElementById("search").className = "linkTitle";
    document.getElementById("senior_search").className = "currentLinkTitle";
    document.getElementById("match").className = "linkTitle";
    document.getElementById("type_search").value = "senior_search";
    document.getElementById("input_search").style.display = "block";
    document.getElementById("input_match").style.display = "none";
    document.getElementById("senior_search_panel").style.display = "block";
    document.getElementById("index_title").style.marginTop = "20px";
})