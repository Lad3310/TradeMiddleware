document.addEventListener('DOMContentLoaded', function() {
    const auditTrailTable = document.getElementById('audit-trail-table');
    if (auditTrailTable) {
        auditTrailTable.addEventListener('click', function(e) {
            if (e.target && e.target.classList.contains('view-trades-btn')) {
                const auditLogId = e.target.getAttribute('data-audit-log-id');
                fetchProcessedTrades(auditLogId);
            }
        });
    }
});

function fetchProcessedTrades(auditLogId) {
    fetch(`/api/trades/${auditLogId}`)
        .then(response => response.json())
        .then(data => {
            displayProcessedTrades(data);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while fetching trade data.');
        });
}

function displayProcessedTrades(trades) {
    const modal = document.createElement('div');
    modal.style.position = 'fixed';
    modal.style.left = '0';
    modal.style.top = '0';
    modal.style.width = '100%';
    modal.style.height = '100%';
    modal.style.backgroundColor = 'rgba(0,0,0,0.5)';
    modal.style.display = 'flex';
    modal.style.justifyContent = 'center';
    modal.style.alignItems = 'center';

    const content = document.createElement('div');
    content.style.backgroundColor = '#fff';
    content.style.padding = '20px';
    content.style.borderRadius = '5px';
    content.style.maxWidth = '80%';
    content.style.maxHeight = '80%';
    content.style.overflow = 'auto';

    const closeBtn = document.createElement('button');
    closeBtn.textContent = 'Close';
    closeBtn.onclick = function() {
        document.body.removeChild(modal);
    };

    const table = document.createElement('table');
    const headerRow = table.insertRow();
    ['Trade ID', 'Symbol', 'Quantity', 'Price', 'Status'].forEach(text => {
        const th = document.createElement('th');
        th.textContent = text;
        headerRow.appendChild(th);
    });

    trades.forEach(trade => {
        const row = table.insertRow();
        [trade.trade_id, trade.symbol, trade.quantity, trade.price, trade.status].forEach(text => {
            const cell = row.insertCell();
            cell.textContent = text;
        });
    });

    content.appendChild(table);
    content.appendChild(closeBtn);
    modal.appendChild(content);
    document.body.appendChild(modal);
}
