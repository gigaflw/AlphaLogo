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
    document.getElementById("input_search").className = "linkTitle";
    document.getElementById("search_container").style.display = "block";
    document.getElementById("senior_search_container").style.display = "none";
    document.getElementById("input_match").style.display = "none";
});

var divSearch = document.getElementById("search");
divSearch.addEventListener("click", function(){
    document.getElementById("search").className = "currentLinkTitle";
    document.getElementById("senior_search").className = "linkTitle";
    document.getElementById("search_container").style.display = "block";
    document.getElementById("senior_search_container").style.display = "none";
})

var divSenior = document.getElementById("senior_search");
divSenior.addEventListener("click", function() {
    document.getElementById("search").className = "linkTitle";
    document.getElementById("senior_search").className = "currentLinkTitle";
    document.getElementById("search_container").style.display = "none";
    document.getElementById("senior_search_container").style.display = "block";
})

function getParameter(name){
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var matched = window.location.search.substr(1).match(reg);
    if (matched != null) {
        return unescape(matched[2])
    }
    return null;
}