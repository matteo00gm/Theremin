package action

import (
	"log"
	"os"
	"strconv"

	"github.com/go-vgo/robotgo"
)

// MouseController manages operating system cursor interactions.
type MouseController struct {
	ScreenWidth  int
	ScreenHeight int
	LastX        float32
	LastY        float32
	Smoothing    float32
}

// NewMouseController initializes the controller with the primary display dimensions.
func NewMouseController() *MouseController {
	width, height := robotgo.GetScreenSize()
	log.Printf("Screen dimensions detected: %dx%d", width, height)

	// Default smoothing value
	smoothing := float32(0.30)

	// Override from .env if present
	if envSmooth := os.Getenv("MOUSE_SMOOTHING"); envSmooth != "" {
		if s, err := strconv.ParseFloat(envSmooth, 32); err == nil {
			smoothing = float32(s)
		}
	}

	return &MouseController{
		ScreenWidth:  width,
		ScreenHeight: height,
		Smoothing:    smoothing, // Lower = smoother, Higher = faster
	}
}

// MoveCursor applies exponential smoothing and moves the OS cursor.
func (m *MouseController) MoveCursor(targetX, targetY float32) {
	// Formula: Current = Previous + (Target - Previous) * Smoothing
	// This prevents the mouse from 'teleporting' and makes it 'glide'
	smoothX := m.LastX + (targetX-m.LastX)*m.Smoothing
	smoothY := m.LastY + (targetY-m.LastY)*m.Smoothing

	// Store for next frame
	m.LastX = smoothX
	m.LastY = smoothY

	pixelX := int(smoothX * float32(m.ScreenWidth))
	pixelY := int(smoothY * float32(m.ScreenHeight))

	robotgo.Move(pixelX, pixelY)
}

// Click performs an OS-level mouse click.
func (m *MouseController) Click() {
	button := "left"

	robotgo.Click(button)
}
