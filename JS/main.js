//INITIALISATIONS
const canvas=document.getElementById("mainboard");
const ctx=canvas.getContext("2d");
const undo_button=document.getElementById("undo-button");
const redo_button=document.getElementById("redo-button");
canvas.width=window.innerWidth;
canvas.height=window.innerHeight;
document.getElementById("pen-button").style="background: #e5e5e5;outline: none;-webkit-box-shadow: inset 0px 0px 5px #c1c1c1;-moz-box-shadow: inset 0px 0px 5px #c1c1c1;box-shadow: inset 0px 0px 5px #c1c1c1;"

var tcanvas = document.createElement('canvas');
var tctx = tcanvas.getContext('2d');
tcanvas.id = 'tcanvas';
tcanvas.width = canvas.width;
tcanvas.height = canvas.height;

sketching_area.appendChild(tcanvas);

var is_drawing=false;
var is_pen=true;

var points=[];
var redo_stack=[];
var current_stroke=[];

var colorButton = document.getElementById("color_picker");
var colorDiv = document.getElementById("color_val");

//SETTING DEFAULTS
var eraser_size=5//default
var pen_colour="#000000";
var pen_size=5;

ctx.lineWidth=pen_size;//default
ctx.lineCap="round";
ctx.strokeStyle=pen_colour;//default
ctx.lineJoin='round';

tctx.lineWidth=pen_size;//default
tctx.lineCap="round";
tctx.strokeStyle=pen_colour;//default
tctx.lineJoin='round';


function mouse_start_draw(e)
{
   is_drawing=true;
   tctx.beginPath();
   current_stroke=[];
   redo_stack=[];
   current_stroke.push
   (
      {
         x:e.offsetX,
         y:e.offsetY,
         width:ctx.lineWidth,
         color:ctx.strokeStyle
      }
   );

}

function collapse_menus()
{
   document.getElementById("sections_panel").style.height="0px";
   document.getElementById("sections_panel_1").style.height="0px";
}

function mouse_stop_draw(e)
{
   is_drawing=false;
   current_stroke.push
   (
      {
         x:e.offsetX,
         y:e.offsetY,
         width:ctx.lineWidth,
         color:ctx.strokeStyle
      }
   );
   ctx.drawImage(tcanvas, 0, 0);
    tctx.clearRect(0, 0, tcanvas.width, tcanvas.height);
   tcanvas.removeEventListener('mousemove', mouse_draw);
   points.push(current_stroke);
   current_stroke=[];
}

function mouse_draw(e)
{
   if(!is_drawing)
   return;

   if(is_pen)
   {
      current_stroke.push
   (
      {
         x:e.offsetX,
         y:e.offsetY,
         width:ctx.lineWidth,
         color:ctx.strokeStyle
      }
   );

      if (current_stroke.length < 3) {
         var b = current_stroke[0];
         tctx.beginPath();
         tctx.arc(b.x, b.y, tctx.lineWidth / 2, 0, Math.PI * 2, !0);
         tctx.fill();
         tctx.closePath();
         return;
       }
       
       // Tmp canvas is always cleared up before drawing.
       tctx.clearRect(0, 0, tcanvas.width, tcanvas.height);
       
       tctx.beginPath();
       tctx.moveTo(current_stroke[0].x, current_stroke[0].y);
       
       for (var i = 1; i < current_stroke.length - 2; i++) {
         var c = (current_stroke[i].x + current_stroke[i + 1].x) / 2;
         var d = (current_stroke[i].y + current_stroke[i + 1].y) / 2;
         
         tctx.quadraticCurveTo(current_stroke[i].x, current_stroke[i].y, c, d);
       }
       
       // For the last 2 points
       tctx.quadraticCurveTo(
         current_stroke[i].x,
         current_stroke[i].y,
         current_stroke[i + 1].x,
         current_stroke[i + 1].y
       );
       tctx.stroke();
       
     }
   else
   {
      //ctx.clearRect(e.clientX-eraser_size, e.clientY-eraser_size-56, 2*eraser_size, 2*eraser_size);
      //its still an issue
   }

}

