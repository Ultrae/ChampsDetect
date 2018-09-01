// Copyright 2010 William Malone (www.williammalone.com)
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

var canvas;
var context;
var canvasWidth = 520;
var canvasHeight = 520;
var padding = 30;
var lineWidth = 200;
var colorPurple = "#c50013";
var colorGreen = "#659b41";
var colorYellow = "#ffcf33";
var colorBrown = "#986928";
var outlineImage = new Image();
var crayonImage = new Image();
var markerImage = new Image();
var eraserImage = new Image();
var crayonBackgroundImage = new Image();
var markerBackgroundImage = new Image();
var eraserBackgroundImage = new Image();
var crayonTextureImage = new Image();
var clickX = new Array();
var clickY = new Array();
var clickColor = new Array();
var clickTool = new Array();
var clickSize = new Array();
var clickDrag = new Array();
var paint = false;
var curColor = colorPurple;
var curTool = "marker";
var curSize = "huge";
var mediumStartX = 18;
var mediumStartY = 19;
var mediumImageWidth = 93;
var mediumImageHeight = 46;
var drawingAreaX = 18;
var drawingAreaY = 18;
var drawingAreaWidth = 484;
var drawingAreaHeight = 484;
var toolHotspotStartY = 0;
var totalLoadResources = 8;
var curLoadResNum = 0;

function click_paint() {
    curTool = "marker";
}

function click_erase() {
    curTool = "eraser";
}

/**
 * Calls the redraw function after all neccessary resources are loaded.
 */
function resourceLoaded() {
    if (++curLoadResNum >= totalLoadResources) {
        redraw();
    }
}

/**
 * Creates a canvas element, loads images, adds events, and draws the canvas for the first time.
 */
function prepareCanvas() {
    // Create the canvas (Neccessary for IE because it doesn't know what a canvas element is)
    var canvasDiv = document.getElementById('canvasDiv');
    canvas = document.createElement('canvas');
    canvas.setAttribute('width', canvasWidth);
    canvas.setAttribute('height', canvasHeight);
    canvas.setAttribute('id', 'canvas');
    canvasDiv.appendChild(canvas);
    if (typeof G_vmlCanvasManager != 'undefined') {
        canvas = G_vmlCanvasManager.initElement(canvas);
    }
    context = canvas.getContext("2d"); // Grab the 2d canvas context
    // Note: The above code is a workaround for IE 8 and lower. Otherwise we could have used:
    //     context = document.getElementById('canvas').getContext("2d");

    // Load images
    // -----------
    crayonImage.onload = function () {
        resourceLoaded();
    };
    crayonImage.src = "/static/images/blank.png";

    markerImage.onload = function () {
        resourceLoaded();
    };
    markerImage.src = "/static/images/blank.png";
    context.drawImage(markerImage, 0, 0, 100, 100);

    eraserImage.onload = function () {
        resourceLoaded();
    };
    eraserImage.src = "/static/images/blank.png";

    crayonBackgroundImage.onload = function () {
        resourceLoaded();
    };
    crayonBackgroundImage.src = "/static/images/crayon-background.png";

    markerBackgroundImage.onload = function () {
        resourceLoaded();
    };
    markerBackgroundImage.src = "/static/images/marker-background.png";

    eraserBackgroundImage.onload = function () {
        resourceLoaded();
    };
    eraserBackgroundImage.src = "/static/images/eraser-background.png";

    crayonTextureImage.onload = function () {
        resourceLoaded();
    };
    crayonTextureImage.src = "/static/images/blank.png";

    outlineImage.onload = function () {
        resourceLoaded();
    };
    outlineImage.src = "/static/images/blank.png";

    // Add mouse events
    // ----------------
    $('#canvas').mousedown(function (e) {
        // Mouse down location
        var mouseX = e.pageX - this.offsetLeft;
        var mouseY = e.pageY - this.offsetTop;

        if (mouseX < drawingAreaX) // Left of the drawing area
        {
            if (mouseX > mediumStartX) {
                if (mouseY > mediumStartY && mouseY < mediumStartY + mediumImageHeight) {
                    curColor = colorPurple;
                } else if (mouseY > mediumStartY + mediumImageHeight && mouseY < mediumStartY + mediumImageHeight * 2) {
                    curColor = colorGreen;
                } else if (mouseY > mediumStartY + mediumImageHeight * 2 && mouseY < mediumStartY + mediumImageHeight * 3) {
                    curColor = colorYellow;
                } else if (mouseY > mediumStartY + mediumImageHeight * 3 && mouseY < mediumStartY + mediumImageHeight * 4) {
                    curColor = colorBrown;
                }
            }
        }
        else if (mouseX > drawingAreaX + drawingAreaWidth) // Right of the drawing area
        {
            if (mouseY > toolHotspotStartY) {
            }
        }
        else if (mouseY > drawingAreaY && mouseY < drawingAreaY + drawingAreaHeight) {
            // Mouse click location on drawing area
        }
        paint = true;
        addClick(mouseX, mouseY, false);
        redraw();
    });

    $('#canvas').mousemove(function (e) {
        if (paint == true) {
            addClick(e.pageX - this.offsetLeft, e.pageY - this.offsetTop, true);
            redraw();
        }
    });

    $('#canvas').mouseup(function (e) {
        paint = false;
        redraw();
    });

    $('#canvas').mouseleave(function (e) {
        paint = false;
    });
}

/**
 * Adds a point to the drawing array.
 * @param x
 * @param y
 * @param dragging
 */
function addClick(x, y, dragging) {
    clickX.push(x);
    clickY.push(y);
    clickTool.push(curTool);
    clickColor.push(curColor);
    clickSize.push(curSize);
    clickDrag.push(dragging);
}

/**
 * Clears the canvas.
 */
function clearCanvas() {
    context.clearRect(0, 0, canvasWidth, canvasHeight);
}

/**
 * Redraws the canvas.
 */
function redraw() {
    // Make sure required resources are loaded before redrawing
    if (curLoadResNum < totalLoadResources) {
        return;
    }

    clearCanvas();

    var locX;
    var locY;

    // Draw the marker tool background
    context.drawImage(markerBackgroundImage, 0, 0, canvasWidth, canvasHeight);


    // Keep the drawing in the drawing area
    context.save();
    context.beginPath();
    context.rect(drawingAreaX, drawingAreaY, drawingAreaWidth, drawingAreaHeight);
    context.clip();

    var i = 0;
    for (; i < clickX.length; i++) {

        context.beginPath();
        if (clickDrag[i] && i) {
            context.moveTo(clickX[i - 1], clickY[i - 1]);
        } else {
            context.moveTo(clickX[i], clickY[i]);
        }
        context.lineTo(clickX[i], clickY[i]);
        context.closePath();

        if (clickTool[i] == "eraser") {
            context.globalCompositeOperation = "destination-out"; // To erase instead of draw over with white
            context.strokeStyle = 'white';
        } else {
            context.globalCompositeOperation = "source-over";	// To erase instead of draw over with white
            context.strokeStyle = clickColor[i];
        }
        context.lineJoin = "round";
        context.lineWidth = 50;
        context.stroke();

    }
    //context.globalCompositeOperation = "source-over";// To erase instead of draw over with white
    context.restore();
    context.globalAlpha = 1; // No IE support
}


/**/