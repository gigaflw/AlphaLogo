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
var idInputSearch = document.getElementById("inputSearch");
var idInputMatch = document.getElementById("inputMatch");
var idAdvancedSearchPanel = document.getElementById("advancedSearchPanel");
var idPreviewImg = document.getElementById("previewImg");
var divResultContainer = document.getElementById("resultContainer");
var divPreview = document.getElementById("previewDiv");

window.addEventListener('load', function(){
    console.log('远看黄山黑黝黝,上面小来下面大,若将黄山倒过来,上面大来下面小');
    modeMatch();
});

function modeMatch() {
    divSearch.className = "linkTitle";
    divMatch.className = "currentLinkTitle";
    divAdvancedSearch.style.display = "none";
    idInputSearch.style.display = "none";
    idInputMatch.style.display = "block";
    idAdvancedSearchPanel.style.transform = "rotateX(90deg)";
}

(function() {
    var rectangleTmp = 111;
    setInterval(function() {
        var temp = document.getElementById("rect1a")
        var rectvalue = temp.textContent;
        temp.style = "width:" + Math.min(100,rectangleTmp) + "%";
        rectangleTmp = parseInt(rectangleTmp * 0.92 + (100 - rectvalue * 100) * 0.08);
    }, 50);
})();

(function() {
    var rectangleTmp2 = 111;
    setInterval(function() {
        var temp2 = document.getElementById("rect1b")
        var rectvalue2 = temp2.textContent;
        temp2.style = "width:" + Math.min(100,rectangleTmp2) + "%";
        rectangleTmp2 = parseInt(rectangleTmp2 * 0.92 + (100 - rectvalue2 * 100) * 0.08);
    }, 50);
})();


(function() {
    var rectangleTmp3 = 111;
    setInterval(function() {
        var temp3 = document.getElementById('chosenRectSaturation')
        var rectvalue3 = temp3.textContent;
        temp3.style = "width:" + Math.min(100,rectangleTmp3) + "%";
        rectangleTmp3 = parseInt(rectangleTmp3 * 0.92 + (100 - rectvalue3 * 100) * 0.08);
    }, 50);
})();

(function() {
    var rectangleTmp4 = 111;
    setInterval(function() {
        var temp4 = document.getElementById('chosenRectValue')
        var rectvalue4 = temp4.textContent;
        temp4.style = "width:" + Math.min(100,rectangleTmp4) + "%";
        rectangleTmp4 = parseInt(rectangleTmp4 * 0.92 + (100 - rectvalue4 * 100) * 0.08);
    }, 50);
})();
