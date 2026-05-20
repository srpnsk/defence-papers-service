// js/main.js
const { useState, useMemo, useEffect, useCallback } = React;

// ----------------------------------------------------------------------
// Валидация одного поля
// ----------------------------------------------------------------------
function validateField(field) {
    if (!field.value || String(field.value).trim() === '') {
        return 'Поле обязательно для заполнения';
    }
    const label = field.label || '';
    if (label.includes('Фамилия Имя Отчество')) {
        if (!/^[А-ЯЁ][А-ЯЁа-яё\-\s]*\s+[А-ЯЁ][а-яё\-]+(?:\s+[А-ЯЁ][а-яё\-]+)?$/.test(field.value.trim())) {
            return 'Формат: Иванов Иван Иванович или Иванов Иван';
        }
    } else if (label.includes('Фамилия И.О.')) {
        if (!/^[А-ЯЁ][А-ЯЁа-яё\-\s]*\s+[А-ЯЁ]\.(?:\s?[А-ЯЁ]\.)?$/.test(field.value.trim())) {
            return 'Формат: Иванов И.И. или Иванов И.';
        }
    }
    return null;
}

// ----------------------------------------------------------------------
// Проверка валидности всех полей текущего шага
// ----------------------------------------------------------------------
function isStepValid(step) {
    for (const group of step.groups) {
        if (group.type === 'single') {
            if (validateField(group.field)) return false;
        } else {
            for (const item of group.items) {
                if (validateField(item)) return false;
            }
        }
    }
    return true;
}

