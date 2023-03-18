package face

import (
	"bytes"
	"context"
	"fmt"
	pb "gozo/face-detection/protocol"
	"gozo/face-detection/src/service/siamese"
	"io"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

func Upload(c *gin.Context) {
	// single file
	file, _ := c.FormFile("file")
	name := c.PostForm("name")
	ctx, cancel := context.WithTimeout(context.Background(), 1*time.Minute)
	defer cancel()
	src, err := file.Open()

	check(err)

	buf := bytes.NewBuffer(nil)

	io.Copy(buf, src)

	siameseStub := siamese.Client()

	// Upload the file to specific dst.
	res, err := siameseStub.StoreFace(ctx, &pb.StoreFaceRequest{File: buf.Bytes(), Name: name})

	check(err)

	c.String(http.StatusOK, fmt.Sprintf("Success is %v", res.Success))
}
