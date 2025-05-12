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
