"""
Orchestrates the microphone detector and gRPC client for touchless clicking.
"""
import logging
import time
from core.detector import AcousticDetector
from network.grpc_client import AudioClient

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main():
    logging.info("Initializing audio components...")
    
    # Initialize the core sensor and network client
    detector = AcousticDetector()
    client = AudioClient(target_address='localhost:50051')

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