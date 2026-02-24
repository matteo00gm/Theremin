package main

import (
	"log"
	"net"

	"action-service/internal/server"
	pb "action-service/pb"

	"google.golang.org/grpc"
)

func main() {
	// 1. Open the TCP port
	lis, err := net.Listen("tcp", ":50051")
	if err != nil {
		log.Fatalf("Failed to listen: %v", err)
	}

	// 2. Create the gRPC server instance
	grpcServer := grpc.NewServer()

	// 3. Instantiate our custom server logic
	hciServer := server.NewHCIServer()

	// 4. Register our logic with the gRPC framework
	pb.RegisterEyeTrackerServer(grpcServer, hciServer)

	log.Printf("Action Service listening at %v", lis.Addr())

	// 5. Start serving
	if err := grpcServer.Serve(lis); err != nil {
		log.Fatalf("Failed to serve: %v", err)
	}
}
