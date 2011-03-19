$(document).ready(function() {

	$("#sketch-id-lookup").click(function() {
		$(this).val("");
		$(this).css("color", "black");
	});

	var canvas;
	var ctx;
	var WIDTH;
	var HEIGHT;
	var mouse_x;
	var mouse_y;
	var mousePressed = false;
    var tool = "pen";

	$( "#slider" ).slider();/*{
		value: 1,
		min: 1,
        max: 10,
        step: 1,
		slide: function( event, ui ) {
			$( "#info" ).html( ui.value );
            ctx.lineWidth = ui.value;
		}
	});
      */

	function init() {
		canvas  = $('#draw-canvas');
		ctx = canvas[0].getContext("2d");
        ctx.lineCap = "round";
		WIDTH = canvas.width();
		HEIGHT = canvas.height();

		ctx.lineWidth = 2;
        $("#pen").css("font-weight", "bold");
        ctx.globalCompositeOperation = "copy";
	}

    $("#pen").click(function() {
      tool = "pen";
      $("#pen").css("font-weight", "bold");
      $("#eraser").css("font-weight", "normal");
      ctx.strokeStyle = "rgba(1, 1, 1, 1)";
      $("#info").val( tool  );
    });
    $("#eraser").click(function() {
      tool = "eraser";
      $("#pen").css("font-weight", "normal");
      $(this).css("font-weight", "bold");
      ctx.strokeStyle = "rgba(255, 0, 0, 0)";
      $("#info").val( tool  );
    });
    $("#grow").click(function() {
      ctx.lineWidth += 1;
      $("#pensize").val( ctx.lineWidth  );
    });
    $("#shrink").click(function() {
      ctx.lineWidth -= 1;
      $("#pensize").val( ctx.lineWidth  );
    });

	function onMouseMove(evt) {
		mouse_last_x = mouse_x;
		mouse_last_y = mouse_y;

		mouse_x = evt.pageX - canvas.offset().left;
		mouse_y = evt.pageY - canvas.offset().top;

		if (mousePressed) {
			ctx.moveTo(mouse_last_x, mouse_last_y);
			ctx.lineTo(mouse_x, mouse_y);
			ctx.stroke();
		}

	}

	function onMouseDown(evt) {
      ctx.beginPath();
      mousePressed = true;

	}

	function onMouseUp(evt) {
      mousePressed = false;
      ctx.closePath();
	}

	$("#draw-canvas").mousemove(onMouseMove);
	$("#draw-canvas").mousedown(onMouseDown);
	$("html").mouseup(onMouseUp);

	init();

	$("#save-button").click(function() {
		var c = document.getElementById("draw-canvas");
		var img = c.toDataURL("image/png");
		var token;
		var sketch_id = 0;

		if (document.cookie && document.cookie != "") {
			cookies = document.cookie.split(";");
			for (i = 0; i < cookies.length; i++) {
				cookie = $.trim(cookies[i]);
				if (cookie.substring(0, 10) == "csrftoken=") {
					token = decodeURIComponent(cookie.substring(10));
					break;
				}
			}
		}

		$.ajax({
			url: "/save/",
			type: "POST",
			dataType: "json",
			data: {"img" : img},
			headers: {"X-CSRFToken" : token },
			async: false,
			success: function( response ){
				sketch_id = response["sketch_id"];
				$("#sketch-id-input").val(sketch_id);
			}
		});

		return true;
	});


});
