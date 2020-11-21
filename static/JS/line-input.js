const canvas=document.getElementById("line-input");
const txtarea=document.getElementById("txtarea");
const ctx=canvas.getContext("2d");



canvas.width=window.innerWidth;
canvas.height=(window.innerHeight * 0.35);
txtarea.style.setProperty('width',`${window.innerWidth}px`,'');
txtarea.style.setProperty('height',`${window.innerHeight-canvas.height}px`,'');


var is_drawing=false;

// Containers for storing coordinates
var points=[];
var redo_stack=[];
var current_stroke=[];


//Setting Default
var eraser_size=5//default
var pen_colour="#000000";
var pen_size=3;
ctx.lineWidth=pen_size;//default
ctx.lineCap="round";
ctx.strokeStyle=pen_colour;//default
ctx.lineJoin='round';


function mouse_start_draw(e)
{
   is_drawing=true;
   ctx.beginPath();
   current_stroke=[];
   redo_stack=[];
   current_stroke.push
   (
      {
         x:e.offsetX,
         y:e.offsetY
      }
   );

}

function mouse_stop_draw(e)
{
   is_drawing=false;
   current_stroke.push
   (
      {
         x:e.offsetX,
         y:e.offsetY
      }
   );

   points.push(current_stroke);
   current_stroke=[];
}

function mouse_draw(e)
{
   if(!is_drawing)
   return;

    current_stroke.push
   (
      {
         x:e.offsetX,
         y:e.offsetY
      }
   );

   ctx.lineTo(e.offsetX,e.offsetY);
   ctx.stroke();
   

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
   ctx.beginPath()
   ctx.clearRect(0,0,canvas.width,canvas.height);
   for (var i=0; i<points.length; i++)
   {
    ctx.lineTo(points[i].x,points[i].y);
    ctx.stroke();
   }
}

function ClearAll()
{
   ctx.clearRect(0,0,canvas.width,canvas.height);
   points=[];
}


canvas.addEventListener("mousedown",mouse_start_draw);
canvas.addEventListener("mouseup",mouse_stop_draw);
canvas.addEventListener("mousemove",mouse_draw);
