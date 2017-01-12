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
var idCurrentPointer = document.getElementById("currentPointer");

window.addEventListener('load', function(){
    console.log('远看黄山黑黝黝,上面小来下面大,若将黄山倒过来,上面大来下面小');
    modeMatchInitial();
    pieAnimationUpload();
});

function modeMatchInitial() {
    divSearch.className = "linkTitle";
    divMatch.className = "currentLinkTitle";
    divAdvancedSearch.style.display = "none";
    idInputSearch.style.display = "none";
    idInputMatch.style.display = "block";
    idAdvancedSearchPanel.style.transform = "rotateX(90deg)";
    divResultContainer.style.marginRight = "250px";
    idCurrentPointer.style.left = "375px";
}


function pieAnimationUpload() {
    var tmp = [];
    var colorlist = document.getElementById(
        "uploadColorsList").textContent.split(',');
    for (var x = 0; x < colorlist.length; ++x) {
        tmp.push(colorlist[x].substring(2, 9));
    }
    console.log(tmp);
    pieAnimation("chosenPie1", tmp);
}

function pieAnimation(pieID, colors_tmp) {
    colors_tmp.push("white");
    var updatingChart = $("#" + pieID).peity("pie", { "fill": colors_tmp, "radius": 38 })
    var timerID = setInterval(function() {
        var values = updatingChart.text().split(",");
        var tmp = values.pop();
        if (tmp > 100) {
            tmp = tmp * 0.3;
        } else if (tmp > 0.1) {
            tmp = tmp * 0.7;
        } else if (tmp > 0.05) {
            tmp = tmp - 0.01;
        } else if (tmp >= 0.00) {
            tmp = tmp - 0.005;
        }
        values.push(tmp);
        updatingChart.text(values.join(",")).change();
    }, 60);
    return timerID;
};

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


