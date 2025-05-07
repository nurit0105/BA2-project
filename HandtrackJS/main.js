document.addEventListener('DOMContentLoaded', () => {
  const video = document.getElementById('video');
  const canvas = document.getElementById('canvas');
  const context = canvas.getContext('2d');
  const gestureOutput = document.getElementById('gestureOutput');

  const modelParams = {
    flipHorizontal: true,  // Flip the video horizontally for a mirror effect
    maxNumBoxes: 1,       // Track only one hand
    scoreThreshold: 0.6,   // Minimum confidence for predictions
  };

  let model;

  // Step 1: Request webcam access
  navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
      video.srcObject = stream;
      video.onloadedmetadata = () => {
        video.play();

        // Step 2: Load the handtrack model
        handTrack.load(modelParams).then((loadedModel) => {
          model = loadedModel;
          runDetection();
        });
      };
    })
    .catch(err => {
      alert("Webcam access denied or error: " + err.message);
    });

  // Step 3: Run Hand Detection and Track Gestures
  function runDetection() {
    model.detect(video).then((predictions) => {
      context.clearRect(0, 0, canvas.width, canvas.height); // Clear previous frames
      model.renderPredictions(predictions, canvas, context, video);

      if (predictions.length > 0) {
        // Handle the first (or only) hand detected
        const hand = predictions[0];
        const landmarks = hand.landmarks; // Get the landmarks of the detected hand

        // Finger gesture tracking logic
        const { indexFinger, middleFinger, ringFinger } = getFingerStatus(landmarks);

        let gesture = '';

        if (indexFinger && middleFinger && ringFinger) {
          gesture = 'Showing Three Fingers';
        } else if (indexFinger && middleFinger) {
          gesture = 'Showing Two Fingers';
        } else if (indexFinger) {
          gesture = 'Showing One Finger';
        } else {
          gesture = 'No relevant gesture';
        }

        gestureOutput.innerText = gesture; // Display the gesture on the screen
      }

      requestAnimationFrame(runDetection); // Repeat the detection loop
    });
  }

  // Helper function to track specific fingers (Index, Middle, Ring)
  function getFingerStatus(landmarks) {
    let indexFinger = false;
    let middleFinger = false;
    let ringFinger = false;

    // Finger landmarks (using indices from the hand landmarks array)
    const indexTip = landmarks[8]; // Index finger tip
    const middleTip = landmarks[12]; // Middle finger tip
    const ringTip = landmarks[16]; // Ring finger tip
    const indexBase = landmarks[6]; // Index base

    // Check if the tips of the fingers are above the base (bent fingers)
    if (indexTip.y < indexBase.y) indexFinger = true;
    if (middleTip.y < indexBase.y) middleFinger = true;
    if (ringTip.y < indexBase.y) ringFinger = true;

    return { indexFinger, middleFinger, ringFinger };
  }
});
