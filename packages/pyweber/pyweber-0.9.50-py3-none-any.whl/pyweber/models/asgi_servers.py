from pyweber.models.ws_message import wsMessage
from pyweber.pyweber.pyweber import Pyweber
from pyweber.connection.session import sessions, Session
from pyweber.core.events import EventConstrutor
from pyweber.utils.utils import PrintLine
import websockets as ws
import inspect
from threading import Thread
import asyncio
from uuid import uuid4
import json


class AsgiWebsockets:
    def __init__(self, app: Pyweber):
        self.app = app
        self.ws_connections: set[str] = set()

    async def asgi_ws_handler(self, scope, receive, send):
        try:
            raw_message = await receive()

            if raw_message.get('type', None) == 'websocket.receive':
                text = raw_message.get('text', None)

                if text:
                    message = wsMessage(raw_message=json.loads(text), app=self.app, protocol='asgi')
                    if not message.session_id or message.session_id not in sessions.all_sessions:
                        ws_id = message.session_id or str(uuid4())
                        sessions.add_session(
                            session_id=ws_id,
                            Session=Session(
                                template=await message.template,
                                window=message.window
                            )
                        )
                        self.ws_connections.add(ws_id)
                        await send({
                            'type': 'websocket.send',
                            'text': json.dumps({'setSessionId': ws_id}),
                        })
                    
                    if message.type and message.event_ref:
                        sessions.get_session(session_id=message.session_id).template = await message.template
                        sessions.get_session(session_id=message.session_id).window = message.window
                        await self.ws_message(send=send, message=message)
        
        except Exception as e:
            print(e)
        
        finally:
            sessions.remove_session(session_id=raw_message.get('id'))

    async def ws_message(self, send, message: wsMessage):
            event_handler = EventConstrutor(
                ws_message=message,
                ws_update=self.send_message,
                ws_reload=self.send_reload,
                send=send
            ).build_event

            print(message.type, message.target_uuid)

            if message.event_ref == 'document':
                if event_handler.element:
                    event_id = event_handler.element.events.__dict__.get(f'on{message.type}')
                    template_events = sessions.get_session(session_id=message.session_id).template.events
                    
                    if event_id and event_id in template_events:
                        handler = template_events.get(event_id)
                        print(handler)

                        if inspect.iscoroutinefunction(handler):
                            Thread(target=asyncio.run, args=(handler(event_handler),), daemon=True).start()
                        
                        else:
                            Thread(target=handler, args=(event_handler,), daemon=True).start()
            
            await self.send_message(send=send, session_id=event_handler.session_id)

    async def send_message(self, send, session_id: str):
        try:
            ws_conn = next((ws for ws in self.ws_connections if ws == session_id), None)

            if ws_conn:
                data = {
                    'template': sessions.get_session(ws_conn).template.build_html(),
                    'window_events': sessions.get_session(ws_conn).window.get_all_event_ids
                }

                await send({
                    'type': 'websocket.send', 
                    'text': json.dumps(data, ensure_ascii=False, indent=4)
                })
        
        except Exception as e:
            PrintLine(f'Error sending message: {e}')
            return

    async def send_reload(self, send, session_id: str = None):
        try:
            if session_id:
                ws_conn = next((ws for ws in self.ws_connections if ws == session_id), None)
                if ws_conn:
                    await send({
                        'type': 'websocket.send',
                        'text': 'reload'
                    })
                    return
            
            for ws_conn in self.ws_connections:
                await send({
                    'type': 'websocket.send',
                    'text': 'reload'
                })

        except Exception as e:
            PrintLine(f'Error sending reload: {e}')
            return
    
    async def __call__(self, scope, receive, send):
        assert scope.get('type', None) == 'websocket'
        r_message = await receive()
        print(r_message)
        await send({'type': 'websocket.accept'})
        await self.asgi_ws_handler(scope=scope, receive=receive, send=send)