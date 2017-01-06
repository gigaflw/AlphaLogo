/*
* @Author: GigaFlower
* @Date:   2016-12-23 23:12:23
* @Last Modified by:   GigaFlower
* @Last Modified time: 2016-12-23 23:16:48
*/

'use strict';

var divSearch = document.getElementById("search");
var divMatch = document.getElementById("match");
var idBrowse = document.getElementById("browse");
var idLogo = document.getElementById("logo");
var idTextfield = document.getElementById("textfield");
var idTypeSearch = document.getElementById("typeSearch");
var idInputSearch = document.getElementById("inputSearch");
var idInputMatch = document.getElementById("inputMatch");
var idEnterpriseName = document.getElementById("enterpriseName");
var divTitleContainer = document.getElementById("titleContainer");
var idTitle = document.getElementById("title");
var idNColors = document.getElementById("nColors");
var idImgSubmit = document.getElementById("imgSubmit");

var divAdvancedSearch = document.getElementById("advanced");
var idAdvancedSearchPanel = document.getElementById("advancedSearchPanel");
var advancedColorNum2 = document.getElementById("colorNum2");
var advancedColorNum3 = document.getElementById("colorNum3");
var advancedColorNum4 = document.getElementById("colorNum4");
var advancedColorNum5 = document.getElementById("colorNum5");
var advancedColorNumMore = document.getElementById("colorNumMore");
var advancedIndustryBank = document.getElementById("industryBank");
var advancedIndustryStock = document.getElementById("industryStock");
var advancedIndustryIT = document.getElementById("industryIT");
var advancedIndustryManufacturing = document.getElementById("industryManufacturing");
var advancedIndustryEducation = document.getElementById("industryEducation");
var advancedEnterpriseName = document.getElementById("advancedEnterpriseName");

window.addEventListener('load', function(){
    advancedSearchTypeInitialization();
    titleContainerActivate();
});

window.onscroll = function() {
    titleContainerActivate();
}

divSearch.addEventListener("click", function(){
    modeSearch();
})

divMatch.addEventListener("click", function() {
    modeMatch();
})

divAdvancedSearch.addEventListener("click", function() {
    switchAdvancedSearch();
})

idBrowse.addEventListener("click", function() {
    idLogo.click();
})

idTitle.addEventListener("click", function() {
    window.location.href = "/";
})

idImgSubmit.addEventListener("click", function() {
    setTimeout('idImgSubmit.disabled = "disabled"', 50);
})

function showTextField() {
    //idImgSubmit.click();

    var fileName = idLogo.value;
    var reg = new RegExp("\\\\\.[^\\\\]*$");
    var regFileName = reg.exec(fileName);
    regFileName = JSON.stringify(regFileName);
    idTextfield.value = regFileName.substring(4, regFileName.length-2);

    //idPreviewImg.src = "/static/uploads/upload.jpg";
}

function modeSearch() {
    divSearch.className = "currentLinkTitle";
    divMatch.className = "linkTitle";
    divAdvancedSearch.className = "passiveAdvancedTitle";
    divAdvancedSearch.style.display = "inline-block";
    idTypeSearch.value = "search";
    idInputSearch.style.display = "block";
    idInputMatch.style.display = "none";
    idAdvancedSearchPanel.style.transform = "rotateX(90deg)";
}

function modeMatch() {
    divSearch.className = "linkTitle";
    divMatch.className = "currentLinkTitle";
    divAdvancedSearch.style.display = "none";
    idInputSearch.style.display = "none";
    idInputMatch.style.display = "block";
    idAdvancedSearchPanel.style.transform = "rotateX(90deg)";
}

function switchAdvancedSearch() {
    if (divAdvancedSearch.className == "passiveAdvancedTitle") {
        idTypeSearch.value = "advancedSearch";
        idAdvancedSearchPanel.style.transform = "rotateX(0deg)";
        divAdvancedSearch.className = "activeAdvancedTitle";
    } else {
        idTypeSearch.value = "search";
        idAdvancedSearchPanel.style.transform = "rotateX(90deg)";
        divAdvancedSearch.className = "passiveAdvancedTitle";
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

function advancedSearchTypeInitialization() {
    var advancedSearchTypeArray = new Array(advancedColorNum2, advancedColorNum3, advancedColorNum4, advancedColorNum5,
                                            advancedColorNumMore, advancedIndustryBank, advancedIndustryStock, advancedIndustryIT,
                                            advancedIndustryManufacturing, advancedIndustryEducation);
    for (var x=0; x<advancedSearchTypeArray.length; ++x) {
        (function(){    // js的函数闭包问题
            var i = x;
            advancedSearchTypeArray[i].addEventListener("click", function(){
                switchAdvancedSearchType(this);
                var colorTotalNum = 5;
                if (i < colorTotalNum) {
                    nColorsInput(i, this);
                }
            });
        })();
    }
}

function switchAdvancedSearchType(advancedSearchType) {
    if (advancedSearchType.className == "advancedSearchType") {
        advancedSearchType.className = "advancedSearchTypeActive";
    } else {
        advancedSearchType.className = "advancedSearchType";
    }
}

function enterpriseNameInput() {
    idEnterpriseName.value = advancedEnterpriseName.value;
}

function titleContainerActivate() {
    var windowScroll = document.documentElement.scrollTop || document.body.scrollTop;
    if (windowScroll >= 150) {
        if (divTitleContainer.className == "titleContainerDefault") {
            divTitleContainer.className = "titleContainerPassive";
        }
    } else {
        if (divTitleContainer.className == "titleContainerPassive") {
            divTitleContainer.className = "titleContainerDefault";
        }
    }
}

function nColorsInput(n, advancedColorNum) {
    var inputNColors = idNColors.value;
    //alert(inputNColors);
    inputNColors = inputNColors.split(",");
    var nDigit = inputNColors[n];
    if (nDigit == "0") {
        inputNColors.splice(n, 1, "1");
    } else {
        inputNColors.splice(n, 1, "0");
    }
    inputNColors = inputNColors.join(",");
    //alert(inputNColors);
    idNColors.value = inputNColors;
}