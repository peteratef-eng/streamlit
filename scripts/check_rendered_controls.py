"""Rendered route/control regression check. Dev-only: requires Playwright + Chromium.
Run: python scripts/check_rendered_controls.py --base-url http://localhost:8501
Start Streamlit separately. Does not click external links or submit forms.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROUTES = ('', 'projects', 'weather_pipeline', 'weather_dashboard', 'project_overview',
          'market_dashboard', 'data_pipeline', 'data_quality', 'ecommerce_overview',
          'ecommerce_dashboard', 'about', 'experience', 'skills', 'contact')
SELECTOR = '[role=option], [role=gridcell], [role=spinbutton], [data-testid=stMultiSelect], [data-testid=stSelectbox], [role=tab], [role=switch], [data-testid=stDateInputField], button, a.pa-button, a.portfolio-button, a.contact-card-action, [data-testid="stPageLink"] a'
INSPECT = r'''els => {
 const rgba = s => {const m=s.match(/[\d.]+/g);return m ? m.map(Number):[0,0,0,0]};
 const over=(fg,bg)=>{const a=fg[3]===undefined?1:fg[3];return [0,1,2].map(i=>fg[i]*a+bg[i]*(1-a)).concat(1)};
 const background=el=>{const chain=[];for(let p=el;p;p=p.parentElement)chain.unshift(p);return chain.reduce((bg,p)=>{bg=over(rgba(getComputedStyle(p).backgroundColor),bg);for(const pseudo of ['::before','::after']){const layer=getComputedStyle(p,pseudo);if(layer.content!=='none'&&layer.content!=='normal')bg=over(rgba(layer.backgroundColor),bg);}return bg},[15,23,42,1])};
 const lum=c=>c.slice(0,3).map(v=>v/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4).reduce((s,v,i)=>s+v*[.2126,.7152,.0722][i],0);
 const contrast=(a,b)=>{const x=lum(a),y=lum(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05)};
 return els.map(el=>{
  const rect=el.getBoundingClientRect(),style=getComputedStyle(el);
  if(!rect.width||!rect.height||style.visibility==='hidden'||el.closest('[aria-hidden="true"]'))return null;
  for(let p=el;p;p=p.parentElement){const s=getComputedStyle(p);if(s.clipPath==='inset(50%)'||s.clip==='rect(0px, 0px, 0px, 0px)')return null;}
  // The collapsed responsive sidebar remains mounted offscreen.
  const sidebar=el.closest('[data-testid="stSidebar"]');if(sidebar&&sidebar.getBoundingClientRect().right<=5)return null;
  const walker=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);const text=[];let node;
  while(node=walker.nextNode()){
   if(!node.textContent.trim()||node.parentElement.closest('svg,[data-testid="stIconMaterial"],script,style'))continue;
   const range=document.createRange();range.selectNodeContents(node);const r=range.getBoundingClientRect();if(!r.width||!r.height)continue;
   const p=node.parentElement,s=getComputedStyle(p),bg=background(p);let opacity=1;for(let a=p;a;a=a.parentElement)opacity*=Number(getComputedStyle(a).opacity);
   const fg=rgba(s.color);fg[3]=(fg[3]===undefined?1:fg[3])*opacity;
   text.push({text:node.textContent.trim(),ratio:contrast(over(fg,bg),bg),color:s.color,background:bg.slice(0,3),opacity});
  }
  if(el.matches('input') && el.value){const s=getComputedStyle(el),bg=background(el);text.push({text:el.value,ratio:contrast(over(rgba(s.color),bg),bg),color:s.color,background:bg.slice(0,3),opacity:1})}
  const icon=!!el.querySelector('svg,[data-testid="stIconMaterial"]');
  const name=el.getAttribute('aria-label')||el.getAttribute('title')||'';
  return {tag:el.tagName,classes:el.className,text:text.map(x=>x.text).join(' '),fragments:text,iconOnly:!text.length&&(icon||el.matches('[role=switch]')),name,disabled:el.disabled||el.getAttribute('aria-disabled')==='true'};
 }).filter(Boolean)
}'''

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--base-url',default='http://localhost:8501');parser.add_argument('--output',default='/tmp/rendered-control-results.json');args=parser.parse_args()
    results=[];failures=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
        for width in (1440,390):
            page=browser.new_page(viewport={'width':width,'height':900})
            for route in ROUTES:
                page.goto(args.base_url.rstrip('/')+'/'+route)
                page.locator('[data-testid="stAppViewContainer"]').wait_for();page.wait_for_timeout(1100)
                try:page.locator('[data-testid="stStatusWidget"]').wait_for(state='hidden',timeout=30000)
                except Exception:pass
                page.add_style_tag(content='*,*::before,*::after { transition: none !important; animation: none !important; }')
                # Expose collapsed navigation and native controls, including download actions.
                page.locator('details:not([open]) > summary').evaluate_all('els=>els.forEach(el=>el.click())')
                page.wait_for_timeout(150)
                # Inspect sidebar links even on mobile by keeping its panel open.
                errors=page.locator('[data-testid="stException"]').all_inner_texts()
                if errors:failures.append({'route':route,'width':width,'exceptions':errors})
                if page.evaluate('document.documentElement.scrollWidth>innerWidth'):failures.append({'route':route,'width':width,'overflow':True})
                def check(state):
                    page.wait_for_function("()=>document.querySelector('[data-testid=stApp]').getAttribute('data-test-script-state')==='notRunning'")
                    page.locator('[data-stale=true]').wait_for(state='hidden',timeout=15000) if page.locator('[data-stale=true]').count()==1 else None
                    items=page.locator(SELECTOR).evaluate_all(INSPECT)
                    for item in items:
                        if item['disabled']:continue  # Disabled controls are exempt from WCAG text contrast.
                        if not item['text'] and not item['iconOnly'] and not (item['tag']=='INPUT' and item['name']):failures.append({'route':route,'width':width,'state':state,'missingLabel':item})
                        for part in item['fragments']:
                            if part['ratio']<4.5:failures.append({'route':route,'width':width,'state':state,'contrast':part,'control':item['text']})
                    results.append({'route':route or 'home','width':width,'state':state,'controls':items})
                check('default')
                nav=page.locator('[data-testid="stSidebar"] [data-testid="stPageLink"] a')
                for i in range(nav.count()):
                    item=nav.nth(i)
                    if item.is_visible():
                        item.hover();check('nav-hover:'+item.inner_text())
                        page.keyboard.press('Tab');item.focus();check('nav-focus:'+item.inner_text())
                        page.mouse.down();check('nav-pressed:'+item.inner_text());page.mouse.move(0,0);page.mouse.up()
                if width==390:
                    sidebar=page.locator('[data-testid="stSidebar"]')
                    if sidebar.evaluate('(el)=>el.getBoundingClientRect().right>5'):
                        page.locator('[data-testid="stSidebarCollapseButton"] button').first.dispatch_event('click')
                        page.wait_for_function('()=>document.querySelector("[data-testid=stSidebar]").getBoundingClientRect().right<=5')
                check('main-default')
                actions=page.locator('section[data-testid="stMain"] button, a.pa-button, a.portfolio-button, a.contact-card-action, [role=combobox], [role=tab], [role=switch], [data-testid=stDateInputField]')
                for i in range(actions.count()):
                    action=actions.nth(i)
                    if action.is_visible() and action.is_enabled():
                        target=action.locator('xpath=..') if action.get_attribute('role')=='switch' else action
                        target.hover(force=True);check('control-hover:'+str(i))
                        page.keyboard.press('Tab');
                        if action.get_attribute('data-testid')=='stDateInputField':action.locator('[role=spinbutton]').first.focus()
                        else:action.focus()
                        check('control-focus:'+str(i))
                        if action.evaluate('el=>el.matches("a.pa-button,a.portfolio-button,a.contact-card-action,[role=tab]")'):
                            target.hover(force=True);page.mouse.down();check('control-pressed:'+str(i));page.mouse.move(0,0);page.mouse.up()
                        page.keyboard.press('Escape')
                # Opening menus/calendars changes no selection or form value.
                for widget in page.locator('[role=combobox], [data-testid=stDateInputField]').all():
                    if widget.is_visible() and widget.is_enabled():
                        widget.click(force=True);page.wait_for_timeout(150);check('open-widget')
                        page.keyboard.press('Escape')
                page.mouse.move(0,0)
                page.close();page=browser.new_page(viewport={'width':width,'height':900})
            page.close()
        browser.close()
    output={'pages':len(ROUTES)*2,'states':len(results),'failures':failures,'results':results}
    Path(args.output).write_text(json.dumps(output,indent=2));print(json.dumps({'pages':output['pages'],'states':len(results),'failures':failures},indent=2))
    if failures:raise SystemExit(1)

if __name__=='__main__':main()
