function verifyDomain() {
    let domainInput = document.getElementById("domainInput").value.trim();
    
    // Extract domain if an email is entered
    if (domainInput.includes("@")) {
        domainInput = domainInput.split("@")[1];
    }

    if (!domainInput) {
        alert("Please enter a valid domain or email");
        return;
    }

    fetch('/verify', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ domain: domainInput })
    })
    .then(response => response.json())
    .then(data => {
        let resultDiv = document.getElementById("result");
        resultDiv.innerHTML = `
            <p><strong>Domain:</strong> ${data.domain}</p>
            <p><strong>Status:</strong> ${data.status}</p>
            <p><strong>Resolved IP:</strong> ${data.resolved_ip || "Not found"}</p>
            <p><strong>WHOIS Info:</strong> ${data.whois || "Not found"}</p>
            <p><strong>MX Records:</strong> ${Array.isArray(data.mx_records) ? data.mx_records.join(", ") : "None"}</p>
            <p><strong>HTTP Status:</strong> ${data.http_status}</p>
        `;
    })
    .catch(error => console.error("Error:", error));
}
