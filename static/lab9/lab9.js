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

// Снежинки
function createSnowflakes() {
    const container = document.querySelector('.snowflakes');
    if (!container) return;

    for (let i = 0; i < 20; i++) {
        const s = document.createElement('div');
        const size = Math.random()*10+5;
        s.className = 'snowflake';
        s.style.cssText = `
            width:${size}px; height:${size}px;
            left:${Math.random()*100}%; top:-10px;
            background:white; border-radius:50%; position:absolute;
            opacity:${Math.random()*0.5+0.3};
            animation: fall ${Math.random()*10+10}s linear ${Math.random()*5}s infinite;
        `;
        container.appendChild(s);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    createSnowflakes();

    document.querySelectorAll('.gift-box:not(.opened)').forEach(box => {
        box.addEventListener('click', () => openGift(box.dataset.id));
        box.addEventListener('mouseenter', () => box.style.transform = 'scale(1.1) rotate(5deg)');
        box.addEventListener('mouseleave', () => box.style.transform = 'scale(1)');
    });

    const santaBtn = document.getElementById('santa-btn');
    if (santaBtn) santaBtn.addEventListener('click', resetGifts);
});
