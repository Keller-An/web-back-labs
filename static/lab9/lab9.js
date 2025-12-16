function openGift(giftId) {
    const giftBox = document.querySelector(`.gift-box[data-id="${giftId}"]`);
    const requireAuth = giftBox.dataset.requireAuth === 'true' || giftBox.dataset.requireAuth === '1';

    if (giftBox.classList.contains('opened')) return showMessage('Подарок уже открыт!', 'warning');
    if (requireAuth && !isAuthenticated()) return showMessage('Войдите в систему, чтобы открыть этот подарок!', 'warning');

    fetch('/lab9/open_gift', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ gift_id: giftId })
    })
    .then(res => res.json())
    .then(data => {
        if (!data.success) return showMessage(data.message || 'Ошибка открытия подарка', 'error');

        document.getElementById('opened-count').textContent = data.opened_count;
        document.getElementById('remaining-count').textContent = data.remaining;

        updateGiftBox(giftId, data.image);
        giftBox.classList.add('opened');

        showGiftModal(data.message, data.image);
        showMessage('🎉 Подарок открыт!', 'success');
    })
    .catch(() => showMessage('Ошибка при открытии подарка', 'error'));
}

function updateGiftBox(giftId, image) {
    const giftBox = document.querySelector(`.gift-box[data-id="${giftId}"]`);
    giftBox.innerHTML = `<img src="${image}" class="gift-inside" alt="Подарок">`;
    giftBox.style.cursor = 'default';
    giftBox.style.opacity = '0.85';
}

// Модальное окно подарка
function showGiftModal(message, image) {
    const modal = document.getElementById('gift-modal');
    document.getElementById('modal-message').textContent = message;
    document.getElementById('modal-image').src = image;
    modal.classList.remove('hidden');
}

// Закрытие модалки
document.addEventListener('click', e => {
    if (e.target.classList.contains('modal-close') || e.target.id === 'gift-modal') {
        document.getElementById('gift-modal').classList.add('hidden');
    }
});

function showMessage(text, type='success') {
    let area = document.getElementById('message-area');
    if (!area) {
        area = document.createElement('div');
        area.id = 'message-area';
        area.style.cssText = 'position: fixed; top:10px; right: 45%; text-align: center; padding:12px 18px; border-radius:10px; z-index: 3000; max-width: 300px;';
        document.body.appendChild(area);
    }
    area.textContent = text;
    const colors = { success: '#4caf50', error: '#f44336', warning: '#ff9800' };
    area.style.backgroundColor = colors[type] || colors.success;
    area.style.color = 'white';
    area.style.display = 'block';
    setTimeout(() => area.style.display = 'none', 5000);
}

function isAuthenticated() {
    const auth = document.getElementById('auth-status');
    return auth && auth.dataset.authenticated === 'true';
}

function resetGifts() {
    if (!confirm('Сбросить все подарки?')) return;
    fetch('/lab9/santa', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            showMessage(data.message, data.success ? 'success' : 'error');
            if (data.success) setTimeout(() => location.reload(), 1500);
        });
}

function createNewYearDecorations() {
    const container = document.querySelector('.new-year-decorations');
    if (!container) return;

    const decorations = ['🥂', '🎁', '🍪', '☃️', '🟣', '🎀', '⭐', '🎄', '❄️', '✨'];
    
    for (let i = 0; i < 25; i++) {
        const dec = document.createElement('div');
        const size = Math.random() * 20 + 15;
        const symbol = decorations[Math.floor(Math.random() * decorations.length)];
        
        dec.className = 'new-year-decoration';
        dec.textContent = symbol;
        dec.style.cssText = `
            font-size: ${size}px;
            left: ${Math.random() * 100}%;
            top: -20px;
            position: absolute;
            opacity: ${Math.random() * 0.5 + 0.3};
            animation: decoration-fall ${Math.random() * 15 + 10}s linear ${Math.random() * 5}s infinite;
            z-index: 1;
            pointer-events: none;
            text-shadow: 0 0 5px rgba(255,255,255,0.5);
        `;
        container.appendChild(dec);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    createNewYearDecorations();

    document.querySelectorAll('.gift-box:not(.opened)').forEach(box => {
        box.addEventListener('click', () => openGift(box.dataset.id));
        box.addEventListener('mouseenter', () => {
            box.style.transform = 'scale(1.15) rotate(8deg)';
            box.style.boxShadow = '0 0 20px rgba(255, 215, 0, 0.7)';
        });
        box.addEventListener('mouseleave', () => {
            box.style.transform = 'scale(1) rotate(0deg)';
            box.style.boxShadow = 'none';
        });
    });

    const santaBtn = document.getElementById('santa-btn');
    if (santaBtn) santaBtn.addEventListener('click', resetGifts);
});