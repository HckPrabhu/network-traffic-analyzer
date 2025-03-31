document.addEventListener('DOMContentLoaded', function() {
    const updateDashboard = () => {
        fetch('/data')
            .then(response => response.json())
            .then(data => {
                // Update IP Chart
                document.getElementById('ipChart').innerHTML = 
                    Object.entries(data.top_ips).map(([ip, count]) => 
                        `<div>${ip}: ${count} packets</div>`
                    ).join('');

                // Update Protocol Chart
                document.getElementById('protocolChart').innerHTML = 
                    Object.entries(data.protocols).map(([proto, count]) => 
                        `<div>${proto}: ${count}</div>`
                    ).join('');

                // Update Plot
                document.getElementById('trafficPlot').src = data.plot;
            });
    };

    // Refresh every 5 seconds
    setInterval(updateDashboard, 5000);
    updateDashboard();
});
