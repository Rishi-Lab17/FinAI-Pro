/*
=========================================================
FinAI Pro
Charts JavaScript
=========================================================
*/

let incomeExpenseChart = null;
let categoryChart = null;
let predictionChart = null;


/*
=========================================================
Income vs Expense Chart
=========================================================
*/

function createIncomeExpenseChart(canvasId, labels, incomeData, expenseData) {

    const canvas = document.getElementById(canvasId);

    if (!canvas) {
        return;
    }

    if (incomeExpenseChart) {
        incomeExpenseChart.destroy();
    }

    incomeExpenseChart = new Chart(canvas, {

        type: "bar",

        data: {

            labels: labels,

            datasets: [

                {
                    label: "Income",

                    data: incomeData,

                    backgroundColor: "#16a34a",

                    borderRadius: 8
                },

                {
                    label: "Expense",

                    data: expenseData,

                    backgroundColor: "#dc2626",

                    borderRadius: 8
                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    position: "top"

                }

            }

        }

    });

}


/*
=========================================================
Expense Category Chart
=========================================================
*/

function createCategoryChart(canvasId, labels, values) {

    const canvas = document.getElementById(canvasId);

    if (!canvas) {
        return;
    }

    if (categoryChart) {
        categoryChart.destroy();
    }

    categoryChart = new Chart(canvas, {

        type: "doughnut",

        data: {

            labels: labels,

            datasets: [

                {

                    data: values,

                    backgroundColor: [

                        "#2563eb",
                        "#16a34a",
                        "#dc2626",
                        "#f59e0b",
                        "#8b5cf6",
                        "#06b6d4",
                        "#ec4899"

                    ]

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false

        }

    });

}


/*
=========================================================
Expense Prediction Chart
=========================================================
*/

function createPredictionChart(canvasId, labels, values) {

    const canvas = document.getElementById(canvasId);

    if (!canvas) {
        return;
    }

    if (predictionChart) {
        predictionChart.destroy();
    }

    predictionChart = new Chart(canvas, {

        type: "line",

        data: {

            labels: labels,

            datasets: [

                {

                    label: "Predicted Expense",

                    data: values,

                    borderColor: "#2563eb",

                    backgroundColor: "rgba(37,99,235,0.15)",

                    fill: true,

                    tension: 0.4

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false

        }

    });

}


/*
=========================================================
Financial Health Gauge
=========================================================
*/

function updateHealthScore(elementId, score) {

    const element = document.getElementById(elementId);

    if (!element) {
        return;
    }

    element.textContent = score + "%";

}


/*
=========================================================
Goal Progress
=========================================================
*/

function updateGoalProgress(progressId, percentage) {

    const progressBar = document.getElementById(progressId);

    if (!progressBar) {
        return;
    }

    progressBar.style.width = percentage + "%";

    progressBar.textContent = percentage + "%";

}


/*
=========================================================
Destroy All Charts
=========================================================
*/

function destroyCharts() {

    if (incomeExpenseChart) {

        incomeExpenseChart.destroy();

        incomeExpenseChart = null;

    }

    if (categoryChart) {

        categoryChart.destroy();

        categoryChart = null;

    }

    if (predictionChart) {

        predictionChart.destroy();

        predictionChart = null;

    }

}


