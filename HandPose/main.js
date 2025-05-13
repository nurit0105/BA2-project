const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const statusEl = document.getElementById('status');

async function setupCamera() {
    const stream = await navigator.mediaDevices.getUserMedia({video: true});
    video.srcObject = stream;
    return new Promise(resolve => {
        video.onloadedmetadata = () => resolve(video);
    });
}

function isFingerUp(landmarks, tip, pip) {
    return landmarks[tip][1] < landmarks[pip][1];
}

let selectedCircle = document.getElementById('1');
selectedCircle.style.outline = '5px solid yellow';

async function main() {
    await setupCamera();
    const model = await handpose.load();
    statusEl.textContent = 'Model Loaded';

    async function detect() {
        const predictions = await model.estimateHands(video, true);
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        if (predictions.length > 0) {
            const landmarks = predictions[0].landmarks;


            // Draws Landmarks
            for (let i = 0; i < landmarks.length; i++) {
                const [x, y] = landmarks[i];

                const mirroredX = canvas.width - x;

                ctx.beginPath();
                ctx.arc(mirroredX, y, 5, 0, 2 * Math.PI);
                ctx.fillStyle = 'lime';
                ctx.fill();
                ctx.fillText(i, mirroredX + 5, y - 5);
            }


            // Finger detection
            const index = isFingerUp(landmarks, 8, 6);
            const middle = isFingerUp(landmarks, 12, 10);
            const ring = isFingerUp(landmarks, 16, 14);
            const pinky = isFingerUp(landmarks, 20, 17);

            const fingersUp = [index, middle, ring, pinky].filter(Boolean).length;

            document.querySelectorAll('.circle').forEach(circle => {
                circle.style.outline = '';
            });

            handleFingerDetection(fingersUp);

            // display which fingers are up
            const labels = ['Index', 'Middle', 'Ring', 'Pinky'];
            const statusText = [index, middle, ring, pinky]
                .map((val, i) => val ? labels[i] : null)
                .filter(Boolean)
                .join(', ');
            statusEl.textContent = statusText || 'No fingers up';
        }

        requestAnimationFrame(detect);
    }

    detect();
}
// Logic for Life Video Stream Gesture Detection and LED Simulation
function handleFingerDetection(fingersUp) {
    let newSelection;

    if (fingersUp === 1) {
        newSelection = document.getElementById('1');
        if (selectedCircle !== newSelection) {
            selectedCircle.classList.remove('selected');
            selectedCircle = newSelection;
            selectedCircle.classList.add('selected');
        }
        console.log("Showing One Finger");
    } else if (fingersUp === 2) {
        newSelection = document.getElementById('2');
        if (selectedCircle !== newSelection) {
            selectedCircle.classList.remove('selected');
            selectedCircle = newSelection;
            selectedCircle.classList.add('selected');
        }
        console.log("Showing Two Fingers");
    } else if (fingersUp === 3) {
        selectedCircle.classList.remove('red');
        selectedCircle.classList.add('green');
        console.log("Showing Three Fingers");
    } else if (fingersUp === 4) {
        selectedCircle.classList.remove('green');
        selectedCircle.classList.add('red');
        console.log("Showing Four Fingers");
    } else {
        console.log("Finger Count out of Scope");
    }
}

main();

// Test Data Set for Performance Test
const testImages = [
    // not 1 to 4 fingers (a fist)
    {src: "../Test_images/own-fist.jpg", label: 0},
    {src: "../Test_images/0-person-01.jpg", label: 0},
    {src: "../Test_images/0-person-02.jpg", label: 0},
    {src: "../Test_images/0-person-03.jpg", label: 0},
    {src: "../Test_images/0-person-04.jpg", label: 0},
    {src: "../Test_images/0-person-05.jpg", label: 0},
    {src: "../Test_images/0-person-06.jpg", label: 0},
    {src: "../Test_images/0-person-07.jpg", label: 0},
    {src: "../Test_images/0-person-08.jpg", label: 0},

    // showing one finger
    {src: "../Test_images/own-one-finger.jpg", label: 1},
    {src: "../Test_images/1-person-01.jpg", label: 1},
    {src: "../Test_images/1-person-02.jpg", label: 1},
    {src: "../Test_images/1-person-03.jpg", label: 1},
    {src: "../Test_images/1-person-04.jpg", label: 1},
    {src: "../Test_images/1-person-05.jpg", label: 1},
    {src: "../Test_images/1-person-06.jpg", label: 1},
    {src: "../Test_images/1-person-07.jpg", label: 1},
    {src: "../Test_images/1-person-08.jpg", label: 1},

    // showing two fingers
    {src: "../Test_images/own-two-fingers.jpg", label: 2},
    {src: "../Test_images/2-person-01.jpg", label: 2},
    {src: "../Test_images/2-person-02.jpg", label: 2},
    {src: "../Test_images/2-person-03.jpg", label: 2},
    {src: "../Test_images/2-person-04.jpg", label: 2},
    {src: "../Test_images/2-person-05.jpg", label: 2},
    {src: "../Test_images/2-person-06.jpg", label: 2},
    {src: "../Test_images/2-person-07.jpg", label: 2},
    {src: "../Test_images/2-person-08.jpg", label: 2},

    // showing three fingers
    {src: "../Test_images/own-three-fingers.jpg", label: 3},
    {src: "../Test_images/3-person-01.jpg", label: 3},
    {src: "../Test_images/3-person-02.jpg", label: 3},
    {src: "../Test_images/3-person-03.jpg", label: 3},
    {src: "../Test_images/3-person-04.jpg", label: 3},
    {src: "../Test_images/3-person-05.jpg", label: 3},
    {src: "../Test_images/3-person-06.jpg", label: 3},
    {src: "../Test_images/3-person-07.jpg", label: 3},
    {src: "../Test_images/3-person-08.jpg", label: 3},

    // showing four fingers
    {src: "../Test_images/own-four-fingers.jpg", label: 4},
    {src: "../Test_images/4-person-01.jpg", label: 4},
    {src: "../Test_images/4-person-02.jpg", label: 4},
    {src: "../Test_images/4-person-03.jpg", label: 4},
    {src: "../Test_images/4-person-04.jpg", label: 4},
    {src: "../Test_images/4-person-05.jpg", label: 4},
    {src: "../Test_images/4-person-06.jpg", label: 4},
    {src: "../Test_images/4-person-07.jpg", label: 4},
    {src: "../Test_images/4-person-08.jpg", label: 4},
];


