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
var idSaturation = document.getElementById("saturation");
var idBrightness = document.getElementById("brightness");
var idImgSubmit = document.getElementById("imgSubmit");
var divResultContainer = document.getElementById("resultContainer");
var idCurrentPointer = document.getElementById("currentPointer");

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
var advancedSaturationLow = document.getElementById("saturationLow");
var advancedSaturationMiddle = document.getElementById("saturationMiddle");
var advancedSaturationHigh = document.getElementById("saturationHigh");
var advancedBrightnessLow = document.getElementById("brightnessLow");
var advancedBrightnessMiddle = document.getElementById("brightnessMiddle");
var advancedBrightnessHigh = document.getElementById("brightnessHigh");
var advancedEnterpriseName = document.getElementById("advancedEnterpriseName");

var currentChosenImg = null;
var divChosenImg = document.getElementById("chosenImgDiv");
var chosenImg = document.getElementById("chosenImg");
var chosenImgEntName = document.getElementById("chosenImgEntName");
var chosenImgSaturation = document.getElementById("chosenImgSaturation");
var chosenImgValue = document.getElementById("chosenImgValue");
var chosenImgRectSaturation = document.getElementById("chosenRectSaturation");
var chosenImgRectValue = document.getElementById("chosenRectValue");
var chosenImgPie = document.getElementById("chosenPie");
var chosenImgThemeColor0 = document.getElementById("chosenImgThemeColor0");
var chosenImgThemeColorTitle0 = document.getElementById("chosenImgThemeColorTitle0");
var chosenImgThemeWeights0 = document.getElementById("chosenImgThemeWeights0");
var chosenImgThemeColor1 = document.getElementById("chosenImgThemeColor1");
var chosenImgThemeColorTitle1 = document.getElementById("chosenImgThemeColorTitle1");
var chosenImgThemeWeights1 = document.getElementById("chosenImgThemeWeights1");
var chosenImgInfo = document.getElementById("chosenImgInfo");

window.addEventListener('load', function() {
    advancedSearchTypeInitialization();
    titleContainerActivate();
});

window.onscroll = function() {
    titleContainerActivate();
}

