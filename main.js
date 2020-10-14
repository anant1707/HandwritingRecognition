const electron= require("electron");
const app=electron.app;
const BrowserWindow=electron.BrowserWindow;

var mainWindow=null;

app.on("ready",function()
{
    mainWindow=new BrowserWindow(
        {
            width:1080,
            height:720
        });
    mainWindow.loadFile("src/index.html");
});