function createConfusionMatrix(numClasses) {
    const matrix = Array.from({length: numClasses}, () =>
        Array(numClasses).fill(0)
    );
    return matrix;
}

const confusionMatrix = createConfusionMatrix(5); // 5 Klassen: 0–4
// UI Creation of Matrix
function renderConfusionMatrix(matrix) {
    const container = document.getElementById('confusionMatrixTable');
    let html = '<table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">';

    // Header row
    html += '<tr><th>Actual \\ Pred</th>';
    for (let i = 0; i < matrix.length; i++) {
        html += `<th>${i}</th>`;
    }
    html += '</tr>';

    // Matrix rows
    for (let i = 0; i < matrix.length; i++) {
        html += `<tr><th>${i}</th>`;
        for (let j = 0; j < matrix[i].length; j++) {
            html += `<td>${matrix[i][j]}</td>`;
        }
        html += '</tr>';
    }

    html += '</table>';
    container.innerHTML = html;
}
// Logic for Calculating Performance Metrics
function calculateMetrics(confusionMatrix) {
    const numClasses = confusionMatrix.length;
    const total = confusionMatrix.flat().reduce((a, b) => a + b, 0);

    let macroPrecision = 0;
    let macroRecall = 0;
    let macroF1 = 0;
    let macroAccuracy = 0;

    for (let i = 0; i < numClasses; i++) {
        const TP = confusionMatrix[i][i];
        const FP = confusionMatrix.reduce((sum, row, r) => r !== i ? sum + row[i] : sum, 0);
        const FN = confusionMatrix[i].reduce((sum, val, c) => c !== i ? sum + val : sum, 0);
        const TN = total - TP - FP - FN;

        const precision = TP + FP === 0 ? 0 : TP / (TP + FP);
        const recall = TP + FN === 0 ? 0 : TP / (TP + FN);
        const f1 = precision + recall === 0 ? 0 : 2 * (precision * recall) / (precision + recall);
        const accuracy = (TP + TN) / total;

        macroPrecision += precision;
        macroRecall += recall;
        macroF1 += f1;
        macroAccuracy += accuracy;
    }

    macroPrecision /= numClasses;
    macroRecall /= numClasses;
    macroF1 /= numClasses;
    macroAccuracy /= numClasses;

    return {
        macroPrecision: macroPrecision.toFixed(3),
        macroRecall: macroRecall.toFixed(3),
        macroF1: macroF1.toFixed(3),
        macroAccuracy: macroAccuracy.toFixed(3)
    };
}

// Testing the Performance
async function testPerformance() {
    const model = await handpose.load();
    const resultsContainer = document.getElementById("results");
    resultsContainer.innerHTML = "";
    for (const test of testImages) {
        try {
            const img = new Image();
            img.src = test.src;

            await img.decode();

            const predictions = await model.estimateHands(img);
            let predicted = 0;

            // Prediction for each finger
            if (predictions.length > 0) {
                const landmarks = predictions[0].landmarks;

                const index = isFingerUp(landmarks, 8, 5);
                const middle = isFingerUp(landmarks, 12, 9);
                const ring = isFingerUp(landmarks, 16, 13);
                const pinky = isFingerUp(landmarks, 20, 18);

                predicted = [index, middle, ring, pinky].filter(Boolean).length;
            }

            const actual = test.label;
            confusionMatrix[actual][predicted] += 1;

            const isCorrect = predicted === actual;
            // Displaying the Images and the Results of the prediction
            const resultHtml = `
        <div style="margin:10px; padding:10px; border:1px solid gray;">
          <img src="${test.src}" width="150" />
          <p>Expected: ${actual} Predicted: ${predicted}
          ${isCorrect ? "Correct" : "Wrong"}</p>
        </div>
      `;
            resultsContainer.innerHTML += resultHtml;

        } catch (err) {
            console.error(`Error processing image ${test.src}:`, err);
            resultsContainer.innerHTML += `
        <div style="margin:10px; padding:10px; border:1px solid red;">
          <p> Failed to process image: ${test.src}</p>
        </div>
      `;
        }
    }

    console.log("Confusion Matrix:");
    console.table(confusionMatrix);
    renderConfusionMatrix(confusionMatrix);

    const metrics = calculateMetrics(confusionMatrix);

    // Displaying the Results of the total Performance Metrics
    document.getElementById("metricsDisplay").innerHTML = `
  <h3>Macro-Averaged Metrics</h3>
  <ul>
    <li><strong>Precision:</strong> ${metrics.macroPrecision}</li>
    <li><strong>Recall:</strong> ${metrics.macroRecall}</li>
    <li><strong>F1 Score:</strong> ${metrics.macroF1}</li>
    <li><strong>Accuracy:</strong> ${metrics.macroAccuracy}</li>
  </ul>
`;
}