# Project Theremin

## Overview

Project Theremin is a low latency, touchless Human-Computer Interface (HCI). It allows users to control their computer mouse entirely hands-free using a webcam for movement (via pinch gestures) and a microphone for clicking (via acoustic "pop" detection).

The application is built on a robust, three-service architecture communicating via gRPC microservices:
* **action-service (Go):** The gRPC server that receives network commands and executes OS-level mouse movements and clicks using `robotgo`.
* **movement-service (Python):** The vision sensor using `mediapipe`. Tracks hand landmarks, calculates relative pinch-and-drag movements, and streams coordinates in real time.
* **audio-service (Python):** The acoustic sensor using `pyaudio`. Listens for sharp transient volume spikes and sends click triggers.

## System Prerequisites

Because this project interfaces directly with operating system-level hardware for mouse control and audio/video capture, requirements strictly vary by underlying operating system. All platforms require **Python 3.x, Go, a functional webcam, and a functional microphone**.

* **Windows:** No extra system libraries needed.
* **macOS:** Must run `brew install portaudio`. Note that macOS will heavily restrict usage initially and prompt for "Accessibility" and "Camera/Microphone" permissions on the first run.
* **Linux:** Must run `sudo apt-get install portaudio19-dev python3-pyaudio libx11-dev x11proto-core-dev libxtst-dev` to enable X11 cursor control and system audio access.

## Local Setup & Installation

Follow these explicit steps to configure the project for local execution.

### Step 1: Clone the Repository

Retrieve the project source code using your preferred terminal:

```bash
git clone https://github.com/matteo00gm/project-theremin.git
cd project-theremin
```

### Step 2: Initialize Dependencies

Execute the initialization sequence which automatically creates Python virtual environments, installs dependencies from `requirements.txt`, and initializes Go modules.

```bash
make init
```

### Step 3: Generate gRPC Network Code

Generate the essential gRPC network code for all three microservices to strictly establish inter-service communication protocols.

```bash
make proto
```

## Running the Application

To launch Project Theremin, simply execute the following command in your terminal:

```bash
make run
```

This command launches all three microservices simultaneously as isolated background processes.

## Usage

Once the application is actively running in the background, you can immediately control your cursor using the following multimodal inputs:

* **Mouse Movement (Drag):** Pinch your fingers together within the camera's field of view and move your hand to steadily drag the cursor across the screen.
* **Mouse Click:** Produce a sharp "pop" sound with your mouth in closer proximity to the microphone to precisely execute a click event.
