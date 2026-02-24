"""
Orchestrates the microphone detector and gRPC client for touchless clicking.
"""
import os
import logging
import time
from dotenv import load_dotenv
from core.detector import AcousticDetector
from network.grpc_client import AudioClient

# Load configuration from the .env file one folder up
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

GRPC_TARGET = f"{os.getenv('GRPC_HOST', 'localhost')}:{os.getenv('GRPC_PORT', '50051')}"

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main():
    logging.info(f"Initializing audio components (Target: {GRPC_TARGET})...")
    
    # Initialize the core sensor and network client
    detector = AcousticDetector()
    client = AudioClient(target_address=GRPC_TARGET)

    logging.info("Audio listener running. Make a 'pop' sound to click!")
    logging.info("Press Ctrl+C to quit.")

    try:
        # The main sensor loop
        while True:
            # If the detector registers a pop, tell the gRPC client to fire
            if detector.process_chunk():
                logging.info("POP DETECTED! Sending click...")
                client.send_click()
                
            # A tiny sleep prevents the while loop from maxing out a CPU core
            time.sleep(0.001)

    except KeyboardInterrupt:
        logging.info("Shutting down audio service...")
    finally:
        # Graceful teardown
        detector.close()
        client.close()

if __name__ == "__main__":
    main()