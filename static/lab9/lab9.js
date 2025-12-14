// static/lab9/lab9.js

// Открытие подарка
function openGift(giftId) {
    const giftBox = document.querySelector(`.gift-box[data-id="${giftId}"]`);
    const requireAuth = giftBox.getAttribute('data-require-auth') === 'True' || 
                        giftBox.getAttribute('data-require-auth') === 'true' || 
                        giftBox.getAttribute('data-require-auth') === '1';
    
    // Проверяем, открыт ли уже подарок
    if (giftBox.classList.contains('opened')) {
        showMessage('Этот подарок уже открыт!', 'warning');
        return;
    }
    
    // Проверяем, требуется ли авторизация
    if (requireAuth && !isAuthenticated()) {
        showMessage('Войдите в систему, чтобы открыть этот подарок!', 'warning');
        return;
    }
    
    // Отправляем запрос на открытие подарка
    fetch('/lab9/open_gift', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ gift_id: giftId })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Обновляем счетчики
            document.getElementById('opened-count').textContent = data.opened_count;
            document.getElementById('remaining-count').textContent = data.remaining;
            
            // Обновляем вид коробки
            updateGiftBox(giftId, data.message, data.image);
            giftBox.classList.add('opened');
            
            // Показываем сообщение об успехе
            showMessage(`🎉 Вы открыли подарок!`, 'success');
        } else {
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('Ошибка при открытии подарка', 'error');
    });
}

// Обновление вида коробки после открытия
function updateGiftBox(giftId, message, image) {
    const giftBox = document.querySelector(`.gift-box[data-id="${giftId}"]`);
    
    const content = `
        <div class="opened-gift">
            <div class="congratulation">
                <p>${message}</p>
            </div>
            <img src="${image}" alt="Подарок" class="gift-inside">
        </div>
    `;
    
    giftBox.innerHTML = content;
    giftBox.style.cursor = 'default';
    giftBox.style.opacity = '0.8';
}

// Показать сообщение
function showMessage(text, type) {
    const messageArea = document.getElementById('message-area');
    if (!messageArea) {
        // Создаем элемент, если его нет
        const div = document.createElement('div');
        div.id = 'message-area';
        div.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 10px;
            z-index: 1000;
            display: none;
            max-width: 300px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            backdrop-filter: blur(10px);
        `;
        document.body.appendChild(div);
    }
    
    const messageElement = document.getElementById('message-area');
    messageElement.textContent = text;
    messageElement.style.display = 'block';
    
    // Устанавливаем стили в зависимости от типа
    switch(type) {
        case 'success':
            messageElement.style.border = '2px solid #4caf50';
            messageElement.style.color = '#2e7d32';
            messageElement.style.backgroundColor = 'rgba(76, 175, 80, 0.9)';
            messageElement.style.color = 'white';
            break;
        case 'error':
            messageElement.style.border = '2px solid #f44336';
            messageElement.style.color = '#d32f2f';
            messageElement.style.backgroundColor = 'rgba(244, 67, 54, 0.9)';
            messageElement.style.color = 'white';
            break;
        case 'warning':
            messageElement.style.border = '2px solid #ff9800';
            messageElement.style.color = '#f57c00';
            messageElement.style.backgroundColor = 'rgba(255, 152, 0, 0.9)';
            messageElement.style.color = 'white';
            break;
    }
    
    // Автоматическое скрытие через 5 секунд
    setTimeout(() => {
        messageElement.style.display = 'none';
    }, 5000);
}

// Проверка авторизации
function isAuthenticated() {
    const authElement = document.getElementById('auth-status');
    return authElement && authElement.dataset.authenticated === 'true';
}

// Сброс подарков (Дед Мороз)
function resetGifts() {
    if (confirm('Вы уверены, что хотите сбросить все подарки? Дедушка Мороз наполнит их снова!')) {
        fetch('/lab9/santa', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                showMessage(data.message, 'success');
                setTimeout(() => {
                    location.reload();
                }, 1500);
            } else {
                showMessage(data.message, 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage('Ошибка при сбросе подарков: ' + error.message, 'error');
        });
    }
}

// Создание снежинок
function createSnowflakes() {
    const snowflakesContainer = document.querySelector('.snowflakes');
    if (!snowflakesContainer) return;
    
    for (let i = 0; i < 15; i++) {
        const snowflake = document.createElement('div');
        snowflake.className = 'snowflake';
        
        // Генерируем случайные значения
        const size = Math.random() * 10 + 5;
        const left = Math.random() * 100;
        const duration = Math.random() * 10 + 10;
        const delay = Math.random() * 5;
        const opacity = Math.random() * 0.5 + 0.3;
        
        snowflake.style.cssText = `
            width: ${size}px;
            height: ${size}px;
            left: ${left}%;
            top: -10px;
            animation-duration: ${duration}s;
            animation-delay: ${delay}s;
            opacity: ${opacity};
            background: white;
            border-radius: 50%;
            position: absolute;
            animation-name: fall;
            animation-timing-function: linear;
            animation-iteration-count: infinite;
        `;
        
        snowflakesContainer.appendChild(snowflake);
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Создаем снежинки
    createSnowflakes();
    
    // Добавляем обработчики клика на коробки
    const giftBoxes = document.querySelectorAll('.gift-box:not(.opened)');
    giftBoxes.forEach(box => {
        box.addEventListener('click', function() {
            const giftId = this.getAttribute('data-id');
            openGift(giftId);
        });
    });
    
    // Добавляем обработчик для кнопки Деда Мороза
    const santaBtn = document.getElementById('santa-btn');
    if (santaBtn) {
        santaBtn.addEventListener('click', resetGifts);
    }
    
    // Добавляем анимацию для коробок
    giftBoxes.forEach(box => {
        box.addEventListener('mouseenter', function() {
            if (!this.classList.contains('opened')) {
                this.style.transform = 'scale(1.1) rotate(5deg)';
                this.style.filter = 'drop-shadow(0 10px 20px rgba(255, 215, 0, 0.5))';
            }
        });
        
        box.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1) rotate(0deg)';
            this.style.filter = 'none';
        });
    });
});