function undo()
{
   if(points.length<1)
   return;

   var last_stroke=points.pop();
   redo_stack.push(last_stroke);
   redraw_all();
}

function redo()
{
   if(redo_stack.length<1)
   return;
   var last_stroke=redo_stack.pop();
   points.push(last_stroke);
   redraw_all();
}

function redraw_all()
{
   ctx.clearRect(0,0,canvas.width,canvas.height);

   for(var j=0; j<points.length ; j++)
      {
         var Stroke=points[j];
         ctx.lineWidth=Stroke[0].width;
         ctx.strokeStyle=Stroke[0].color;
         ctx.beginPath();
         ctx.moveTo(Stroke[0].x, Stroke[0].y);
             
         if (Stroke.length < 3) {
            var b = Stroke[0];
            ctx.beginPath();
            
            ctx.arc(b.x, b.y, ctx.lineWidth / 2, 0, Math.PI * 2, !0);
            ctx.fill();
            ctx.closePath();
            continue;
          }

         for (var i = 1; i < Stroke.length - 2; i++) {
         var c = (Stroke[i].x + Stroke[i + 1].x) / 2;
         var d = (Stroke[i].y + Stroke[i + 1].y) / 2;
         
         ctx.quadraticCurveTo(Stroke[i].x, Stroke[i].y, c, d);
         }
         
         // For the last 2 points
         ctx.quadraticCurveTo(
         Stroke[i].x,
         Stroke[i].y,
         Stroke[i + 1].x,
         Stroke[i + 1].y
         );
         ctx.stroke();
   }
}

function ClearAll()
{
   console.log(points);
   ctx.clearRect(0,0,canvas.width,canvas.height);
   points=[];
   
}

function selectPen()
{
   if(is_pen==false)
   {
      is_pen=true;
      document.getElementById("pen-button").style="background: #e5e5e5;outline: none;-webkit-box-shadow: inset 0px 0px 5px #c1c1c1;-moz-box-shadow: inset 0px 0px 5px #c1c1c1;box-shadow: inset 0px 0px 5px #c1c1c1;"
      document.getElementById("eraser-button").style="";
   }
   else
   {
      //show sizes and colour
      var panel = document.getElementById("sections_panel");
      var maxH="150px";
      if(panel.style.height == maxH){
          panel.style.height = "0px";
      } else {
          panel.style.height = maxH;
      }
     }
}

function selectEraser()
{
   if(is_pen==true)
   {
   is_pen=false;
   document.getElementById("eraser-button").style="background: #e5e5e5;outline: none;-webkit-box-shadow: inset 0px 0px 5px #c1c1c1;-moz-box-shadow: inset 0px 0px 5px #c1c1c1;box-shadow: inset 0px 0px 5px #c1c1c1;";
   document.getElementById("pen-button").style="";

   }
   else
   {
      //show sizes option
    var panel = document.getElementById("sections_panel_1");
    var maxH="150px";
    if(panel.style.height == maxH){
        panel.style.height = "0px";
    } else {
        panel.style.height = maxH;
    }
   }
}


canvas.addEventListener("mousedown",mouse_start_draw);
canvas.addEventListener("mouseup",mouse_stop_draw);
canvas.addEventListener("mousemove",mouse_draw);
undo_button.addEventListener("mouseenter",function()
{
   if(points.length==0)
      undo_button.style.cursor="not-allowed"
   else
      undo_button.style.cursor="hand";
})
redo_button.addEventListener("mouseenter",function()
{
   if(redo_stack.length==0)
      redo_button.style.cursor="not-allowed";
   else
      redo_button.style.cursor="hand";

})
document.getElementById("toolbar").addEventListener("mousedown",collapse_menus);
colorButton.onchange = function() {
   console.log(colorButton.value);
   ctx.strokeStyle=colorButton.value;
}
