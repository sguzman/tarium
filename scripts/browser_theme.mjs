import assert from "node:assert/strict";
import {existsSync} from "node:fs";
import {chromium} from "playwright-core";

const executablePath = [
  "/usr/bin/google-chrome",
  "/usr/bin/google-chrome-stable",
  "/usr/bin/chromium"
].find(existsSync);
assert.ok(executablePath,"A headless Chrome or Chromium executable is required");

const browser = await chromium.launch({
  executablePath,headless:true,args:["--no-sandbox"]
});
const errors=[];
const base="http://127.0.0.1:8766/";
try {
  const context=await browser.newContext({viewport:{width:1440,height:900},colorScheme:"dark"});
  const page=await context.newPage();
  page.on("pageerror",e=>errors.push(e.message));
  await page.goto(base,{waitUntil:"load"});
  await page.locator(".project-card").first().waitFor();

  const select=page.locator("#theme-mode");
  assert.equal(await select.isVisible(),true,"The appearance selector must be visible in the header");
  assert.equal(await select.inputValue(),"system","System must be the default");
  assert.deepEqual(await select.locator("option").evaluateAll(
    nodes=>nodes.map(x=>x.value)),["system","light","dark"]);
  assert.equal(await page.locator("html").getAttribute("data-theme"),"dark");

  const regions=[".collection-section",".principles-section",".site-footer",".project-card"];
  const visualState=async()=>page.evaluate(selectors=>{
    const colors={};
    const rgb=css=>css.match(/[0-9]+(?:[.][0-9]+)?/g)?.slice(0,3).map(Number)||[];
    for(const selector of selectors){
      const el=document.querySelector(selector);
      if(!el)throw new Error("Missing visual region: "+selector);
      const style=getComputedStyle(el);
      const color=rgb(style.backgroundColor);
      colors[selector]=color;
    }
    colors.hero=getComputedStyle(document.querySelector(".dark-region")).backgroundImage;
    return colors;
  },regions);
  const dark=await visualState();
  for(const selector of regions){
    assert.equal(dark[selector].length,3,"No background for "+selector);
    assert.ok(Math.max(...dark[selector])<100,"Dark mode region is too light: "+selector+" "+dark[selector]);
  }

  await select.selectOption("light");
  assert.equal(await page.locator("html").getAttribute("data-theme"),"light");
  const light=await visualState();
  for(const selector of regions){
    assert.ok(Math.min(...light[selector])>175,
      "Light mode region remains dark: "+selector+" "+light[selector]);
  }
  assert.notEqual(light.hero,dark.hero,"Hero background must change with theme");
  await page.reload({waitUntil:"load"});
  assert.equal(await select.inputValue(),"light","Manual override must persist");
  assert.equal(await page.locator("html").getAttribute("data-theme"),"light");

  await select.selectOption("dark");
  await page.emulateMedia({colorScheme:"light"});
  assert.equal(await page.locator("html").getAttribute("data-theme"),"dark",
    "Manual theme must not follow system changes");
  await select.selectOption("system");
  assert.equal(await page.locator("html").getAttribute("data-theme"),"light");
  await page.emulateMedia({colorScheme:"dark"});
  assert.equal(await page.locator("html").getAttribute("data-theme"),"dark",
    "System preference must react without a page reload");

  await page.setViewportSize({width:390,height:844});
  assert.equal(await select.isVisible(),true,"Appearance control must remain visible on mobile");
  const rect=await select.boundingBox();
  assert.ok(rect && rect.x>=0 && rect.x+rect.width<=390,
    "The appearance control must fit within the mobile viewport");
  assert.equal(errors.length,0,"Browser errors: "+errors.join("; "));
  console.log("Real-browser theme QA passed: visible control, complete light/dark pages, live system changes, persistence, mobile layout.");
}finally{
  await browser.close();
}
