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
var divResultContainer = document.getElementById("resultContainer");
var idCurrentPointer = document.getElementById("currentPointer");

var idTriangleLeft = document.getElementById("triangleLeft");
var idTriangleRight = document.getElementById("triangleRight");
var idResultPart1 = document.getElementById("resultPart1");
var idResultPart2 = document.getElementById("resultPart2");
var idResultPart3 = document.getElementById("resultPart3");

var logoNum = parseInt(idTriangleRight.getAttribute("dataLogoNum"));

window.addEventListener('load', function(){
    console.log('远看黄山黑黝黝,上面小来下面大,若将黄山倒过来,上面大来下面小');
    resultPartInitialization();
    modeSearchInitial();
});

idTriangleLeft.addEventListener("click", function() {
    if (idTriangleLeft.className == "triangleLeft") {
        previousPage();
    }
})

idTriangleRight.addEventListener("click", function() {
    if (idTriangleRight.className == "triangleRight") {
        nextPage();
    }
})

function modeSearchInitial() {
    divSearch.className = "currentLinkTitle";
    divMatch.className = "linkTitle";
    divAdvancedSearch.className = "passiveAdvancedTitle";
    divAdvancedSearch.style.display = "inline-block";
    idTypeSearch.value = "search";
    idInputSearch.style.display = "block";
    idInputMatch.style.display = "none";
    idAdvancedSearchPanel.style.transform = "rotateX(90deg)";
    idCurrentPointer.style.left = "252px";
    divResultContainer.style.marginRight = "0px";
}

function resultPartInitialization () {
    try {
        idResultPart1.style.opacity = "1";
        idResultPart1.style.left = "0%";
        idResultPart2.style.opacity = "1";
        idResultPart2.style.left = "140%";
        idResultPart3.style.opacity = "1";
        idResultPart3.style.left = "280%";
    } catch (e) {
        console.log(e.message);
    }
    if ( logoNum <= 20 ) {
        idTriangleRight.className = "triangleRightUnable";
    }
}

function nextPage () {
    if (idResultPart1.style.left == "0%") {
        try {
            idResultPart1.style.left = "-140%";
            idResultPart2.style.left = "0%";
            idResultPart3.style.left = "140%";
        } catch (e) {
            console.log(e.message);
        }
        
        idTriangleLeft.className = "triangleLeft";
        if (logoNum <= 40) {
            idTriangleRight.className = "triangleRightUnable";
        }
    } else if (idResultPart1.style.left == "-140%") {
        try {
            idResultPart1.style.left = "-280%";
            idResultPart2.style.left = "-140%";
            idResultPart3.style.left = "0%";
        } catch (e) {
            console.log(e.message);
        }
        idTriangleRight.className = "triangleRightUnable";
    }
}

function previousPage () {
    if (idResultPart1.style.left == "-140%") {
        try {
            idResultPart1.style.left = "0%";
            idResultPart2.style.left = "140%";
            idResultPart3.style.left = "280%";
        } catch (e) {
            console.log(e.message);
        }
        idTriangleLeft.className = "triangleLeftUnable";
    } else if (idResultPart1.style.left == "-280%") {
        try {
            idResultPart1.style.left = "-140%";
            idResultPart2.style.left = "0%";
            idResultPart3.style.left = "140%";
        } catch (e) {
            console.log(e.message);
        }
        idTriangleRight.className = "triangleRight";
    }
}