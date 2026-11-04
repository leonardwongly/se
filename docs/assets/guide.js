(() => {
  'use strict';
  const root=document.getElementById('workflow-capture');if(!root)return;
  const $=id=>document.getElementById(id), diagram=$('flow-diagram'), reduced=matchMedia('(prefers-reduced-motion: reduce)');
  const nodes=[...diagram.querySelectorAll('[data-node]')],tokens=[$('token-a'),$('token-b')];
  const stages=[
    ['ground','Start with the actual project','Identify current contracts, active paths and the exact source state before making a claim.','GROUND','PROJECT CONTEXT'],
    ['decide','Ask the questions that change the decision','Use what, why, who, where, how and when as needed. Select suitable expertise and relevant available tools.','DECIDE','SCOPED OUTCOME'],
    ['trust','Review the boundary before writing code','Inspect identity, inputs, authority and effects. The baseline applies to every new or modified code change.','REVIEW','BEFORE IMPLEMENTATION'],
    ['build','Split only work that can safely overlap','Optional swarm: two owners work against one shared contract. Concurrent keeps write ownership disjoint.','BUILD','OPTIONAL PARALLEL WORK'],
    ['integrate','Bring the work into one stable revision','Confirm writers have stopped, reconcile interfaces and capture the combined source state.','INTEGRATE','REVISION A'],
    ['review','Inspect the final diff and combined boundaries','Re-evaluate trust assumptions on revision A. Individually safe changes can combine into an unsafe path.','REVIEW','REVISION A'],
    ['verify','A failed check is evidence, too','Revision A violates the interface contract. Retain the failure; this revision cannot pass.','FAIL','REVISION A'],
    ['trust','Reassess before making the repair','Review the affected assumptions. Reuse still-valid evidence and preserve the original failed result.','REASSESS','REPAIR WITHIN SCOPE'],
    ['build','Repair the evidenced gap','Owner A fixes the interface mismatch. Continue authorized work; do not broaden scope or weaken the check.','REPAIR','OWNER A'],
    ['integrate','Capture a new combined revision','Stop writers and reintegrate the repair. Revision B needs new evidence for affected behavior.','INTEGRATE','REVISION B'],
    ['review','Review the repaired final diff','Check revision B’s affected trust boundaries before accepting the new verification evidence.','REVIEW','REVISION B'],
    ['verify','Rerun the checks against revision B','In this example, the failed check and required combined checks now pass. The original failure remains recorded.','PASS','REVISION B'],
    ['outcome','Make a claim no larger than the evidence','Report the scoped local result and its limits. Visualise the mechanism when useful. A local pass is not deployment permission.','LOCAL PASS','SCOPED EVIDENCE']
  ];
  let index=0,playing=false,timer=null,animations=[],previous=null;
  const center=el=>{const a=el.getBoundingClientRect(),b=diagram.getBoundingClientRect();return{x:a.left-b.left+a.width/2-5,y:a.top-b.top+a.height/2-5};};
  const nodePoint=key=>center(diagram.querySelector('[data-node="'+key+'"] .port'));
  const lanePoint=key=>center(diagram.querySelector('[data-worker="'+key+'"] .worker-port'));
  function wires(){
    const order=['ground','decide','trust','build','integrate','review','verify','outcome'];
    $('main-wire').setAttribute('d',order.map((name,i)=>{const p=nodePoint(name);return(i?'L':'M')+(p.x+5)+','+(p.y+5);}).join(' '));
    const a=nodePoint('verify'),b=nodePoint('trust');$('repair-wire').setAttribute('d','M'+(a.x+5)+','+(a.y+5)+' L'+(b.x+5)+','+(b.y+5));
  }
  function positionTokens(motion=false){
    const split=index===3,merge=index===4&&previous&&previous.length===2;
    const targets=split?[lanePoint('a'),lanePoint('b')]:[index===8?lanePoint('a'):nodePoint(stages[index][0])];
    if(merge)targets.push(targets[0]);
    animations.forEach(a=>a.cancel());animations=[];
    tokens.forEach((token,i)=>{
      const target=targets[i];token.hidden=!target;if(!target)return;
      const from=previous&&(previous[i]||previous[0]);token.style.transform=`translate(${target.x}px,${target.y}px)`;
      if(motion&&from&&!reduced.matches){
        const points=[from];if(split)points.push(nodePoint('build'));points.push(target);
        const a=token.animate(points.map(p=>({transform:`translate(${p.x}px,${p.y}px)`})),{duration:650,easing:'ease-in-out'});
        if(merge&&i===1)a.onfinish=()=>{token.hidden=true;};animations.push(a);
      }else if(merge&&i===1)token.hidden=true;
    });previous=targets;
  }
  function render(motion=false){
    const s=stages[index];root.dataset.stage=String(index);root.dataset.playing=String(playing);
    nodes.forEach(n=>{n.dataset.active=String(n.dataset.node===s[0]);n.removeAttribute('data-result');if(n.dataset.node===s[0])n.setAttribute('aria-current','step');else n.removeAttribute('aria-current');});
    if(index===6)diagram.querySelector('[data-node="verify"]').dataset.result='fail';diagram.classList.toggle('repairing',index===7||index===8);
    $('stage-count').textContent=String(index+1).padStart(2,'0')+' / '+stages.length;$('stage-title').textContent=s[1];$('stage-detail').textContent=s[2];$('stage-tag').textContent=s[3];$('stage-tag').dataset.kind=index===6?'fail':'normal';$('revision-label').textContent=s[4];
    $('verify-node-text').textContent=index<6?'Check actual outcomes':index<11?'A: FAIL retained':'A: FAIL · B: PASS';
    $('evidence-record').textContent=index<6?'No completed checks in this illustrative starting state.':index<11?'Revision A: FAIL retained. New evidence required after repair.':'Revision A: FAIL retained → Revision B: required checks PASS. Local scope only.';
    $('play').textContent=playing?'Pause Ⅱ':'Play the journey ▶';$('play').disabled=index===stages.length-1;$('step').disabled=index===stages.length-1;$('motion-note').textContent=reduced.matches?'Reduced motion: use Step to inspect the complete sequence.':'Motion explains sequence; timing is illustrative.';
    wires();positionTokens(motion);
  }
  function stop(){playing=false;clearTimeout(timer);timer=null;animations.forEach(a=>{if(a.playState==='running')a.pause();});root.dataset.playing='false';$('play').textContent='Play the journey ▶';}
  function schedule(){clearTimeout(timer);timer=setTimeout(()=>{if(!playing)return;index++;if(index===stages.length-1)playing=false;render(true);if(playing)schedule();},1750);}
  $('play').addEventListener('click',()=>{if(playing){stop();return;}if(index===stages.length-1)return;playing=true;root.dataset.playing='true';$('play').textContent='Pause Ⅱ';animations.forEach(a=>{if(a.playState==='paused')a.play();});schedule();});
  $('step').addEventListener('click',()=>{stop();index=Math.min(index+1,stages.length-1);render(true);});
  $('replay').addEventListener('click',()=>{stop();index=0;previous=null;playing=!reduced.matches;render();if(playing)schedule();});
  reduced.addEventListener('change',()=>{stop();previous=null;render();});document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
  let width=diagram.getBoundingClientRect().width;
  new ResizeObserver(()=>{wires();const next=diagram.getBoundingClientRect().width;if(Math.abs(next-width)>1){width=next;positionTokens(false);}}).observe(diagram);
  const skills={
    proof:['UNDERSTAND & EXPLAIN','Earn the conclusion.','Ground material claims in current evidence and explain the mechanism, assumptions and limits.','A question, the relevant source state, and the evidence available.','Supported claims, precise references and visible uncertainty.','Citations and agent agreement cannot replace required behavioral checks.'],
    visualise:['UNDERSTAND & EXPLAIN','Make the mechanism visible.','Choose an inline representation for the reader’s question. Animate time, state and causality when movement helps.','A grounded mechanism and the relationship that needs explaining.','A readable visual, meaningful controls and an accessible alternative.','A persuasive diagram does not prove runtime behavior.'],
    what:['FRAME & SHAPE','Name the outcome.','Turn an engineering request into bounded scope and observable acceptance criteria.','The request, current contracts and unresolved requirements.','Scope, acceptance conditions, non-goals and material questions.','Defining scope does not by itself authorize implementation.'],
    why:['FRAME & SHAPE','Understand the reason.','Distinguish recorded rationale from inference, compare credible alternatives and expose tradeoffs.','A decision, its history and current supporting evidence.','An evidence-backed rationale with alternatives and limits.','Observed behavior does not prove the original author’s intent.'],
    who:['FRAME & SHAPE','Choose the right expertise.','Match people or available agents to the actual knowledge gap, tools, access and task.','The responsibility, required expertise and current capability evidence.','An evidenced owner or bounded assignment with an integration owner.','Expertise and ownership are separate from authority to act.'],
    where:['FRAME & SHAPE','Find the active path.','Locate the responsible code, architecture layer, environment and evidence.','A behavior or claim and the current project context.','Precise locations and a traced connection to the behavior.','Navigation remains read-only unless a change is authorized.'],
    how:['FRAME & SHAPE','Explain what makes it work.','Trace the mechanism or form an implementation approach inside the authorized scope.','The desired outcome, active code and applicable contracts.','A causal explanation or a concrete, verifiable implementation approach.','An explanation request does not imply permission to edit.'],
    when:['FRAME & SHAPE','Respect the prerequisites.','Sequence dependencies, timing and rollout conditions using current evidence.','The intended action, dependency state and verification gate.','The eligible next action and concrete unresolved prerequisites.','Scheduling cannot override a failed or blocked verification gate.'],
    'zero-trust':['REQUIRED FOR CODE CHANGES','Review the real boundary.','Inspect untrusted inputs, authoritative identity, resource authorization and actual enforcement.','The change, its callers and affected trust assumptions.','Risk-scaled findings and permitted/denied behavior to verify.','Prompts and user-interface checks do not substitute for enforcement.'],
    verify:['REQUIRED FOR CODE CHANGES','Show that it behaves correctly.','Execute applicable project checks and qualify evidence against the exact final source state.','Acceptance criteria, risks, a stable revision and required environments.','Observed results, preserved failures, a scoped gate and limitations.','A local pass is not deployed proof or deployment authorization.'],
    swarm:['OPTIONAL EXECUTION STRATEGY','Coordinate, then improve.','Launch a useful bounded team, inspect its outputs, integrate and remediate evidenced gaps.','An authorized outcome, dependencies and available worker capacity.','Integrated work with actual checks and a clear completion boundary.','Continuous progress does not bypass real approvals or resource limits.'],
    concurrent:['OPTIONAL EXECUTION STRATEGY','Make parallel work safe.','Use disjoint ownership, appropriate isolation and a stable combined revision for verification.','Independent tasks, interfaces and shared mutable resources.','Clear assignments, safe handoffs and combined validation.','Worker completion alone does not establish integrated correctness.']
  };
  document.querySelectorAll('[data-skill]').forEach(button=>button.addEventListener('click',()=>{
    const key=button.dataset.skill,s=skills[key];if(!s)return;document.querySelectorAll('[data-skill]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
    $('skill-category').textContent=s[0];$('skill-name').textContent='/se-'+key;$('skill-purpose').textContent=s[1];$('skill-description').textContent=s[2];$('skill-input').textContent=s[3];$('skill-output').textContent=s[4];$('skill-boundary').textContent=s[5];$('skill-invocation').textContent='Codex invocation: $se-'+key;$('skill-source').href='https://github.com/leonardwongly/se/blob/main/se-'+key+'/SKILL.md';$('skill-detail').dataset.selected=key;
  }));
  $('skill-detail').dataset.selected='proof';render();
})();
