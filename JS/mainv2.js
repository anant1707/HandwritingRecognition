//INITIALISATIONS
const canvas=document.getElementById("mainboard");
const ctx=canvas.getContext("2d");
const undo_button=document.getElementById("undo-button");
const redo_button=document.getElementById("redo-button");
canvas.width=window.innerWidth;
canvas.height=window.innerHeight;

var shiftY=0;

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
var pen_size=10;

ctx.lineWidth=pen_size;//default
ctx.lineCap="round";
ctx.strokeStyle=pen_colour;//default
ctx.lineJoin='round';


function start_draw(e)
{
   is_drawing=true;
   current_stroke=[];
   current_stroke.push(
       {
           x:e.clientX,
           y:e.clientY+shiftY
       }
   );
   ctx.beginPath();
}
function stop_draw()
{
   is_drawing=false;
   points.push(current_stroke);
}
function draw(e)
{
   if(!is_drawing)
   return;

   if(is_pen)
   {
    current_stroke.push(
        {
            x:e.clientX,
            y:e.clientY+shiftY
        }
    );
   ctx.lineTo(e.clientX,e.clientY);
   ctx.stroke();
   }
   else
   {
      ctx.clearRect(e.clientX-eraser_size,e.clientY-eraser_size,eraser_size,eraser_size);
   }
}

function collapse_menus()
{
   document.getElementById("sections_panel").style.height="0px";
   document.getElementById("sections_panel_1").style.height="0px";
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

    for(var i=0;i<points.length;i++)
    {
        var Stroke=points[i];
        ctx.moveTo(Stroke[0].x,Stroke[0].y-shiftY);
        ctx.beginPath();
        for(var j=1;j<Stroke.length;j++)
        {
            if(Stroke[j].y-shiftY>=0 && Stroke[j].y-shiftY<=canvas.height)
            {
            ctx.lineTo(Stroke[j].x,Stroke[j].y-shiftY);
            ctx.stroke();
            }
            
        }
        ctx.stroke();
    }
    
}

function ClearAll()
{
   console.log(points);
   ctx.clearRect(0,0,canvas.width,canvas.height);
   points=[];
   
}

function scroll(e)
{
    shiftY+=e.deltaY*0.5;
    if(shiftY<=0)
    shiftY=0;
    redraw_all();
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


canvas.addEventListener("mousedown",start_draw);
canvas.addEventListener("mouseup",stop_draw);
canvas.addEventListener("mousemove",draw);
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
canvas.addEventListener("wheel",scroll);
document.getElementById("toolbar").addEventListener("mousedown",collapse_menus);
colorButton.onchange = function() {
   console.log(colorButton.value);
   ctx.strokeStyle=colorButton.value;
}