// ----------------------------------------------------------------------
// Главное приложение
// ----------------------------------------------------------------------
const App = () => {
    const [appState, setAppState] = useState('login');
    const [isPdfLoading, setIsPdfLoading] = useState(false);

    const [drafts, setDrafts] = useState(() => {
        const saved = localStorage.getItem('tex_drafts');
        return saved ? JSON.parse(saved) : [];
    });
    useEffect(() => {
        localStorage.setItem('tex_drafts', JSON.stringify(drafts));
    }, [drafts]);

    // Динамические настройки
    const [opponentCount, setOpponentCount] = useState(3);
    const [hasAdditionalJob, setHasAdditionalJob] = useState(false);
    const [hasHonorsDiploma, setHasHonorsDiploma] = useState(false);
    const [hasPostgradDiploma, setHasPostgradDiploma] = useState(false);
    const [specialtyItemCount, setSpecialtyItemCount] = useState(2);
    const [taskCount, setTaskCount] = useState(5);
    const [noveltyCount, setNoveltyCount] = useState(4);
    const [valueCount, setValueCount] = useState(3);
    const [provisionCount, setProvisionCount] = useState(4);
    const [articlesCount, setArticlesCount] = useState(3);
    const [conferencesCount, setConferencesCount] = useState(2);
    const [advisorArticlesCount, setAdvisorArticlesCount] = useState(7);
    const [opponentArticlesCount, setOpponentArticlesCount] = useState(5);
    const [commissionOffline, setCommissionOffline] = useState(10);
    const [commissionOnline, setCommissionOnline] = useState(5);
    const [defenceOffline, setDefenceOffline] = useState(11);
    const [defenceOnline, setDefenceOnline] = useState(4);
    const [showParams, setShowParams] = useState(true);

    const fields = useMemo(() => {
        return window.buildAllFields({
            opponentCount,
            hasAdditionalJob,
            hasHonorsDiploma,
            hasPostgradDiploma,
            specialtyItemCount,
            taskCount,
            noveltyCount,
            valueCount,
            provisionCount,
            articlesCount,
            conferencesCount,
            advisorArticlesCount,
            opponentArticlesCount,
            commissionOffline,
            commissionOnline,
            defenceOffline,
            defenceOnline
        });
    }, [opponentCount, hasAdditionalJob, hasHonorsDiploma, hasPostgradDiploma, specialtyItemCount, taskCount, noveltyCount, valueCount, provisionCount, articlesCount, conferencesCount, advisorArticlesCount, opponentArticlesCount, commissionOffline, commissionOnline, defenceOffline, defenceOnline]);

    const [currentFields, setCurrentFields] = useState(fields);
    useEffect(() => { setCurrentFields(fields); }, [fields]);

    const [currentStep, setCurrentStep] = useState(0);
    const [isMobile, setIsMobile] = useState(false);
    const [showErrors, setShowErrors] = useState(false);
    const [thesisId, setThesisId] = useState('');

    useEffect(() => {
        const checkMobile = () => setIsMobile(window.innerWidth < 768);
        checkMobile();
        window.addEventListener('resize', checkMobile);
        return () => window.removeEventListener('resize', checkMobile);
    }, []);

    const steps = useMemo(() => {
        const grouped = [];
        const files = [...new Set(currentFields.map(f => f.file))];
        files.forEach(file => {
            const fileFields = currentFields.filter(f => f.file === file);
            const sections = [...new Set(fileFields.map(f => f.section))];
            sections.forEach(section => {
                const rawFields = fileFields.filter(f => f.section === section);
                const groups = [];
                const groupedByName = {};
                const processedIds = new Set();
                rawFields.forEach(f => {
                    const match = f.id.match(/^(.*?)_?(\d+)$/);
                    if (match) {
                        const base = match[1];
                        if (!groupedByName[base]) groupedByName[base] = [];
                        groupedByName[base].push(f);
                    }
                });
                const repeatableBases = Object.keys(groupedByName).filter(base =>
                    groupedByName[base].some(f => f.id.endsWith('_1') || f.id.endsWith('1'))
                );
                rawFields.forEach(f => {
                    if (processedIds.has(f.id)) return;
                    const match = f.id.match(/^(.*?)_?(\d+)$/);
                    if (match && repeatableBases.includes(match[1])) {
                        const base = match[1];
                        const items = groupedByName[base];
                        let maxIdx = 0;
                        items.forEach(it => {
                            const m = it.id.match(/^(.*?)_?(\d+)$/);
                            if (m) maxIdx = Math.max(maxIdx, parseInt(m[2], 10));
                        });
                        groups.push({ type: 'repeatable', base, label: f.label || base, items, maxIdx });
                        items.forEach(it => processedIds.add(it.id));
                    } else {
                        groups.push({ type: 'single', field: f });
                        processedIds.add(f.id);
                    }
                });
                grouped.push({ file, section, groups });
            });
        });
        return grouped;
    }, [currentFields]);

    const handleChange = useCallback((id, newValue) => {
        setCurrentFields(prev => prev.map(f => f.id === id ? { ...f, value: newValue } : f));
    }, []);

    const addRepeatableField = useCallback((base, maxIdx, section, file, type, label) => {
        const newIdx = maxIdx + 1;
        const sample = currentFields.find(f => f.id.startsWith(base));
        let delimiter = "_";
        let sampleValue = '';
        if (sample) {
            const match = sample.id.match(/^(.*?)(_?)(\d+)$/);
            if (match) delimiter = match[2];
            sampleValue = sample.value || '';
        }
        if (!sampleValue || sampleValue.trim() === '') {
            sampleValue = 'Заполните данные';
        }
        const newId = `${base}${delimiter}${newIdx}`;
        const newField = {
            id: newId,
            value: sampleValue,
            type: type,
            label: `${label} (добавленный)`,
            section: section,
            file: file
        };
        setCurrentFields(prev => [...prev, newField]);
    }, [currentFields]);

    const removeRepeatableField = useCallback((id) => {
        setCurrentFields(prev => prev.filter(f => f.id !== id));
    }, []);

    const [serverTheses, setServerTheses] = useState([]);
    const loadServerTheses = useCallback(async () => {
        const data = await window.fetchMyTheses();
        if (data) setServerTheses(data);
        else if (data === null) setAppState('login');
    }, []);

    useEffect(() => {
        if (appState === 'dashboard') loadServerTheses();
    }, [appState, loadServerTheses]);

    const loadThesisIntoEditor = async (tid) => {
        const data = await window.loadThesisData(tid);
        if (data) {
            setCurrentFields(prev => prev.map(f => {
                if (data.hasOwnProperty(f.id)) {
                    const cleanValue = String(data[f.id] ?? "").replace(/~/g, ' ');
                    return { ...f, value: cleanValue };
                }
                return f;
            }));
            setThesisId(String(tid));
            setAppState('generator');
        } else {
            alert('Ошибка загрузки диссертации');
        }
    };

    const saveToServer = async () => {
        const data = {};
        currentFields.forEach(f => data[f.id] = f.value);
        const result = await window.saveThesis(data, thesisId);
        if (result) {
            if (result.thesis_id) setThesisId(String(result.thesis_id));
            alert('Сохранено');
        } else {
            alert('Ошибка сохранения');
        }
    };

    const handleLogin = async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const ok = await window.login(formData.get('email'), formData.get('password'));
        if (ok) setAppState('dashboard');
        else alert('Ошибка входа');
    };

    const handleRegister = async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const payload = {
            last_name: formData.get('last_name'),
            first_name: formData.get('first_name'),
            second_name: formData.get('second_name'),
            email: formData.get('email'),
            password: formData.get('password'),
            degree: '',
            academic_title: '',
            phone_number: '',
            specialty_id: null
        };
        const ok = await window.register(payload);
        if (ok) {
            alert('Регистрация успешна');
            setAppState('dashboard');
        } else {
            alert('Ошибка регистрации');
        }
    };

    const step = steps[currentStep];

    if (appState === 'login') {
        return (
            <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
                <div className="w-full max-w-md bg-white rounded-2xl shadow-xl p-8 space-y-6">
                    <div className="text-center">
                        <h1 className="text-2xl font-bold text-gray-900">Вход в систему</h1>
                    </div>
                    <form className="space-y-4" onSubmit={handleLogin}>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Email</label>
                            <input type="email" name="email" required className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500" />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Пароль</label>
                            <input type="password" name="password" required className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500" />
                        </div>
                        <button type="submit" className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700">
                            Войти
                        </button>
                    </form>
                    <div className="text-center">
                        <button onClick={() => setAppState('register')} className="text-sm text-blue-600 hover:text-blue-800">
                            Нет аккаунта? Зарегистрироваться
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    if (appState === 'register') {
        return (
            <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
                <div className="w-full max-w-md bg-white rounded-2xl shadow-xl p-8 space-y-6">
                    <div className="text-center">
                        <h1 className="text-2xl font-bold text-gray-900">Регистрация</h1>
                    </div>
                    <form className="space-y-4" onSubmit={handleRegister}>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Фамилия*</label>
                            <input type="text" name="last_name" required className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500" />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Имя*</label>
                            <input type="text" name="first_name" required className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500" />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Отчество</label>
                            <input type="text" name="second_name" className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500" />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Email*</label>
                            <input type="email" name="email" required className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500" />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Пароль (мин. 6 символов)*</label>
                            <input type="password" name="password" required minLength="6" className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500" />
                        </div>
                        <button type="submit" className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700">
                            Зарегистрироваться
                        </button>
                    </form>
                    <div className="text-center">
                        <button onClick={() => setAppState('login')} className="text-sm text-blue-600 hover:text-blue-800">
                            Уже есть аккаунт? Войти
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    if (appState === 'dashboard') {
        return (
            <div className="min-h-screen bg-gray-100">
                <nav className="bg-white shadow">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div className="flex justify-between h-16">
                            <div className="flex items-center">
                                <h1 className="text-xl font-bold text-blue-600">Личный кабинет</h1>
                            </div>
                            <div className="flex items-center">
                                <button onClick={() => setAppState('login')} className="ml-4 text-sm text-gray-500 hover:text-gray-700">Выйти</button>
                            </div>
                        </div>
                    </div>
                </nav>
                <main className="max-w-7xl mx-auto py-10 px-4 sm:px-6 lg:px-8">
                    <div className="bg-white rounded-lg shadow px-5 py-6 sm:px-6">
                        <div className="flex items-center justify-between mb-4">
                            <h2 className="text-lg leading-6 font-medium text-gray-900">Ваши документы</h2>
                            <button onClick={() => { setCurrentFields(fields); setCurrentStep(0); setThesisId(''); setAppState('generator'); }} className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700">
                                + Создать новые
                            </button>
                        </div>
                        {serverTheses.length === 0 ? (
                            <div className="border-4 border-dashed border-gray-200 rounded-lg h-64 flex flex-col items-center justify-center">
                                <p className="text-gray-500">Нет сохранённых диссертаций</p>
                            </div>
                        ) : (
                            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
                                {serverTheses.map(t => (
                                    <div key={t.id} className="rounded-lg border border-gray-300 bg-white px-6 py-5 shadow-sm hover:border-blue-500 transition-colors cursor-pointer" onClick={() => loadThesisIntoEditor(t.id)}>
                                        <p className="text-sm font-medium text-gray-900 truncate">{t.title}</p>
                                        <p className="text-sm text-gray-500">{t.target_degree}</p>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </main>
            </div>
        );
    }

    // Генератор
    return (
        <div className={`flex flex-col bg-gray-100 ${isMobile ? 'fixed inset-0 z-50' : 'fixed inset-0 z-50 items-center justify-center p-4 sm:p-6'}`}>
            {!isMobile && (
                <div className="w-full max-w-3xl mb-4 shrink-0 flex justify-between items-center">
                    <button onClick={() => setAppState('dashboard')} className="text-gray-500 hover:text-gray-700 text-sm font-medium">
                        ← Вернуться в ЛК
                    </button>
                    <div className="flex space-x-2">
                        <button onClick={() => setShowParams(true)} className="px-4 py-2 rounded-lg font-bold bg-blue-500 hover:bg-blue-600 text-white transition-colors shadow text-sm">
                            Настройки
                        </button>
                        <button onClick={saveToServer} className="px-4 py-2 rounded-lg font-bold bg-green-500 hover:bg-green-600 text-white transition-colors shadow text-sm">
                            Сохранить на сервер
                        </button>
                    </div>
                </div>
            )}
            {isMobile && (
                <div className="bg-gray-100 p-3 shrink-0 flex items-center justify-between border-b">
                    <button onClick={() => setAppState('dashboard')} className="text-gray-600 hover:text-gray-900 text-sm font-medium">
                        ← Назад
                    </button>
                    <div className="flex space-x-2">
                        <button onClick={() => setShowParams(true)} className="px-3 py-1.5 rounded-md bg-blue-500 text-white text-xs font-semibold">
                            Настройки
                        </button>
                        <button onClick={saveToServer} className="px-3 py-1.5 rounded-md bg-green-500 text-white text-xs font-semibold">
                            Сохранить
                        </button>
                    </div>
                </div>
            )}

            {/* ПАНЕЛЬ ПАРАМЕТРОВ */}
            {showParams && (
                <div className="w-full max-w-3xl mb-4 p-4 bg-white rounded-xl shadow">
                    <h3 className="text-lg font-bold mb-2">Параметры диссертации</h3>
                    <div className="grid grid-cols-2 gap-2">
                        <label className="text-sm">Количество оппонентов</label>
                        <input type="number" min="1" max="10" value={opponentCount}
                            onChange={(e) => setOpponentCount(Number(e.target.value))}
                            className="border rounded px-2" />

                        <label className="text-sm">Пунктов паспорта специальности</label>
                        <input type="number" min="1" max="10" value={specialtyItemCount}
                            onChange={(e) => setSpecialtyItemCount(Number(e.target.value))}
                            className="border rounded px-2" />

                        <label className="text-sm">Количество задач</label>
                        <input type="number" min="1" max="20" value={taskCount}
                            onChange={(e) => setTaskCount(Number(e.target.value))}
                            className="border rounded px-2" />

                        <label className="text-sm">Пунктов научной новизны</label>
                        <input type="number" min="1" max="20" value={noveltyCount}
                            onChange={(e) => setNoveltyCount(Number(e.target.value))}
                            className="border rounded px-2" />

                        <label className="text-sm">Пунктов практической ценности</label>
                        <input type="number" min="1" max="20" value={valueCount}
                            onChange={(e) => setValueCount(Number(e.target.value))}
                            className="border rounded px-2" />

                        <label className="text-sm">Положений</label>
                        <input type="number" min="1" max="20" value={provisionCount}
                            onChange={(e) => setProvisionCount(Number(e.target.value))}
                            className="border rounded px-2" />

                        <label className="text-sm">Статей соискателя</label>
                        <input type="number" min="1" max="50" value={articlesCount}
                            onChange={(e) => setArticlesCount(Number(e.target.value))}
                            className="border rounded px-2" />

                        <label className="text-sm">Конференций</label>
                        <input type="number" min="0" max="50" value={conferencesCount}
                            onChange={(e) => setConferencesCount(Number(e.target.value))}
                            className="border rounded px-2" />

                        <label className="text-sm">Статей руководителя</label>
                        <input type="number" min="0" max="50" value={advisorArticlesCount}
                            onChange={(e) => setAdvisorArticlesCount(Number(e.target.value))}
                            className="border rounded px-2" />

                        <label className="text-sm">Статей оппонента</label>
                        <input type="number" min="0" max="50" value={opponentArticlesCount}
                            onChange={(e) => setOpponentArticlesCount(Number(e.target.value))}
                            className="border rounded px-2" />

                        <label className="text-sm">Членов комиссии очно</label>
                        <input type="number" min="0" max="30" value={commissionOffline}
                            onChange={(e) => setCommissionOffline(Number(e.target.value))}
                            className="border rounded px-2" />

                        <label className="text-sm">Членов комиссии онлайн</label>
                        <input type="number" min="0" max="30" value={commissionOnline}
                            onChange={(e) => setCommissionOnline(Number(e.target.value))}
                            className="border rounded px-2" />

                        <label className="text-sm">Членов совета на защите очно</label>
                        <input type="number" min="0" max="30" value={defenceOffline}
                            onChange={(e) => setDefenceOffline(Number(e.target.value))}
                            className="border rounded px-2" />

                        <label className="text-sm">Членов совета на защите онлайн</label>
                        <input type="number" min="0" max="30" value={defenceOnline}
                            onChange={(e) => setDefenceOnline(Number(e.target.value))}
                            className="border rounded px-2" />

                        <label className="text-sm">Работа по совместительству</label>
                        <input type="checkbox" checked={hasAdditionalJob}
                            onChange={(e) => setHasAdditionalJob(e.target.checked)} />

                        <label className="text-sm">Диплом с отличием</label>
                        <input type="checkbox" checked={hasHonorsDiploma}
                            onChange={(e) => setHasHonorsDiploma(e.target.checked)} />

                        <label className="text-sm">Диплом об окончании аспирантуры</label>
                        <input type="checkbox" checked={hasPostgradDiploma}
                            onChange={(e) => setHasPostgradDiploma(e.target.checked)} />
                    </div>
                    <button className="mt-2 px-4 py-1 bg-blue-500 text-white rounded" onClick={() => {
                        setCurrentFields(fields);
                        setCurrentStep(0);
                        setShowParams(false);
                    }}>Продолжить</button>
                </div>
            )}

            {/* ОСНОВНОЙ РЕДАКТОР ШАГОВ */}
            <div className={`w-full max-w-3xl bg-white flex flex-col ${isMobile ? 'h-full flex-1' : 'shadow-xl rounded-2xl overflow-hidden h-[800px] max-h-full'}`}>
                <div className="bg-blue-600 p-4 sm:p-6 text-white flex justify-between items-center shrink-0">
                    <h2 className="text-lg sm:text-2xl font-bold">{step.section}</h2>
                    <div className="text-xs sm:text-sm font-medium bg-blue-700 px-3 py-1 rounded-full">
                        Шаг {currentStep + 1} из {steps.length}
                    </div>
                </div>
                
                <div className="p-4 sm:p-8 flex-1 overflow-y-auto space-y-6 sm:space-y-8">
                    {step.groups.map(group => {
                        if (group.type === 'single') {
                            return (
                                <window.FieldInput
                                    key={group.field.id}
                                    field={group.field}
                                    onChange={handleChange}
                                    showErrors={showErrors}
                                    validate={validateField}
                                />
                            );
                        } else {
                            return (
                                <window.RepeatableGroup
                                    key={group.base}
                                    group={group}
                                    onChange={handleChange}
                                    onAdd={addRepeatableField}
                                    onRemove={removeRepeatableField}
                                    showErrors={showErrors}
                                    validate={validateField}
                                    section={step.section}
                                    file={step.file}
                                />
                            );
                        }
                    })}
                </div>

                <div className="bg-gray-50 border-t border-gray-200 p-4 flex justify-between shadow-inner shrink-0">
                    <button disabled={currentStep === 0} onClick={() => { setShowErrors(false); setCurrentStep(prev => prev - 1); }} className={`px-4 sm:px-6 py-2 rounded-lg font-medium transition-colors ${currentStep === 0 ? 'bg-gray-200 text-gray-400 cursor-not-allowed' : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50'}`}>
                        Назад
                    </button>
                    {currentStep === steps.length - 1 ? (
                        <div className="flex space-x-2">
                            <button onClick={() => { if (isStepValid(step)) { window.downloadTexZip(currentFields); } else { setShowErrors(true); } }} className="px-4 py-2 rounded-lg font-bold bg-gray-500 hover:bg-gray-600 text-white transition-colors shadow text-sm">
                                Скачать .tex
                            </button>
                            <button onClick={() => { if (isStepValid(step)) { /* handleSendPDF using fetch */ } else { setShowErrors(true); } }} disabled={isPdfLoading} className={`px-4 sm:px-6 py-2 rounded-lg font-bold text-white transition-colors shadow ${isPdfLoading ? 'bg-green-400 cursor-not-allowed' : 'bg-green-500 hover:bg-green-600'}`}>
                                {isPdfLoading ? 'Генерация...' : 'Скачать PDF'}
                            </button>
                        </div>
                    ) : (
                        <button onClick={() => { if (isStepValid(step)) { setShowErrors(false); setCurrentStep(prev => prev + 1); } else { setShowErrors(true); } }} className="px-4 sm:px-6 py-2 rounded-lg font-bold bg-blue-600 hover:bg-blue-700 text-white transition-colors shadow">
                            Вперед
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);