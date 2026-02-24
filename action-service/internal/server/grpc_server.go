package server

import (
	"context"
	"fmt"
	"io"
	"log"
	"time"

	"action-service/internal/action"
	pb "action-service/pb"
)

type HCIServer struct {
	pb.UnimplementedEyeTrackerServer
	Mouse *action.MouseController
}

func NewHCIServer() *HCIServer {
	return &HCIServer{
		Mouse: action.NewMouseController(),
	}
}

// StreamCoordinates is the function the vision service calls to start streaming data
func (s *HCIServer) StreamCoordinates(stream pb.EyeTracker_StreamCoordinatesServer) error {
	log.Println("Vision Sensor connected to the stream!")

	for {
		point, err := stream.Recv()

		if err == io.EOF {
			log.Println("Vision Sensor disconnected cleanly.")
			return stream.SendAndClose(&pb.StreamStatus{
				Success: true,
				Message: "Stream ended normally",
			})
		}

		if err != nil {
			log.Printf("Error receiving from stream: %v", err)
			return err
		}

		// Calculate latency
		now := time.Now().UnixMilli()
		latency := now - point.Timestamp

		fmt.Printf("Received -> X: %.4f, Y: %.4f | Conf: %.2f | Latency: %dms\n",
			point.X, point.Y, point.Confidence, latency)

		// Move the OS mouse cursor
		s.Mouse.MoveCursor(point.X, point.Y)
	}
}

// SendClick receives the trigger from the audio-service and commands the MouseController to click.
func (s *HCIServer) SendClick(ctx context.Context, req *pb.Empty) (*pb.ClickResponse, error) {

	s.Mouse.Click()

	return &pb.ClickResponse{Success: true}, nil
}
