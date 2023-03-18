package siamese

import (
	"fmt"
	pb "gozo/face-detection/protocol"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

var (
	siameseStub pb.SiameseClient
	connection  *grpc.ClientConn
)
var serverAddr = "localhost:50051"

func Client() pb.SiameseClient {
	if siameseStub != nil {
		return siameseStub
	}

	conn := GetConnection()

	siameseStub = pb.NewSiameseClient(conn)

	return siameseStub
}

func GetConnection() *grpc.ClientConn {
	if connection != nil {
		return connection
	}

	conn, err := grpc.Dial(serverAddr, grpc.WithTransportCredentials(insecure.NewCredentials()))

	if err != nil {
		fmt.Printf("Failed to create TLS credentials %v", err)
	}

	connection = conn

	return connection
}
