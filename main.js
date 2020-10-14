const {dialog}= require("electron");
var electron=require("electron");
const fs = require("fs");
const app=electron.app;
const BrowserWindow=electron.BrowserWindow;
const ipc=electron.ipcMain;
var mainWindow=null;

app.on("ready",function()
{
    mainWindow=new BrowserWindow(
        {
            width:1080,
            height:720,
            webPreferences: 
            {
            nodeIntegration: true
            }
        });
    mainWindow.loadFile("src/index.html");
});

ipc.on('save-this-file', (event,arg)=>
{

    dialog.showOpenDialog({properties: ['openDirectory']}).then(result=>{
        var folder=result.filePaths;
        fs.writeFileSync(folder+'////data.wbd', JSON.stringify(arg,null,2) , 'utf-8');
    })
});