// Independent, bounded regression oracle from observed defects; no network operations.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import crypto from 'node:crypto';
import { pathToFileURL, fileURLToPath } from 'node:url';
const root=path.resolve(process.argv[2]);
const output=path.resolve(process.argv[3]);
const {scanHtmlAttributes:scan}=await import(pathToFileURL(path.join(root,'scripts/lib/html-attributes.mjs')));
const {collectRenderedAssetReferences:assets}=await import(pathToFileURL(path.join(root,'scripts/check-performance-budget.mjs')));
const {collectHtmlUrls}=await import(pathToFileURL(path.join(root,'scripts/check-link-health.mjs')));
const results=[];
const check=(name,fn)=>{try{fn();results.push({name,passed:true});}catch(e){results.push({name,passed:false,error:e.message});}};
check('valid attribute at budget',()=>assert.deepEqual(scan('<img src="book/a.jpg">',{maxAttributes:1}).attributes.map(x=>x.value),['book/a.jpg']));
check('valid excess attribute rejected',()=>assert.throws(()=>scan('<img src="a" alt="b">',{maxAttributes:1}),/entry limit/));
check('malformed tokens consume budget',()=>assert.throws(()=>scan('<'+'a'.repeat(1024)+' '+'='.repeat(1024)+'>',{maxAttributes:1}),/entry limit/));
check('diagnostics do not repeat arbitrarily long tag names',()=>{
  const sum=n=>scan('<'+'a'.repeat(n)+' '+'='.repeat(64)+'>',{maxAttributes:64}).findings.reduce((v,s)=>v+s.length,0);
  const small=sum(128),large=sum(8192);
  assert.ok(small>0&&large<small*2,`64x tag-name length produced diagnostic lengths ${small} -> ${large}; expected bounded context, not full-name repetition`);
});
for(const html of ['<img','<img src="book/a.jpg"','<img src=book/a.jpg','<img disabled','<img/']){
 check('EOF diagnostic '+html,()=>assert.ok(scan(html).findings.some(s=>/unterminated/i.test(s))));
}
check('double opener retains real attribute',()=>assert.deepEqual(scan('<<img src="book/a.jpg">',{attributeNames:['src']}).attributes.map(x=>x.value),['book/a.jpg']));
check('performance collector sees double opener',()=>assert.deepEqual(assets('<<img src="book/a.jpg">').references,['book/a.jpg']));
check('performance collector reports truncated input',()=>assert.ok(assets('<img src="book/a.jpg"').findings.length>0));
check('comment and raw text positive control',()=>assert.deepEqual(scan('<!-- <img src="ignored"> --><script>"<img src=ignored>"</script><img src="ok">',{attributeNames:['src']}).attributes.map(x=>x.value),['ok']));
const temp=fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(),'scanner-oracle-')));
try{
 const html='<<img src="https://example.invalid/image.jpg">';
 fs.writeFileSync(path.join(temp,'page.html'),html);
 check('link collector sees double opener without fetch',()=>{
  const links=collectHtmlUrls('page.html',{rootDir:temp});
  assert.ok(links.some(x=>x.url==='https://example.invalid/image.jpg'));
  assert.equal(fs.readFileSync(path.join(temp,'page.html'),'utf8'),html);
 });
}finally{fs.rmSync(temp,{recursive:true,force:true});}
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const record={node:process.version,project:root,source_sha256:sha(path.join(root,'scripts/lib/html-attributes.mjs')),checker_sha256:sha(fileURLToPath(import.meta.url)),passed:results.filter(x=>x.passed).length,total:results.length,results,limits:'Bounded parser/caller cases; diagnostic logical lengths, not heap/exhaustion measurement. No network fetch, production impact or complete browser equivalence.'};
fs.writeFileSync(output,JSON.stringify(record,null,2)+'\n');
console.log(JSON.stringify({passed:record.passed,total:record.total,checker_sha256:record.checker_sha256}));
process.exitCode=record.passed===record.total?0:1;
