const path=require('path'), fs=require('fs');
const {chromium}=require(require.resolve('playwright',{paths:['/opt/node22/lib/node_modules']}));
const CHROME=['/opt/pw-browsers/chromium-1194/chrome-linux/chrome'].find(p=>fs.existsSync(p));
(async()=>{
  const file=process.argv[2], out=process.argv[3], routes=(process.argv[4]||'#/').split(',');
  const b=await chromium.launch({executablePath:CHROME});
  for(const vp of [{n:'m',w:390,h:844,mob:true},{n:'d',w:1440,h:900}]){
    const c=await b.newContext({viewport:{width:vp.w,height:vp.h},isMobile:vp.mob,hasTouch:vp.mob,deviceScaleFactor:vp.mob?2:1});
    const p=await c.newPage();
    for(const r of routes){
      await p.goto('file://'+path.resolve(file)+r,{waitUntil:'load'});
      await p.waitForTimeout(300);
      const tag=r.replace(/[#/]/g,'')||'hub';
      await p.screenshot({path:`${out}-${vp.n}-${tag}.png`, fullPage:false});
    }
    await c.close();
  }
  await b.close(); console.log('shot '+out);
})();
