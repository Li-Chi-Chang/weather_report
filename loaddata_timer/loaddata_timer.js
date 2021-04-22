import appid from './secrets'
import dirid from './secrets'

const locations = {
  'FortWayne':{'lat': 41.1306,'lon':-85.12886},
  'Taipei':{'lon': 121.651611,'lat': 25.025881}
}

function saveData(folder, filename, contents) {
  if(filename == '')
  {
    filename = 'testFile.txt'
  }
  let children = folder.getFilesByName(filename)
  console.log(children)
  let file = null
  if (children.hasNext()) {
    file = children.next()
    file.setContent(contents)
  } else {
    file = folder.createFile(filename, contents)
  }
}

function getWeather(time,location){
  let url = 'https://api.openweathermap.org/data/2.5/onecall/timemachine?lat='+location.lat+'&lon='+location.lon+'&dt='+time+'&appid='+appid
  let options = {
    'method': 'get',
  }
  return UrlFetchApp.fetch(url,options)
}

function getEachLocationWeatherWithTimer() {
  let today = new Date()
  let nowTime = Math.floor(today.getTime()/1000)
  for(location in locations){
    let output = getWeather(nowTime-60*60*13,locations[location])
    let folder = DriveApp.getFolderById(dirid) // database folder
    if (folder === undefined)
    {
      system.log("error")
    }
    saveData(folder,today.getUTCDate()+'_'+today.getUTCHours()+'_'+today.getUTCMinutes()+'_'+location+'.json',output)
  }
}