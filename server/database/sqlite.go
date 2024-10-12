package database

import (
	"github.com/jonathangfletcher/fractal-explorer/server/models"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

func Connect() *gorm.DB {
	db, err := gorm.Open(sqlite.Open("/data/fractal-explorer.db"), &gorm.Config{})
	if err != nil {
		panic(err)
	}

	db.AutoMigrate(&models.VideoTask{})

	// prepare(db)
	return db
}

// func prepare(db *gorm.DB) {
// 	fmt.Println("Preparing database...")

// }
