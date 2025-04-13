import json
import inspect
import asyncio
import ssl
from uuid import uuid4
import websockets as ws
from typing import Callable, Union
from concurrent.futures import ThreadPoolExecutor
from websockets.asyncio.server import serve as async_serve
from pyweber.pyweber.pyweber import Pyweber
from pyweber.models.ws_message import wsMessage
from pyweber.core.events import EventConstrutor, EventHandler
from pyweber.utils.utils import PrintLine, Colors
from pyweber.connection.session import sessions, Session

class WsServer:
    def __init__(self, host: str, port: int, cert_file: str, key_file: str):
        self.host: str = host
        self.port: int = port
        self.app: Pyweber = None
        self.ws_connections: set[ws.server.ServerConnection] = set()
        self.color_red = Colors.RED
        self.color_reset = Colors.RESET
        self.cert_file = cert_file
        self.key_file = key_file
        self.ssl_context = None
    
    async def ws_handler(self, websocket: ws.server.ServerConnection):
        try:
            async for message in websocket:
                message = wsMessage(raw_message=json.loads(message), app=self.app, protocol='pyweber')
                message.template = await message.template

                if not message.session_id or message.session_id not in sessions.all_sessions:
                    websocket.id = message.session_id or str(websocket.id)
                    sessions.add_session(
                        session_id=websocket.id,
                        Session=Session(
                            template=message.template,
                            window=message.window
                        )
                    )
                    self.ws_connections.add(websocket)
                    await websocket.send(json.dumps({'setSessionId': websocket.id}))
                
                if message.type and message.event_ref:
                    sessions.get_session(session_id=message.session_id).template = message.template
                    sessions.get_session(session_id=message.session_id).window = message.window
                    await self.ws_message(message=message)
        
        except Exception as e:
            PrintLine(f'Error [ws]: {self.color_red}{e}{self.color_reset}')

        finally:
            self.ws_connections.discard(websocket)
            sessions.remove_session(session_id=websocket.id)
    
    async def ws_message(self, message: wsMessage):
        event_handler = EventConstrutor(
            ws_message=message,
            ws_update=self.send_message,
            ws_reload=self.send_reload,
            send=None
        ).build_event

        if message.event_ref == 'document':
            if event_handler.element:
                event_id = event_handler.element.events.__dict__.get(f'on{message.type}')
                template_events = sessions.get_session(session_id=message.session_id).template.events
                
                if event_id and event_id in template_events:
                    handler = template_events.get(event_id)

                    if inspect.iscoroutinefunction(handler):
                        asyncio.create_task(handler(event_handler))
                    
                    else:
                        loop = asyncio.get_running_loop()
                        loop.run_in_executor(None, lambda: handler(event_handler))
        
        await self.send_message(session_id=event_handler.session_id)
    
    async def send_message(self, send=None, session_id: str=None):
        try:
            ws_conn = next((ws for ws in self.ws_connections if ws.id == session_id), None)

            if ws_conn:
                data = {
                    'template': sessions.get_session(ws_conn.id).template.build_html(),
                    'window_events': sessions.get_session(ws_conn.id).window.get_all_event_ids
                }

                await ws_conn.send(json.dumps(data, ensure_ascii=False, indent=4))
        
        except Exception as e:
            PrintLine(f'Error sending message: {e}')
            return
    
    async def send_reload(self, send=None, session_id: str = None):
        try:
            if session_id:
                ws_conn = next((ws for ws in self.ws_connections if ws.id == session_id), None)
                if ws_conn:
                    await ws_conn.send('reload')
                    return
            
            for ws_conn in self.ws_connections:
                await ws_conn.send('reload')

        except Exception as e:
            PrintLine(f'Error sending reload: {e}')
            return
    
    def ssl_setup(self):
        try:
            self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            self.ssl_context.load_cert_chain(certfile=self.cert_file, keyfile=self.key_file)
        except Exception as e:
            PrintLine(f'{Colors.RED}WebSocket SSL configuration failed: {e}{Colors.RESET}')
            self.ssl_context = None

    async def ws_start(self):
        try:
            self.ssl_setup()
            if self.ssl_context:
                PrintLine(text=f"Server [ws] is running in wss://{self.host}:{self.port}")
            else:
                PrintLine(text=f"Server [ws] is running in ws://{self.host}:{self.port}")
            
            async with async_serve(self.ws_handler, self.host, self.port, ssl=self.ssl_context) as server:
                await server.serve_forever()
                
        except OSError as e:
            PrintLine(f"{Colors.RED}WebSocket server error: {e}{Colors.RESET}")
        except Exception as e:
            PrintLine(f"{Colors.RED}Unexpected error in WebSocket server: {e}{Colors.RESET}")

