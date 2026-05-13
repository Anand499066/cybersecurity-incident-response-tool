document.addEventListener("DOMContentLoaded", function () {
  const notifications = document.querySelectorAll(".notification");

  notifications.forEach((notification) => {
    setTimeout(() => {
      notification.style.transition = "all 0.5s ease";

      notification.style.opacity = "0";

      notification.style.transform = "translateY(-20px)";

      setTimeout(() => {
        notification.remove();
      }, 500);
    }, 3000);
  });
});
// =========================
// Live Threat Feed
// =========================

const attackMessages = [
  "SQL Injection Attempt Detected",
  "Brute Force Login Attempt",
  "Phishing Email Reported",
  "Unauthorized Access Attempt",
  "DDoS Traffic Spike Detected",
  "Ransomware Signature Found",
  "Suspicious IP Connected",
  "Firewall Rule Triggered",
];

function addFeedItem() {
  const attackFeed = document.getElementById("attackFeed");

  if (!attackFeed) return;

  const randomMessage =
    attackMessages[Math.floor(Math.random() * attackMessages.length)];

  const now = new Date();

  const time = now.toLocaleTimeString();

  const div = document.createElement("div");

  div.classList.add("feed-item");

  div.innerText = `[${time}] ${randomMessage}`;

  attackFeed.prepend(div);
  // =========================
  // Global Threat Activity
  // =========================

  const countries = [
    "USA",
    "Russia",
    "China",
    "Germany",
    "India",
    "Brazil",
    "North Korea",
    "UK",
    "France",
    "Canada",
  ];

  const threats = [
    "SQL Injection Attempt",
    "Brute Force Attack",
    "DDoS Traffic Spike",
    "Phishing Campaign",
    "Ransomware Detection",
    "Unauthorized Access",
    "Malware Infection",
  ];

  function addThreatActivity() {
    const threatMap = document.getElementById("threatMap");

    if (!threatMap) return;

    const country = countries[Math.floor(Math.random() * countries.length)];

    const threat = threats[Math.floor(Math.random() * threats.length)];

    const now = new Date();

    const time = now.toLocaleTimeString();

    const div = document.createElement("div");

    div.classList.add("threat-item");

    div.innerText = `[${time}] 🌍 ${country} - ${threat}`;

    threatMap.prepend(div);

    // Limit Entries

    if (threatMap.children.length > 8) {
      threatMap.removeChild(threatMap.lastChild);
    }
  }

  // Add Every 6 Seconds

  setInterval(addThreatActivity, 6000);

  // Limit Feed Size

  if (attackFeed.children.length > 8) {
    attackFeed.removeChild(attackFeed.lastChild);
  }
}

// Add New Feed Item Every 5 Seconds

setInterval(addFeedItem, 5000);
// =========================
// Animated Dashboard Counters
// =========================

const counters =
    document.querySelectorAll(".counter");

counters.forEach(counter => {

    counter.innerText = "0";

    const updateCounter = () => {

        const target =
            Number(counter.dataset.target);

        const current =
            Number(counter.innerText);

        const increment =
            target / 50;

        if (current < target) {

            counter.innerText =
                `${Math.ceil(
                    current + increment
                )}`;

            setTimeout(updateCounter, 40);

        } else {

            counter.innerText = target;

        }

    };

    updateCounter();

});
// =========================
// Dark / Light Theme Toggle
// =========================

const themeToggle =
    document.getElementById(
        "themeToggle"
    );

if (themeToggle) {

    themeToggle.addEventListener(
        "click",
        () => {

            document.body.classList.toggle(
                "light-theme"
            );

        }
    );

}
// =========================
// Cyber Alert Sounds
// =========================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        const sound =
            document.getElementById(
                "alertSound"
            );

        if (!sound) return;

        const notifications =
            document.querySelectorAll(
                ".notification"
            );

        notifications.forEach(notification => {

            const text =
                notification.innerText
                .toLowerCase();

            if (
                text.includes("critical") ||
                text.includes("attack") ||
                text.includes("brute")
            ) {

                // Small delay helps browser

                setTimeout(() => {

                    sound.currentTime = 0;

                    sound.play()
                    .catch(error => {

                        console.log(
                            "Audio blocked:",
                            error
                        );

                    });

                }, 500);

            }

        });

    }
);
// =========================
// Real-Time Attack Trend Chart
// =========================

const liveChartCanvas =
    document.getElementById(
        "liveAttackChart"
    );

if (liveChartCanvas) {

    const liveLabels = [];

    const liveData = [];

    const liveAttackChart =
        new Chart(liveChartCanvas, {

            type: "line",

            data: {

                labels: liveLabels,

                datasets: [{

                    label: "Attack Traffic",

                    data: liveData,

                    borderColor: "#ef4444",

                    backgroundColor:
                        "rgba(239,68,68,0.2)",

                    tension: 0.4,

                    fill: true

                }]

            },

            options: {

                responsive: true,

                scales: {

                    y: {

                        beginAtZero: true

                    }

                }

            }

        });

    function updateLiveChart() {

        const now =
            new Date()
            .toLocaleTimeString();

        const randomValue =
            Math.floor(
                Math.random() * 100
            );

        liveLabels.push(now);

        liveData.push(randomValue);

        // Keep only latest 10 points

        if (liveLabels.length > 10) {

            liveLabels.shift();

            liveData.shift();

        }

        liveAttackChart.update();

    }

    // Update every 3 seconds

    setInterval(updateLiveChart, 3000);

}