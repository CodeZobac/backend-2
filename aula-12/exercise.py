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
