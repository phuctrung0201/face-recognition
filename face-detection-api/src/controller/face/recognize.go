package face

import (
	"bytes"
	"context"
	"fmt"
	"gozo/face-detection/src/service/siamese"
	"io"
	"net/http"
	"time"

	pb "gozo/face-detection/protocol"

	"github.com/gin-gonic/gin"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func Recognize(c *gin.Context) {
	// single file
	file, _ := c.FormFile("file")
	ctx, cancel := context.WithTimeout(context.Background(), 1*time.Minute)
	defer cancel()
	src, err := file.Open()

	check(err)

	buf := bytes.NewBuffer(nil)

	io.Copy(buf, src)

	siameseStub := siamese.Client()

	// Upload the file to specific dst.
	res, err := siameseStub.Predict(ctx, &pb.PredictRequest{File: buf.Bytes()})

	check(err)

	c.String(http.StatusOK, fmt.Sprintf("May be %s", res.Name))
}
