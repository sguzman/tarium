import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {runInNewContext} from "node:vm";
import {test} from "node:test";

const source = readFileSync(new URL("../site/theme.js",import.meta.url),"utf8");

function setup({saved=null,dark=false,storageFails=false,legacyMedia=false}={}) {
  const elements = new Map();
  const events = {};
  const attributes = {};
  const meta = {setAttribute(k,v){this[k]=v;}};
  const root = {setAttribute(k,v){attributes[k]=v;}};
  const select = {
    value:"system",
    addEventListener(type,fn){events["select:"+type]=fn;},
  };
  const media = {matches:dark};
  if(legacyMedia) media.addListener=fn=>events.media=fn;
  else media.addEventListener=(type,fn)=>{events["media:"+type]=fn;};
  const kv = new Map(saved===null?[]:[["tarium:theme-mode",saved]]);
  const storage = {
    getItem(key){if(storageFails)throw Error("blocked");return kv.get(key)||null;},
    setItem(key,value){if(storageFails)throw Error("blocked");kv.set(key,value);},
    removeItem(key){if(storageFails)throw Error("blocked");kv.delete(key);}
  };
  const document = {
    documentElement:root,
    querySelector(q){return q==='meta[name="theme-color"]'?meta:null;},
    getElementById(q){return elements.get(q)||null;},
    addEventListener(type,fn){events[type]=fn;},
  };
  runInNewContext(source,{document,window:{matchMedia:()=>media},localStorage:storage,Set});
  elements.set("theme-mode",select);
  events.DOMContentLoaded();
  const choose=value=>{select.value=value;events["select:change"]();};
  const systemChange=value=>{
    media.matches=value;
    (events["media:change"]||events.media)();
  };
  return {attributes,meta,select,kv,choose,systemChange};
}

test("system preference initializes before paint and responds to live browser changes",()=>{
  const x=setup({dark:false});
  assert.equal(x.attributes["data-theme"],"light");
  assert.equal(x.select.value,"system");
  assert.equal(x.meta.content,"#f3f1eb");
  x.systemChange(true);
  assert.equal(x.attributes["data-theme"],"dark");
  assert.equal(x.meta.content,"#10191c");
  x.systemChange(false);
  assert.equal(x.attributes["data-theme"],"light");
});

test("manual override ignores system events and survives new visits",()=>{
  const x=setup({dark:true});
  x.choose("light");
  assert.equal(x.attributes["data-theme"],"light");
  assert.equal(x.kv.get("tarium:theme-mode"),"light");
  x.systemChange(false);x.systemChange(true);
  assert.equal(x.attributes["data-theme"],"light");
  const y=setup({saved:x.kv.get("tarium:theme-mode"),dark:true});
  assert.equal(y.attributes["data-theme"],"light");
  y.choose("dark");
  assert.equal(y.attributes["data-theme"],"dark");
  y.systemChange(false);
  assert.equal(y.attributes["data-theme"],"dark");
  y.choose("system");
  assert.equal(y.kv.has("tarium:theme-mode"),false);
  assert.equal(y.attributes["data-theme"],"light");
  y.systemChange(true);
  assert.equal(y.attributes["data-theme"],"dark");
});

test("blocked storage and older change listener remain functional",()=>{
  const x=setup({dark:true,storageFails:true,legacyMedia:true});
  assert.equal(x.attributes["data-theme"],"dark");
  x.choose("light");
  assert.equal(x.attributes["data-theme"],"light");
  x.choose("system");x.systemChange(false);
  assert.equal(x.attributes["data-theme"],"light");
});

test("unsupported stored theme is ignored",()=>{
  const x=setup({saved:"strange",dark:true});
  assert.equal(x.select.value,"system");
  assert.equal(x.attributes["data-theme"],"dark");
  x.choose("strange");
  assert.equal(x.select.value,"strange");
  assert.equal(x.attributes["data-theme"],"dark");
});

test("all page sections, cards, orbit, and theme control have theme styling",()=>{
  const css=readFileSync(new URL("../site/styles.css",import.meta.url),"utf8");
  for(const selector of [
    'html[data-theme="dark"] .collection-section',
    'html[data-theme="dark"] .project-card',
    'html[data-theme="dark"] .card-body h3',
    'html[data-theme="light"] .dark-region',
    'html[data-theme="light"] .orbit-project-face',
    'html[data-theme="light"] .principles-section',
    'html[data-theme="light"] .site-footer',
    '.theme-control select'
  ])assert.ok(css.includes(selector),selector);
});
