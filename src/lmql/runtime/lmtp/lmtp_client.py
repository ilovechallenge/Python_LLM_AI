import aiohttp
import asyncio
import json
import sys
import multiprocessing
from multiprocessing.connection import Connection

from .lmtp_server import TokenSession

class LMTPWebSocketClient:
    def __init__(self, model_identifier, ws: aiohttp.ClientWebSocketResponse):
        self.ws = ws
        self.stream_id = 0
        self.model_identifier = model_identifier

        self.handler = None
        self.iterators = {}

    async def generate(self, prompt, **kwargs):
        self.stream_id += 1
        payload = {
            **kwargs,
            "model": self.model_identifier,
            "prompt": prompt,
            "stream_id": self.stream_id
        }
        if payload.get("logit_bias", None) is None:
            payload.pop("logit_bias", None)
        await self.ws.send_str("GENERATE {}".format(json.dumps(payload)))

        async for token in self.stream_iterator(self.stream_id):
            yield token

    async def score(self, prompt, scored_prompt, **kwargs):
        self.stream_id += 1
        payload = {
            **kwargs,
            "model": self.model_identifier,
            "prompt": prompt,
            "scored": scored_prompt,
            "stream_id": self.stream_id
        }

        await self.ws.send_str("SCORE {}".format(json.dumps(payload)))

        async for token in self.stream_iterator(self.stream_id):
            yield token

    async def stream_iterator(self, stream_id):
        q = asyncio.Queue()
        self.iterators.setdefault(stream_id, []).append(q)
        
        while True:
            item = await q.get()
            if item is None: 
                break
            if item.get("finish_reason") is not None:
                yield item
                break
            yield item

    def connect(self):
        async def msg_handler():
            async for msg in self.ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    try:
                        self.handle(msg)
                    except Exception as e:
                        print("failed to handle msg", e, flush=True)
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break
        self.handler = asyncio.create_task(msg_handler())

    def handle(self, msg):
        cmd, args = msg.data.split(" ",1)
        if cmd == "TOKEN":
            data = json.loads(args)
            
            for d in data:
                stream_id = d["stream_id"]
                consumers = self.iterators.get(stream_id, [])
                for q in consumers: q.put_nowait(d)
        else:
            print("Unknown command: {}".format(cmd), flush=True)

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect('http://localhost:8080') as ws:
            import tiktoken

            model = sys.argv[1]
            tokenizer = tiktoken.encoding_for_model("text-ada-001")

            client = LMTPWebSocketClient(model, ws)
            client.connect()

            async def generate_call(i):
                prompt = tokenizer.encode("French: Sonde V18, Ø18 x 85mm, 33kHz, 8m, raccord ressort & taraudé M12, livré avec 2 piles 3.6V LS14250\nFrench:")
                ids = [*prompt]

                async for t in client.generate(prompt, max_tokens=32, logit_bias={0: -100, 12: -100}, temperature=0.0):
                    ids.append(t["token"])
                    print(i, [tokenizer.decode(ids)], flush=True)
            
            await asyncio.gather(*[generate_call(i) for i in range(1)])
            
            print("[LMTP connection closed]", flush=True)


# time.sleep(1.5)
# print("Starting LMTP client", flush=True)
if __name__ == "__main__":
    asyncio.run(main())