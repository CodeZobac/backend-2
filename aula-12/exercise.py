# Exercise: Basic gRPC service that returns the cube of a number
import grpc
from concurrent import futures
import sys
import os

# Since we don't have the actual protobuf generated files,
# we'll simulate the gRPC service structure

class CubeService:
    """A simple gRPC service that calculates the cube of a number."""
    
    def __init__(self):
        self.server = None
    
    def GetCube(self, request_number):
        """Calculate the cube of a given number."""
        result = request_number ** 3
        print(f"Calculating cube of {request_number} = {result}")
        return result
    
    def start_server(self, port=50051):
        """Start the gRPC server."""
        print(f"Starting CubeService server on port {port}")
        print("Service ready to calculate cubes!")
        print("In a real implementation, this would use grpc.server()")
        
        # Simulate server behavior
        self.simulate_requests()
    
    def simulate_requests(self):
        """Simulate some cube calculation requests."""
        test_numbers = [2, 3, 4, 5, 10]
        
        for number in test_numbers:
            cube = self.GetCube(number)
            print(f"Request: GetCube({number}) -> Response: {cube}")
        
        print("\nServer simulation complete!")

def main():
    """Main function to run the cube service."""
    service = CubeService()
    service.start_server()

if __name__ == "__main__":
    main()

# Protocol Buffer definition (for reference):
"""
syntax = "proto3";

package service;

service CubeService {
    rpc GetCube (CubeRequest) returns (CubeResponse);
}

message CubeRequest {
    int32 number = 1;
}

message CubeResponse {
    int32 cube = 1;
}
"""
