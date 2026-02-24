package main

import (
	"log"
	"net"
	"os"
	"path/filepath"

	"action-service/internal/server"
	pb "action-service/pb"

	"github.com/joho/godotenv"
	"google.golang.org/grpc"
)

func main() {
	// 1. Load the .env file from the parent directory
	envPath := filepath.Join("..", ".env")
	if err := godotenv.Load(envPath); err != nil {
		log.Println("No .env file found, using defaults.")
	}

	// 2. Read the port with a fallback
	port := os.Getenv("GRPC_PORT")
	if port == "" {
		port = "50051"
	}
	target := ":" + port

	// 3. Open the TCP port
	lis, err := net.Listen("tcp", target)
	if err != nil {
		log.Fatalf("Failed to listen: %v", err)
	}

	// 4. Create and register the gRPC server
	grpcServer := grpc.NewServer()
	hciServer := server.NewHCIServer()
	pb.RegisterEyeTrackerServer(grpcServer, hciServer)

	log.Printf("Action Service listening at %v", lis.Addr())

	// 5. Start serving
	if err := grpcServer.Serve(lis); err != nil {
		log.Fatalf("Failed to serve: %v", err)
	}
}
