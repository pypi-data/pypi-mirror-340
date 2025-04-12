import os
import asyncio
import httpx
import socket
from fastapi import FastAPI
from dotenv import load_dotenv
from minakicoin.p2p_node.routes import chain, peer, mining, broadcast, status
from minakicoin.p2p_node.state import known_peers
from minakicoin.services.mempool import cleanup_mempool
from minakicoin.p2p_node.services.sync import sync_chain_from_peers

# 🌱 Load from .env
load_dotenv()
env_node_address = os.getenv("NODE_ADDRESS")

# 🌐 Detect public IP if NODE_ADDRESS not set (non-seed nodes)
async def get_public_ip():
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get("https://api.ipify.org")
            if res.status_code == 200:
                return f"http://{res.text}:7777"
    except Exception:
        return None

app = FastAPI()

# ✅ Include route modules
app.include_router(status.router)
app.include_router(peer.router)
app.include_router(chain.router)
app.include_router(mining.router)
app.include_router(broadcast.router)

NODE_ADDRESS = None  # Will be set in startup

async def register_with_peers():
    for peer in list(known_peers):
        if peer == NODE_ADDRESS:
            print(f"[🔁] Skipping self-registration ({NODE_ADDRESS})")
            continue

        try:
            async with httpx.AsyncClient() as client:
                res = await client.post(f"{peer}/register", json={"peer": NODE_ADDRESS})
                if res.status_code == 200:
                    print(f"[✅] Registered with {peer}")
        except Exception as e:
            print(f"[❌] Could not register with {peer} — {e}")

@app.on_event("startup")
async def startup():
    global NODE_ADDRESS

    print("🔁 Node starting up...")

    if env_node_address:
        NODE_ADDRESS = env_node_address
        print(f"[🌍] Using .env NODE_ADDRESS: {NODE_ADDRESS}")
    else:
        NODE_ADDRESS = await get_public_ip()
        print(f"[🌍] Detected public IP: {NODE_ADDRESS}")

    if not NODE_ADDRESS:
        print("[❌] Failed to determine NODE_ADDRESS. Exiting.")
        return

    await register_with_peers()
    await sync_chain_from_peers()

    async def ping_loop():
        while True:
            print("[🔎] Checking peer heartbeats...")
            for peer in list(known_peers):
                try:
                    async with httpx.AsyncClient() as client:
                        res = await client.get(f"{peer}/ping", timeout=2)
                        if res.status_code == 200:
                            print(f"[💓] {peer} is alive")
                        else:
                            print(f"[💤] {peer} responded with {res.status_code}")
                except Exception as e:
                    print(f"[💔] {peer} is unreachable — {e}")
            await asyncio.sleep(10)

    async def mempool_ttl_cleanup_loop():
        while True:
            cleanup_mempool()
            await asyncio.sleep(60)

    asyncio.create_task(ping_loop())
    asyncio.create_task(mempool_ttl_cleanup_loop())
