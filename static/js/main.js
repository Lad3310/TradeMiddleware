document.addEventListener('DOMContentLoaded', function() {
    const auditTrailTable = document.getElementById('audit-trail-table');
    const fileUploadForm = document.getElementById('file-upload-form');
    const dashboardStats = document.getElementById('dashboard-stats');

    if (auditTrailTable) {
        initializeAuditTrail(auditTrailTable);
    }

    if (fileUploadForm) {
        initializeFileUpload(fileUploadForm);
    }

    if (dashboardStats) {
        fetchDashboardStats();
    }
});

function initializeAuditTrail(table) {
    table.addEventListener('click', function(e) {
        if (e.target && e.target.classList.contains('view-trades-btn')) {
            const auditLogId = e.target.getAttribute('data-audit-log-id');
            fetchProcessedTrades(auditLogId);
        }
    });

    const headers = table.querySelectorAll('th');
    headers.forEach(header => {
        header.addEventListener('click', () => {
            const column = header.dataset.column;
            const order = header.dataset.order = header.dataset.order === 'asc' ? 'desc' : 'asc';
            sortTable(table, column, order);
        });
    });
}

function initializeFileUpload(form) {
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(form);
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            showModal(data.status, data.message, data.details);
            if (data.status === 'success') {
                form.reset();
                fetchDashboardStats();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showModal('error', 'An error occurred while uploading the file.');
        });
    });
}

function fetchProcessedTrades(auditLogId) {
    fetch(`/api/trades/${auditLogId}`)
        .then(response => response.json())
        .then(data => {
            displayProcessedTrades(data);
        })
        .catch(error => {
            console.error('Error:', error);
            showModal('error', 'An error occurred while fetching trade data.');
        });
}

function displayProcessedTrades(trades) {
    const modal = createModal('Processed Trades');
    const table = document.createElement('table');
    table.innerHTML = `
        <thead>
            <tr>
                <th>Trade ID</th>
                <th>Symbol</th>
                <th>Quantity</th>
                <th>Price</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            ${trades.map(trade => `
                <tr>
                    <td>${trade.trade_id}</td>
                    <td>${trade.symbol}</td>
                    <td>${trade.quantity}</td>
                    <td>${trade.price}</td>
                    <td>${trade.status}</td>
                </tr>
            `).join('')}
        </tbody>
    `;
    modal.querySelector('.modal-content').appendChild(table);
    document.body.appendChild(modal);
}

function sortTable(table, column, order) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const sortedRows = rows.sort((a, b) => {
        const aValue = a.querySelector(`td[data-column="${column}"]`).textContent;
        const bValue = b.querySelector(`td[data-column="${column}"]`).textContent;
        return order === 'asc' ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue);
    });
    tbody.innerHTML = '';
    sortedRows.forEach(row => tbody.appendChild(row));
}

function showModal(status, message, details = null) {
    const modal = createModal(status === 'success' ? 'Success' : status === 'warning' ? 'Warning' : 'Error');
    const content = document.createElement('div');
    content.innerHTML = `
        <p>${message}</p>
        ${details ? `
            <h4>API Simulation Details:</h4>
            <p>Attempts: ${details.attempts}</p>
            <p>Total Delay: ${details.total_delay.toFixed(2)} seconds</p>
        ` : ''}
    `;
    modal.querySelector('.modal-content').appendChild(content);
    document.body.appendChild(modal);
}

function createModal(title) {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <span class="close">&times;</span>
            <h2>${title}</h2>
        </div>
    `;
    modal.querySelector('.close').onclick = function() {
        document.body.removeChild(modal);
    };
    return modal;
}

function fetchDashboardStats() {
    fetch('/api/dashboard_stats')
        .then(response => response.json())
        .then(data => {
            updateDashboardStats(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function updateDashboardStats(data) {
    const statsContainer = document.getElementById('dashboard-stats');
    if (!statsContainer) return;

    statsContainer.innerHTML = `
        <h3>Upload Statistics</h3>
        <p>Total Files: ${data.total_files}</p>
        <p>Successful Uploads: ${data.successful_uploads}</p>
        <p>Failed Uploads: ${data.failed_uploads}</p>
        <h3>Recent Uploads</h3>
        <ul>
            ${data.recent_uploads.map(upload => `
                <li>${upload.filename} - ${upload.status} (${upload.timestamp})</li>
            `).join('')}
        </ul>
    `;
}
