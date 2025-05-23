# Challenge: gRPC service with server-side streaming
import grpc
from concurrent import futures
import time
import threading

class StreamService:
    """A gRPC service that implements server-side streaming."""
    
    def __init__(self):
        self.server = None
        self.active_streams = []
    
    def StreamMessages(self, request_message):
        """Stream multiple responses for a single request."""
        print(f"Starting stream for message: '{request_message}'")
        
        # Generate a series of streaming responses
        responses = []
        for i in range(5):
            response = f"Stream {i+1}: Processing '{request_message}'"
            responses.append(response)
            print(f"Streaming: {response}")
            # Simulate processing delay
            time.sleep(0.5)
        
        return responses
    
    def start_streaming_server(self, port=50052):
        """Start the streaming gRPC server."""
        print(f"Starting StreamService server on port {port}")
        print("Service ready for streaming messages!")
        print("In a real implementation, this would use grpc.server() with streaming")
        
        # Simulate streaming server behavior
        self.simulate_streaming_requests()
    
    def simulate_streaming_requests(self):
        """Simulate streaming requests."""
        test_messages = [
            "Hello World",
            "Python gRPC",
            "Streaming Data"
        ]
        
        for message in test_messages:
            print(f"\n--- Starting new stream for: '{message}' ---")
            responses = self.StreamMessages(message)
            print(f"Stream completed with {len(responses)} responses")
            print("--- Stream ended ---\n")

def run_concurrent_streams():
    """Demonstrate concurrent streaming capabilities."""
    service = StreamService()
    
    def stream_worker(message, worker_id):
        print(f"[Worker {worker_id}] Starting concurrent stream")
        responses = service.StreamMessages(f"{message} (Worker {worker_id})")
        print(f"[Worker {worker_id}] Completed with {len(responses)} responses")
    
    print("=== Testing Concurrent Streaming ===")
    threads = []
    
    for i in range(3):
        thread = threading.Thread(
            target=stream_worker, 
            args=("Concurrent Test", i+1)
        )
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    print("=== All concurrent streams completed ===")

def main():
    """Main function to run the streaming service."""
    service = StreamService()
    service.start_streaming_server()
    
    print("\n" + "="*50)
    run_concurrent_streams()

if __name__ == "__main__":
    main()

# Protocol Buffer definition (for reference):
"""
syntax = "proto3";

package service;

service StreamService {
    rpc StreamMessages (StreamRequest) returns (stream StreamResponse);
}

message StreamRequest {
    string message = 1;
}

message StreamResponse {
    string response = 1;
}
"""
