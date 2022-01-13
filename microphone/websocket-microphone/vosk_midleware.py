#!/usr/bin/env python3

import asyncio
import websockets
import sys
import requests
import json

IP = '127.0.0.1'
PORT = 8080

async def listen_results(uri):
    async with websockets.connect(uri) as websocket:
        print(f'start loop on {IP}')
        while True:
            answer_from_vosk = await websocket.recv()
            print(answer_from_vosk)
            answer = json.loads(answer_from_vosk)
            detected_text = answer['text']
            if detected_text == '':
                continue
            payload = {
                    'entity': 'detected_text',
                    'text': detected_text
                }
            print(payload)
            try:
                address = f'http://{IP}:{PORT}/voice_detect'
                r = requests.get(address, params=payload)
            except requests.exceptions.ConnectionError:
                print(f'Django server is not available {address}')
            

print('start program')
asyncio.get_event_loop().run_until_complete(
    listen_results('ws://localhost:2700'))
