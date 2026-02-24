"""
Handles asynchronous gRPC streaming to the action-service.
"""
import grpc, queue, threading, time, sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pb')))
import tracker_pb2, tracker_pb2_grpc

class GazeStreamer:
    def __init__(self, target_address):
        self.channel = grpc.insecure_channel(target_address)
        self.stub = tracker_pb2_grpc.EyeTrackerStub(self.channel)
        
        # Maxsize prevents memory leaks if the server is offline
        self.queue = queue.Queue(maxsize=60) 
        self.is_streaming = False
        self._thread = None

    def start(self):
        """Starts the background streaming thread."""
        self.is_streaming = True
        self._thread = threading.Thread(target=self._stream_loop, daemon=True)
        self._thread.start()

    def stop(self):
        """Cleanly shuts down the stream."""
        self.is_streaming = False
        if self._thread:
            self._thread.join(timeout=1.0)
        self.channel.close()

    def send_point(self, x, y, confidence):
        """Pushes a coordinate to the queue to be sent to Go."""
        if self.is_streaming:
            try: self.queue.put_nowait((x, y, confidence, time.time_ns() // 1_000_000))
            except queue.Full: pass

    def _generate_messages(self):
        """Yields messages from the queue to the gRPC stream."""
        while self.is_streaming:
            try:
                # Timeout allows the loop to periodically check if is_streaming is False
                x, y, conf, ts = self.queue.get(timeout=0.1)
                yield tracker_pb2.GazePoint(x=x, y=y, confidence=conf, timestamp=ts)
            except queue.Empty: pass

    def _stream_loop(self):
        """The core loop running in the background thread."""
        try: self.stub.StreamCoordinates(self._generate_messages())
        except grpc.RpcError: pass