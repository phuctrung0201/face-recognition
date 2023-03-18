package main

import (
	"flag"

	"gozo/face-detection/src"
	"gozo/face-detection/src/service/siamese"
)

var (
	serverAddr = flag.String("addr", "localhost:50051", "The server address in the format of host:port")
	filePath   = flag.String("file-path", "elephant.jpeg", "The path to load image")
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func main() {

	conn := siamese.GetConnection()
	defer conn.Close()
	router := src.Router()
	router.Run(":8080")
}
