"""Read immutable GitHub interaction batches directly from cloud custody.
No local database, checkpoint, disk cache or owner-host service is required.
"""
import base64,hashlib,hmac,json,os,urllib.request
from datetime import datetime,timezone
from .custody import _aes,secure_key,KEY_REFERENCE
from .discovery import _existing_credential
from .agent_inventory import NOTE

REPO='tokenjunkielabs/swarm-telemetry-custody'
def read_interactions(config=None,*,limit=100,cursor=None,direction=None,kind=None):
    config=config or {};limit=max(1,min(1000,int(limit)))
    token=os.environ.get('SWARM_GITHUB_WORKING_TOKEN') or _existing_credential(config,'github/tokenjunkielabs')
    supplied=os.environ.get('SWARM_SOURCE_CUSTODY_KEY')
    key=base64.b64decode(supplied,validate=True) if supplied else secure_key()
    if len(key)!=64:raise RuntimeError('shared_custody_key_unavailable')
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
    def get(path,binary=False):
        req=urllib.request.Request('https://api.github.com/repos/'+REPO+path,headers={'Authorization':'Bearer '+token,'Accept':'application/octet-stream' if binary else 'application/vnd.github+json','User-Agent':'Commons-Telemetry'})
        with opener.open(req,timeout=25) as r:raw=r.read()
        return raw if binary else json.loads(raw)
    release=get('/releases/tags/telemetry-custody-v1');pointer=json.loads(release.get('body') or '{}');asset_id=pointer.get('events_asset_id');offset=0
    if cursor:
        page=json.loads(base64.urlsafe_b64decode(cursor+'='*(-len(cursor)%4)))
        if page.get('direction')!=direction or page.get('kind')!=kind:raise ValueError('Keep cursor filters unchanged')
        asset_id=int(page['asset_id']);offset=int(page['offset'])
        if asset_id<=0 or offset<0:raise ValueError('Invalid cloud cursor')
    if not asset_id:return {'status':'pending','events':[],'counts_are_lower_bounds':True,'corpus_complete':False,'peer_note':NOTE}
    record=json.loads(get('/releases/assets/'+str(asset_id),True))
    iv=base64.b64decode(record['iv']);cipher=base64.b64decode(record['ciphertext']);mac=hmac.new(key[32:],b'swarm-source-v1'+iv+cipher,hashlib.sha256).digest()
    if not hmac.compare_digest(mac,base64.b64decode(record['mac'])):raise RuntimeError('cloud_custody_mac_mismatch')
    raw=_aes(cipher,key[:32],iv,True)
    if hashlib.sha256(raw).hexdigest()!=record['sha256'] or len(raw)!=record['byte_length']:raise RuntimeError('cloud_custody_hash_mismatch')
    batch=json.loads(raw);rows=[r for r in batch.get('events',[]) if (not direction or r.get('direction')==direction) and (not kind or r.get('kind')==kind)]
    at=datetime.now(timezone.utc);age=(at-datetime.fromisoformat(batch['observed_at'].replace('Z','+00:00'))).total_seconds();fresh=0<=age<=300
    end=min(len(rows),offset+limit);next_cursor=base64.urlsafe_b64encode(json.dumps({'asset_id':asset_id,'offset':end,'direction':direction,'kind':kind}).encode()).decode().rstrip('=') if end<len(rows) else None
    return {'status':'observed','measured_at':at.isoformat(),'source_batch_at':batch['observed_at'],'age_seconds':age,'fresh':fresh,'execution_state':'unknown','collector_observation_state':'observed' if fresh else 'unknown','current_interaction_count':len(rows) if fresh else None,'reported_interaction_count':len(rows),'events':rows[offset:end],'next_cursor':next_cursor,'has_more':bool(next_cursor),'source_refs':batch.get('reads',[]),'cloud_custody_verified':True,'source_custody_repo':REPO,'key_reference':KEY_REFERENCE,'counts_are_lower_bounds':True,'corpus_complete':False,'peer_note':NOTE,'scope':'This retained cloud batch and exact pinned pagination; historical cloud batches and all source gaps remain visible. This page is not the corpus.'}
