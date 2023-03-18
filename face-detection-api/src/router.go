package src

import (
	"gozo/face-detection/src/controller/face"

	"github.com/gin-gonic/gin"
)

func Router() *gin.Engine {
	router := gin.Default()

	// Set a lower memory limit for multipart forms (default is 32 MiB)
	router.MaxMultipartMemory = 8 << 20 // 8 MiB
	router.POST("/recognize", face.Recognize)
	router.POST("/upload", face.Upload)

	return router
}
