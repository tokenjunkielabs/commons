/** Exact-source forwarding for an existing native connector host.
 * The host supplies readPage and selects its actual authenticated account.
 * No dependency, peer registration, work dispatch or notification ack is used.
 */
export async function collectNativePass({baseURL='http://127.0.0.1:8893', readPage,
  fetchImpl=globalThis.fetch, availableTools, concurrency=4, signal, pageSize=128}) {
  if (typeof readPage!=='function') throw new TypeError('Existing authenticated readPage binding required');
  const base=baseURL.replace(/\/$/,'');
  const request=async(path, body)=>{
    const response=await fetchImpl(base+path,{signal, ...(body===undefined?{}:
      {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})});
    const result=await response.json();
    if (!response.ok || result.ok===false) throw new Error(result.error||'telemetry_receipt_unavailable');
    return result;
  };
  const health=await request('/api/telemetry/health');
  if (health.storage?.status==='pending_storage') return {captured:0,pending_storage:true,swarm_execution_independent:true};
  const jobs=[];
  let cursor='';
  do {
    const page=await request('/api/telemetry/source-jobs?limit='+Math.max(1,pageSize)+'&cursor='+encodeURIComponent(cursor));
    jobs.push(...page.jobs);
    cursor=page.next_cursor;
  } while(cursor && !signal?.aborted);
  const available=availableTools ? new Set(availableTools) : null;
  const now=Date.now()/1000;
  const pending=[];
  let deferred=0, nextAttempt=null;
  for (const job of jobs) {
    if (!job.tool_name || job.complete || (available && !available.has(job.tool_name))) continue;
    const retryAt=Number(job.next_attempt_epoch);
    if (Number.isFinite(retryAt) && retryAt>now) {
      deferred++;
      nextAttempt=nextAttempt===null ? retryAt : Math.min(nextAttempt,retryAt);
    } else pending.push(job);
  }
  const outcomes=[];
  let next=0;
  const worker=async()=>{
    while(next<pending.length && !signal?.aborted) {
      const job=pending[next++];
      try {
        // Arguments and native results never pass through model summarization.
        const argumentsCopy=structuredClone(job.args||{});
        const observed=await readPage({tool_name:job.tool_name,args:argumentsCopy,
          account_ref:job.account_ref,service:job.service,reader:job.reader,signal});
        if (!observed || observed.account_ref!==job.account_ref || !('payload' in observed)) {
          outcomes.push({job_id:job.job_id,status:'account_binding_unresolved'});
          continue;
        }
        const receipt=await request('/api/telemetry/source-response',{
          job_id:job.job_id,reader:job.reader,arguments:argumentsCopy,tool_name:job.tool_name,
          account_ref:observed.account_ref,service:job.service,payload:observed.payload,
          binding_evidence:observed.binding_evidence});
        outcomes.push({job_id:job.job_id,status:'captured',source_record_ref:receipt.source_record_ref});
      } catch(error) {
        outcomes.push({job_id:job.job_id,status:'pending_recovery',error:error.name||'SourceReadError'});
      }
    }
  };
  await Promise.all(Array.from({length:Math.max(1,Math.min(32,concurrency,pending.length||1))},worker));
  return {captured:outcomes.filter(row=>row.status==='captured').length,
    considered:pending.length,discovered_jobs:jobs.length,outcomes,corpus_complete:false,
    deferred_jobs:deferred,next_attempt_epoch:nextAttempt,
    sampling:false,swarm_execution_independent:true};
}

export async function runNativeCollector(options) {
  const delay=Math.max(1000,options.pollMilliseconds||10000);
  while(!options.signal?.aborted) {
    try { const result=await collectNativePass(options); options.onStatus?.(result); }
    catch(error) { options.onStatus?.({status:'pending_recovery',error:error.name}); }
    if(options.signal?.aborted) break;
    await new Promise(resolve=>{
      const finish=()=>{clearTimeout(timer);options.signal?.removeEventListener('abort',finish);resolve();};
      const timer=setTimeout(finish,delay);
      options.signal?.addEventListener('abort',finish,{once:true});
    });
  }
}
