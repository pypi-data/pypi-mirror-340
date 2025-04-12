# minakicoin/p2p_node/routes/peer.py

from fastapi import APIRouter, Request
from minakicoin.p2p_node.state import known_peers
from minakicoin.services.peer_store import save_peers
import httpx

router = APIRouter()

@router.get("/ping")
async def ping():
    return {"status": "alive"}

@router.get("/peers")
async def get_peers():
    return {"known_peers": known_peers}

@router.post("/register")
async def register_peer(request: Request):
    data = await request.json()
    peer_url = data.get("peer")
    if peer_url and peer_url not in known_peers:
        known_peers.append(peer_url)
        save_peers(known_peers)
        print(f"[🔗] New peer registered: {peer_url}")
    return {"peers": known_peers}

@router.post("/peer/forget")
async def forget_peer(request: Request):
    data = await request.json()
    peer = data.get("peer")
    if peer in known_peers:
        known_peers.remove(peer)
        save_peers(known_peers)
        print(f"[🗑️] Peer removed: {peer}")
        return {"removed": peer}
    return {"error": "peer not found"}

@router.get("/heartbeat")
async def heartbeat():
    live_peers = []
    for peer in known_peers:
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(f"{peer}/ping", timeout=2)
                if res.status_code == 200:
                    live_peers.append(peer)
        except Exception:
            pass
    return {"live_peers": live_peers}