divSearch.addEventListener("click", function() {
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
    idTextfield.value = regFileName.substring(4, regFileName.length - 2);

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
    idCurrentPointer.style.left = "252px";
}

function modeMatch() {
    divSearch.className = "linkTitle";
    divMatch.className = "currentLinkTitle";
    divAdvancedSearch.style.display = "none";
    idInputSearch.style.display = "none";
    idInputMatch.style.display = "block";
    idAdvancedSearchPanel.style.transform = "rotateX(90deg)";
    idCurrentPointer.style.left = "375px";
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

function getParameter(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var matched = window.location.search.substr(1).match(reg);
    if (matched != null) {
        return unescape(matched[2])
    }
    return null;
}

function advancedSearchTypeInitialization() {
    var advancedSearchTypeArray = new Array(advancedColorNum2, advancedColorNum3, advancedColorNum4, advancedColorNum5, advancedColorNumMore,
        advancedSaturationLow, advancedSaturationMiddle, advancedSaturationHigh, advancedBrightnessLow,
        advancedBrightnessMiddle, advancedBrightnessHigh, advancedIndustryBank, advancedIndustryStock,
        advancedIndustryIT, advancedIndustryManufacturing, advancedIndustryEducation);
    for (var x = 0; x < advancedSearchTypeArray.length; ++x) {
        (function() { // js的函数闭包问题
            var i = x;
            advancedSearchTypeArray[i].addEventListener("click", function() {
                switchAdvancedSearchType(this);
                if (i < 5) {
                    nColorsInput(i, this);
                } else if (i < 8) {
                    saturationInput(i - 5, this);
                } else if (i < 11) {
                    brightnessInput(i - 8, this);
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
            divResultContainer.style.marginTop = "120px";
        }
    } else {
        if (divTitleContainer.className == "titleContainerPassive") {
            divTitleContainer.className = "titleContainerDefault";
            divResultContainer.style.marginTop = "0px";
        }
    }
}

function nColorsInput (n, advancedColorNum) {
    var inputNColors = idNColors.value;
    inputNColors = advancedValueModification(n, inputNColors);
    idNColors.value = inputNColors;
}

function saturationInput(n, advancedSaturationNum) {
    var inputSaturation = idSaturation.value;
    inputSaturation = advancedValueModification(n, inputSaturation);
    idSaturation.value = inputSaturation;
}

function brightnessInput (n, advancedBrightnessNum) {
    var inputBrightness = idBrightness.value;
    inputBrightness = advancedValueModification(n, inputBrightness);
    idBrightness.value = inputBrightness;
}

function advancedValueModification (n, value) {
    var valueList = value.split(",");
    var nDigit = valueList[n];
    if (nDigit == "0") {
        valueList.splice(n, 1, "1");
    } else {
        valueList.splice(n, 1, "0");
    }
    value = valueList.join(",");
    return value;
}

function showChosenImgMoreInfo (pointer, mode) {
    // mode0 = matchedResult; mode1 = similarResult;
    if (mode == 0) {
        if (currentChosenImg == pointer) { // from active to passive
            currentChosenImg.className = "matchedResult";
            currentChosenImg = null;
            moveMoreInfoChosenImg(1);
            moveResultContainer(1);
        } else if (currentChosenImg != null) { // from active to active 
            currentChosenImg.className = "matchedResult";
            currentChosenImg = pointer;
            currentChosenImg.className = "matchedResultActive";
            fillMoreInfoChosenImg(pointer);
        } else {  // from passive to active
            currentChosenImg = pointer;
            currentChosenImg.className = "matchedResultActive";
            moveMoreInfoChosenImg(0);
            moveResultContainer(0);
            fillMoreInfoChosenImg(pointer);
        }
    } else {
        if (currentChosenImg == pointer) { // from active to passive
            currentChosenImg.className = "similarResult";
            currentChosenImg = null;
            moveMoreInfoChosenImg(1);
            moveResultContainer(1);
        } else if (currentChosenImg != null) { // from active to active 
            currentChosenImg.className = "similarResult";
            currentChosenImg = pointer;
            currentChosenImg.className = "similarResultActive";
            fillMoreInfoChosenImg(pointer);
        } else {  // from passive to active
            currentChosenImg = pointer;
            currentChosenImg.className = "similarResultActive";
            moveMoreInfoChosenImg(0);
            moveResultContainer(0);
            fillMoreInfoChosenImg(pointer);
        }
    }
}

function moveMoreInfoChosenImg(mode) {  
    // mode0 = left move; mode1 = right move;
    if (mode == 0) {
        if ( divChosenImg.className == "moreInfoChosenImgDivLeft") {
            divChosenImg.className = "moreInfoChosenImgDivDoubleLeft";
        } else {
            divChosenImg.className = "moreInfoChosenImgDivLeft";
        }
    } else {
        if ( divChosenImg.className == "moreInfoChosenImgDivDoubleLeft") {
            divChosenImg.className = "moreInfoChosenImgDivLeft";
        } else {
            divChosenImg.className = "moreInfoChosenImgDivDefault";
        }
    }
}

function moveResultContainer(mode) {  
    // mode0 = left move; mode1 = right move;
    if (mode == 0) {
        if ( divResultContainer.style.marginRight == "0px") {
            divResultContainer.style.marginRight = "250px";
        } else {
            divResultContainer.style.marginRight = "500px";
        }
    } else {
        if ( divResultContainer.style.marginRight == "500px") {
            divResultContainer.style.marginRight = "250px";
        } else {
            divResultContainer.style.marginRight = "0px";
        }
    }
}

function fillMoreInfoChosenImg (pointer) {
    chosenImg.src = "/static/" + pointer.getAttribute("dataFilename");
    chosenImgEntName.textContent = pointer.getAttribute("dataEntName");
    chosenImgSaturation.textContent = pointer.getAttribute("dataS");
    chosenImgValue.textContent = pointer.getAttribute("dataV");
    chosenImgRectSaturation.textContent = pointer.getAttribute("dataS");
    chosenImgRectValue.textContent = pointer.getAttribute("dataV");
    var chosenImgThemeColorsList = extractListElement(pointer.getAttribute("dataThemeColors"));
    var chosenImgThemeColorWeightsList = extractListElement(pointer.getAttribute("dataThemeWeights"));
    chosenImgPie.textContent = pointer.getAttribute("dataThemeWeights") + ", 800";
    chosenImgThemeColor0.style.backgroundColor = chosenImgThemeColorsList[0];
    chosenImgThemeColorTitle0.style.title = chosenImgThemeColorsList[0];
    chosenImgThemeWeights0.textContent = chosenImgThemeColorWeightsList[0];
    chosenImgThemeColor1.style.backgroundColor = chosenImgThemeColorsList[1];
    chosenImgThemeColorTitle1.style.title = chosenImgThemeColorsList[1];
    chosenImgThemeWeights1.textContent = chosenImgThemeColorWeightsList[1];
    chosenImgInfo.textContent = pointer.getAttribute("dataInfo");

    setRectLength(chosenImgRectSaturation);
    setRectLength(chosenImgRectValue);
}

function extractListElement (listInStr) {
    listInStr = listInStr.substring(1, listInStr.length-2); // cut the first and the last list sign
    var listCutted = listInStr.split(",");
    //alert(listCutted);
    return listCutted;
}

function setRectLength(rect) {
    var rectangleTmp = 111;
    setInterval(function() {
        var rectValue = rect.textContent;
        rect.style.width = Math.min(100, rectangleTmp) + "%";
        rectangleTmp = parseInt(rectangleTmp * 0.92 + (100 - rectValue * 100) * 0.08);
    }, 50);
}

// (function() {
//     var rectangleTmp = 111;
//     setInterval(function() {
//         var temp = document.getElementById("chosenRectSaturation")
//         var rectvalue = temp.textContent.split(":")[1];
//         temp.style = "width:" + Math.min(100,rectangleTmp) + "%";
//         rectangleTmp = parseInt(rectangleTmp * 0.92 + (100 - rectvalue * 100) * 0.08);
//     }, 50);
// })();

// (function() {
//     var rectangleTmp2 = 111;
//     setInterval(function() {
//         var temp2 = document.getElementById("chosenRectValue")
//         var rectvalue2 = temp2.textContent.split(":")[1];
//         temp2.style = "width:" + Math.min(100,rectangleTmp2) + "%";
//         rectangleTmp2 = parseInt(rectangleTmp2 * 0.92 + (100 - rectvalue2 * 100) * 0.08);
//     }, 50);
// })();

// function drawPie(pieNo,portion,colors){
// document.write('<span id="pie'+pieNo+'" class="pie">'+{{logo_matched[0].theme_weights | join(",")}}',800                            </span>")
jQuery(function() {
        function pieAnimation(pieNo) {
            var updatingChart = $("#chosenPie" + pieNo).peity("pie", { "fill": ["red", "green", "blue", "white"], "radius": 40 })
            setInterval(function() {
                var values = updatingChart.text().split(",");
                var tmp = values.pop();
                if (tmp > 100) {
                    tmp = tmp * 0.3;
                } else if (tmp > 0.1) {
                    tmp = tmp * 0.7;
                } else if (tmp > 0.05) {
                    tmp = tmp - 0.01;
                } else if (tmp > 0.00) {
                    tmp = tmp - 0.005;
                }
                values.push(tmp);
                updatingChart.text(values.join(",")).change();
            }, 64)
        };
        pieAnimation("1");
        pieAnimation("2");
    })
    // }