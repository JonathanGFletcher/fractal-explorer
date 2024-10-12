package models

import (
	"gorm.io/gorm"
)

type VideoTask struct {
	Id              int            `json:"id" gorm:"primaryKey;autoIncrement"`
	SessionId       string         `json:"session_id"`
	DeletedAt       gorm.DeletedAt `json:"deleted_at" gorm:"index"`
	Completed       bool           `json:"completed"`
	TotalFrames     int            `json:"total_frames"`
	CompletedFrames int            `json:"completed_frames"`
}
