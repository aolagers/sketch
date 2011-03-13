$(document).ready(function() {

	var canvas;
	var ctx;
	var WIDTH;
	var HEIGHT;
	var mouse_x;
	var mouse_y;
	var mousePressed = false;
	
	function init() {
		canvas  = $('#draw-canvas');
		ctx = canvas[0].getContext("2d");
		WIDTH = canvas.width();
		HEIGHT = canvas.height();
	}

	function onMouseMove(evt) {
		mouse_last_x = mouse_x;
		mouse_last_y = mouse_y;

		mouse_x = evt.pageX - canvas.offset().left;
		mouse_y = evt.pageY - canvas.offset().top;

		$("#info").html("x: " + mouse_x + " y: " + mouse_y + " " + mousePressed);
		if (mousePressed) {
			ctx.beginPath();
			ctx.moveTo(mouse_last_x, mouse_last_y);
			ctx.lineTo(mouse_x, mouse_y);
			ctx.stroke();
			ctx.closePath();
		}
	}

	function onMouseDown(evt) {
		mousePressed = true;

	}
	function onMouseUp(evt) {
		mousePressed = false;
	}

	$("#draw-canvas").mousemove(onMouseMove);
	$("#draw-canvas").mousedown(onMouseDown);
	$("#draw-canvas").mouseup(onMouseUp);

	init();
	//init_mouse();



});
