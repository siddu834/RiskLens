// ==========================================
// RISKLENS - THRESHOLD ANALYSIS
// ==========================================

let thresholdData = [];

const slider = document.getElementById("thresholdSlider");


// ==========================================
// LOAD THRESHOLD DATA
// ==========================================

async function loadThresholdData() {

    try {

        const response = await fetch(
            "data/threshold_metrics.json"
        );

        if (!response.ok) {
            throw new Error("Could not load threshold JSON");
        }

        thresholdData = await response.json();

        if (!Array.isArray(thresholdData) || thresholdData.length === 0) {
            throw new Error("Threshold data is empty or invalid");
        }

        document.getElementById("status").textContent =
            "Threshold data loaded successfully.";

        updateMetrics();

    }

    catch (error) {

        document.getElementById("status").textContent =
            "Error loading threshold data: " + error.message;

        console.error(error);

    }

}


// ==========================================
// UPDATE METRICS
// ==========================================

function updateMetrics() {

    if (thresholdData.length === 0) {
        return;
    }

    const selectedThreshold = Number(slider.value);

    // Find the nearest available threshold.
    const result = thresholdData.reduce((best, row) => {

        return Math.abs(row.threshold - selectedThreshold) <
               Math.abs(best.threshold - selectedThreshold)
            ? row
            : best;

    });

    document.getElementById("thresholdValue").textContent =
        Number(result.threshold).toFixed(2);

    document.getElementById("precision").textContent =
        (result.precision * 100).toFixed(2) + "%";

    document.getElementById("recall").textContent =
        (result.recall * 100).toFixed(2) + "%";

    document.getElementById("f1").textContent =
        Number(result.f1_score).toFixed(4);

    document.getElementById("flagRate").textContent =
        (result.flag_rate * 100).toFixed(2) + "%";

    document.getElementById("tp").textContent =
        Number(result.tp).toLocaleString();

    document.getElementById("fp").textContent =
        Number(result.fp).toLocaleString();

    document.getElementById("fn").textContent =
        Number(result.fn).toLocaleString();

    document.getElementById("tn").textContent =
        Number(result.tn).toLocaleString();

}


// ==========================================
// SLIDER EVENT
// ==========================================

slider.addEventListener("input", updateMetrics);


// ==========================================
// INITIALIZE
// ==========================================

loadThresholdData();
