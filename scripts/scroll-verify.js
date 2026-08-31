/* Scroll-capture a book end to end at a given route, both themes.
   Written because the design pass that preceded it looked at a cover
   screenshot and stopped, and drew conclusions from that. */
const path=require('path'), fs=require('fs');
const {chromium}=require(require.resolve('playwright',{paths:['/opt/node22/lib/node_modules']}));
const CHROME='/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
(async()=>{
  const file=process.argv[2], out=process.argv[3], route=process.argv[4]||'#/';
  const dark=process.argv.includes('--dark');
  const w=+(process.argv.find(a=>a.startsWith('--w='))||'--w=1200').slice(4);
  const b=await chromium.launch({executablePath:CHROME});
  const c=await b.newContext({viewport:{width:w,height:900},isMobile:w<500,hasTouch:w<500,
    deviceScaleFactor:w<500?2:1});
  const p=await c.newPage();
  const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.goto('file://'+path.resolve(file)+route,{waitUntil:'load'});
  if(dark) await p.evaluate(()=>document.documentElement.classList.add('dark'));
  await p.waitForTimeout(500);
  const total=await p.evaluate(()=>document.body.scrollHeight);
  let i=0;
  for(let y=0;y<total && i<10;y+=850){
    await p.evaluate(yy=>window.scrollTo(0,yy),y);
    await p.waitForTimeout(260);
    await p.screenshot({path:`${out}-${String(i).padStart(2,'0')}.png`});
    i++;
  }
  console.log(`${path.basename(path.dirname(file))} ${route} ${dark?'dark':'light'} ${w}px: ${i} frames, ${total}px tall, ${errs.length?'ERRORS '+errs[0]:'no errors'}`);
  await b.close();
})();
