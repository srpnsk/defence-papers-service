// js/api.js
// Модуль для взаимодействия с серверным API

/**
 * Вход в систему.
 * @param {string} email
 * @param {string} password
 * @returns {Promise<boolean>} true, если вход успешен
 */
window.login = async function(email, password) {
    try {
        const resp = await fetch(`${window.API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password }),
            credentials: 'include'
        });
        return resp.ok;
    } catch (e) {
        console.error(e);
        return false;
    }
};

/**
 * Регистрация нового пользователя.
 * @param {Object} data - поля: last_name, first_name, second_name, email, password
 * @returns {Promise<boolean>} true, если регистрация успешна
 */
window.register = async function(data) {
    try {
        const resp = await fetch(`${window.API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
            credentials: 'include'
        });
        return resp.ok;
    } catch (e) {
        console.error(e);
        return false;
    }
};

/**
 * Получить список диссертаций текущего пользователя.
 * @returns {Promise<Array|null>} Массив диссертаций или null при ошибке
 */
window.fetchMyTheses = async function() {
    try {
        const resp = await fetch(`${window.API_BASE_URL}/api/my-theses`, {
            credentials: 'include'
        });
        if (resp.ok) {
            return await resp.json();
        } else if (resp.status === 401) {
            return null;
        }
        return null;
    } catch (e) {
        console.error(e);
        return null;
    }
};

/**
 * Загрузить данные диссертации по ID.
 * @param {number} thesisId
 * @returns {Promise<Object|null>} JSON с данными формы или null
 */
window.loadThesisData = async function(thesisId) {
    try {
        const resp = await fetch(`${window.API_BASE_URL}/api/thesis/${thesisId}/form-data`, {
            credentials: 'include'
        });
        if (resp.ok) {
            const data = await resp.json();
            // Заменяем тильды на пробелы во всех значениях
            for (const key in data) {
                if (typeof data[key] === 'string') {
                    data[key] = data[key].replace(/~/g, ' ');
                }
            }
            return data;
        }
        return null;
    } catch (e) {
        console.error(e);
        return null;
    }
};

/**
 * Сохранить (создать или обновить) диссертацию.
 * @param {Object} data - объект вида {field_id: value, ...}
 * @param {string|null} thesisId - ID диссертации (null для создания новой)
 * @returns {Promise<Object|null>} ответ сервера (свойство thesis_id при создании) или null
 */
window.saveThesis = async function(data, thesisId) {
    const url = thesisId
        ? `${window.API_BASE_URL}/api/thesis/${thesisId}/form-data`
        : `${window.API_BASE_URL}/api/thesis/form-data`;
    try {
        const resp = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
            credentials: 'include'
        });
        if (resp.ok) {
            return await resp.json();
        }
        return null;
    } catch (e) {
        console.error(e);
        return null;
    }
};