"""
Metadata Service for ZeroMQ-based device metadata distribution.
Implements a REQ/REP pattern where metadata is sent in response to client requests.
"""
import asyncio
import zmq
import zmq.asyncio
from typing import Dict, Any, Optional
import threading
from ..utils.logger import logger
from ..utils.shared_state import SharedState
import json

class MetadataResponder:
    """
    Service that provides device metadata via a REP socket.
    Clients can connect with a REQ socket to request and receive the metadata.
    """
    _instance = None
    _lock = threading.Lock()
    
    @classmethod
    def get_instance(cls):
        """Get or create the singleton instance of MetadataResponder."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = MetadataResponder()
            return cls._instance
    
    def __init__(self):
        """Initialize the metadata service."""
        self.ctx = zmq.asyncio.Context.instance()
        self.shared_state = SharedState.get_instance()
        
        # Socket to respond to metadata requests (REP)
        # Bind to all interfaces (0.0.0.0) instead of specific IP to allow connections from any network
        self.rep_socket = self.ctx.socket(zmq.REP)
        self.metadata_responder_port = 5570
        # Update the port in the shared state
        self.shared_state.update("Orcustrator", {"MetadataResponder": self.metadata_responder_port})
        self.rep_socket.bind(f"tcp://0.0.0.0:{self.metadata_responder_port}")  # Changed from specific IP to 0.0.0.0
        self._running = False
        self._task = None
        
    async def start(self):
        """Start the metadata service."""
        if self._running:
            logger.warning("Metadata service is already running")
            return
            
        self._running = True
        self._task = asyncio.create_task(self._reply_loop())
        logger.success(f"Metadata available at: 0.0.0.0:{self.metadata_responder_port}")
        
    async def stop(self):
        """Stop the metadata service."""
        if not self._running:
            return
            
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None
            
        # Close socket
        self.rep_socket.close()
        logger.info("Metadata service stopped")
        
    async def _reply_loop(self):
        """Main loop to respond to metadata requests."""
        logger.debug("Metadata reply loop started")
        
        try:
            while self._running:
                try:
                    # Wait for a request
                    request_bytes = await self.rep_socket.recv()
                    try:
                        request = json.loads(request_bytes.decode('utf-8'))
                        logger.debug(f"Received metadata request: {request}")
                    except json.JSONDecodeError:
                        logger.error(f"Received non-JSON request: {request_bytes}")
                        await self.rep_socket.send_json({"type": "error", "error": "Invalid JSON request"})
                        continue
                    
                    # Process specific requests
                    request_type = request.get("request")
                    logger.debug(f"Processing request type: {request_type}")
                    if request_type == "GET_SUBDEVICE_TOPICS":
                        logger.debug("Processing GET_SUBDEVICE_TOPICS request...")
                        topics_data = {}
                        devices_state = self.shared_state.get("Devices", {})
                        for device_name, device_info in devices_state.items():
                            if isinstance(device_info, dict):
                                selected_middleware = device_info.get("SelectedMiddleware")
                                if selected_middleware:
                                    middlewares = device_info.get("AvailableMiddlewares", {})
                                    middleware_info = middlewares.get(selected_middleware, {})
                                    subdevices = middleware_info.get("SubDevices", {})
                                else:
                                    logger.warning(f"No SelectedMiddleware found for device '{device_name}'. Cannot extract topics.")
                                    subdevices = {}
                                for sub_name, sub_info in subdevices.items():
                                    full_topic_name = f"{device_name}.{sub_name}"
                                    sampling_rate = sub_info.get("SamplingFrequency")
                                    topics_data[full_topic_name] = {"sampling_rate": sampling_rate}
                        
                        # Format response specifically for topic requests
                        response_payload = {
                            "type": "topics_response",
                            "topics": topics_data
                        }
                        logger.debug(f"Sending {len(topics_data)} topics.")
                    
                    elif request_type == "GET_ALL_STATE":
                        logger.debug("Processing GET_ALL_STATE request...")
                        all_state = self.shared_state.get(None) # Get the full state dict
                        response_payload = {
                            "type": "state_response",
                            "state": all_state
                        }
                        logger.debug("Sending full shared state.")
                        
                    else:
                        logger.warning(f"Received unknown request type: {request_type}")
                        response_payload = {"type": "error", "error": f"Unknown request type: {request_type}"}
                        
                    # Send the metadata response
                    await self.rep_socket.send_json(response_payload)
                    
                except zmq.ZMQError as e:
                    logger.error(f"ZMQ error in metadata service: {e}")
                    await asyncio.sleep(1.0)  # Wait a bit before retrying
                except Exception as e:
                    logger.error(f"Error handling metadata request: {e}")
                    # Try to send an error response if possible
                    try:
                        await self.rep_socket.send_json({
                            "type": "error",
                            "error": str(e)
                        })
                    except:
                        pass
                    await asyncio.sleep(1.0)  # Wait a bit before retrying
                    
        except asyncio.CancelledError:
            logger.debug("Metadata reply loop cancelled")
            raise