class WsServerAsgi:
    def __init__(self, app: Pyweber):
        self.app = app
        self.ws_connections: set[str] = set()
        self.task_manager = TaskManager()
    
    async def ws_handler(self, scope, receive, send):
        ws_id = None
        try:
            while True:
                raw_message = await receive()
                
                if raw_message.get('type') == 'websocket.connect':
                    await send({'type': 'websocket.accept'})

                elif raw_message.get('type') == 'websocket.receive':
                    text: str = raw_message.get('text', None)

                    if text:
                        message = wsMessage(raw_message=json.loads(text), app=self.app)
                        message.template = await message.template

                        if not message.session_id or message.session_id not in sessions.all_sessions:
                            ws_id = message.session_id or str(uuid4())
                            sessions.add_session(
                                session_id=ws_id,
                                Session=Session(
                                    template=message.template,
                                    window=message.window
                                )
                            )

                            await send({'type': 'websocket.send', 'text': json.dumps({'setSessionId': str(uuid4())})})

                        if message.type and message.event_ref:
                            ws_id = message.session_id
                            sessions.get_session(session_id=message.session_id).template = message.template
                            sessions.get_session(session_id=message.session_id).window = message.window
                            await self.ws_message(send, message=message)

                else:
                    break
                
        except Exception as e:
            print(f'Error [ws asgi]: {e}')
        
        finally:
            self.ws_connections.discard(ws_id)
            sessions.remove_session(session_id=ws_id)
            await self.task_manager.cancel_all_tasks(session_id=ws_id)
    
    async def ws_message(self, send, message: wsMessage):
        event_handler = EventConstrutor(
            ws_message=message,
            ws_update=self.send_message,
            ws_reload=self.send_reload,
            send=send
        ).build_event

        if message.event_ref == 'document':
            if event_handler.element:
                event_id = event_handler.element.events.__dict__.get(f'on{message.type}')
                template_events = sessions.get_session(session_id=message.session_id).template.events
                
                if event_id and event_id in template_events:
                    handler = template_events.get(event_id)

                    if inspect.iscoroutinefunction(handler):
                        await ExecuteHander(
                            session_id=message.session_id,
                            event_id=event_id,
                            handler=handler,
                            event_handler=event_handler,
                            task_manager=self.task_manager
                        ).run_async_handler()
                    else:
                        await ExecuteHander(
                            session_id=message.session_id,
                            event_id=event_id,
                            handler=handler,
                            event_handler=event_handler,
                            task_manager=self.task_manager
                        ).run_sync_handler(send=send, send_message=self.send_message)
                
        await self.send_message(send, message.session_id)
        
    async def send_message(self, send, session_id):
        try:
            data = {
                'template': sessions.get_session(session_id).template.build_html(),
                'window_events': sessions.get_session(session_id).window.get_all_event_ids
            }
            await send({'type': 'websocket.send', 'text': json.dumps(data, ensure_ascii=False, indent=4)})

        except Exception as e:
            print(f'Error [ws asgi]: {e}')

    async def send_reload(self, send, session_id=None):
        await send({'type': 'websocket.send', 'text': 'reload'})
    
    async def __call__(self, scope, receive, send):
        assert scope.get('type', None) == 'websocket'
        await self.ws_handler(scope, receive, send)

class TaskManager:
    def __init__(self):
        self.tasks: dict[str, dict[str, asyncio.Task]] = {}
        self.executors: dict[str, ThreadPoolExecutor] = {}
        self.__lock = asyncio.Lock()

    async def create_task(self, session_id, coro, event_id):
        async with self.__lock:
            if session_id not in self.tasks:
                self.tasks[session_id] = {}
            
            if event_id not in self.tasks[session_id]:
                task = asyncio.create_task(coro)
                self.tasks[session_id][event_id] = task
        
                task.add_done_callback(
                    lambda t: asyncio.create_task(self.clean_task(session_id, event_id))
                )
    
    async def clean_task(self, session_id, event_id):
        if session_id in self.tasks and event_id in self.tasks[session_id]:
            del self.tasks[session_id][event_id]
    
    def get_executor(self, session_id, max_workers=10):
        if session_id not in self.executors:
            self.executors[session_id] = ThreadPoolExecutor(max_workers=max_workers)
        
        return self.executors[session_id]
    
    async def cancel_all_tasks(self, session_id):
        async with self.__lock:
            if session_id in self.tasks:
                tasks = list(self.tasks[session_id].values())
                for task in tasks:
                    if not task.done() and not task.cancelled():
                        task.cancel()
                
                if tasks:
                    await asyncio.gather(*tasks, return_exceptions=True)
                
                self.tasks[session_id].clear()
            
            if session_id in self.executors:
                self.executors[session_id].shutdown(wait=False)
                del self.executors[session_id]

class ExecuteHander:
    def __init__(self, session_id: str, event_id: str, handler: Callable, event_handler: EventHandler, task_manager: TaskManager):
        self.handler = handler
        self.event_handler = event_handler
        self.session_id = session_id
        self.event_id = event_id
        self.task_manager = task_manager

    async def run_async_handler(self):
        await self.task_manager.create_task(
            self.session_id,
            self.handler(self.event_handler),
            event_id=self.event_id
        )
    
    async def run_sync_handler(self, send, send_message):
        # Para funções síncronas
        main_loop = asyncio.get_running_loop()
        executor = self.task_manager.get_executor(self.session_id)
        
        def thread_safe_update():
            # Enviamos a atualização usando o loop principal
            future = asyncio.run_coroutine_threadsafe(
                send_message(send, self.session_id),
                main_loop
            )
            # Aguardamos a conclusão para garantir que a atualização seja finalizada
            try:
                future.result(timeout=5)
            except Exception as e:
                print(f"Erro ao atualizar: {e}")
        
        # Substituir o método update no event_handler
        self.event_handler.update = thread_safe_update
        
        # Executamos o handler em uma thread e criamos uma tarefa para monitorá-lo
        async def monitor_sync_handler():
            try:
                # Executar o handler em uma thread
                await main_loop.run_in_executor(executor, lambda: self.handler(self.event_handler))
            except Exception as e:
                print(f"Erro no handler síncrono: {e}")
        
        # Registrar a tarefa no gerenciador
        await self.task_manager.create_task(
            self.session_id,
            monitor_sync_handler(),
            event_id=self.event_id
        )