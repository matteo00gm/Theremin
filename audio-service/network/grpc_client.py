"""
Handles synchronous gRPC Unary calls to the action-service for mouse clicks.
"""
import grpc
import sys
import os
import logging

# Dynamically add the 'pb' directory to Python's path
pb_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pb'))
sys.path.append(pb_dir)

import tracker_pb2
import tracker_pb2_grpc

class AudioClient:
    def __init__(self, target_address='localhost:50051'):
        self.target = target_address
        self.channel = grpc.insecure_channel(self.target)
        self.stub = tracker_pb2_grpc.EyeTrackerStub(self.channel)
        logging.info(f"gRPC Audio Client connected, targeting {self.target}")

    def send_click(self):
        """Sends an immediate click command to the Go backend."""
        try:
            req = tracker_pb2.Empty()
            resp = self.stub.SendClick(req, timeout=0.5)
            
            if not resp.success:
                logging.warning("Action service received click but reported failure.")
        except grpc.RpcError as e:
            logging.error(f"gRPC connection failed: {e.code().name} - {e.details()}")

    def close(self):
        self.channel.close()