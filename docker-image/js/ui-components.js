// js/ui-components.js
// Переиспользуемые UI-компоненты для формы диссертации

/**
 * Универсальный компонент поля ввода.
 * @param {Object} field - объект поля (id, value, type, label, inputType, ...)
 * @param {Function} onChange - callback(id, newValue)
 * @param {boolean} showErrors - показывать ли ошибки валидации
 * @param {Function|null} validate - функция валидации (возвращает строку ошибки или null)
 */
window.FieldInput = function({ field, onChange, showErrors, validate }) {
    const error = validate ? validate(field) : null;
    const commonClasses = `border rounded-lg px-4 py-2.5 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all shadow-sm w-full ${showErrors && error ? 'border-red-500 bg-red-50' : 'border-gray-300'}`;

    const handleChange = (e) => onChange(field.id, e.target.value);

    const labelEl = React.createElement('label', { className: 'text-sm font-semibold text-gray-700 mb-2' }, field.label);

    let inputEl;
    switch (field.inputType) {
        case 'text':
        case 'tel':
        case 'email':
            inputEl = React.createElement('input', {
                type: field.inputType === 'tel' ? 'tel' : field.inputType === 'email' ? 'email' : 'text',
                value: field.value,
                onChange: handleChange,
                className: commonClasses
            });
            break;
        case 'number':
            inputEl = React.createElement('input', {
                type: 'number',
                value: field.value,
                onChange: handleChange,
                className: commonClasses
            });
            break;
        case 'date':
            inputEl = React.createElement('input', {
                type: 'date',
                value: field.value,
                onChange: handleChange,
                className: commonClasses
            });
            break;
        case 'time':
            inputEl = React.createElement('input', {
                type: 'time',
                value: field.value,
                onChange: handleChange,
                className: commonClasses
            });
            break;
        case 'degree_select':
            inputEl = React.createElement('select', { value: field.value, onChange: handleChange, className: commonClasses },
                React.createElement('option', { value: '' }, 'Выберите степень'),
                window.DEGREES.map(deg => React.createElement('option', { key: deg, value: deg }, deg))
            );
            break;
        case 'title_select':
            inputEl = React.createElement('select', { value: field.value, onChange: handleChange, className: commonClasses },
                React.createElement('option', { value: '' }, 'Выберите звание'),
                window.TITLES.map(t => React.createElement('option', { key: t, value: t }, t))
            );
            break;
        case 'doc_select':
            inputEl = React.createElement('select', { value: field.value, onChange: handleChange, className: commonClasses },
                React.createElement('option', { value: '' }, 'Выберите тип документа'),
                window.DOC_TYPES.map(d => React.createElement('option', { key: d, value: d }, d))
            );
            break;
        case 'sex_select':
            inputEl = React.createElement('select', { value: field.value, onChange: handleChange, className: commonClasses },
                React.createElement('option', { value: '1' }, 'Мужской'),
                React.createElement('option', { value: '2' }, 'Женский')
            );
            break;
        case 'specialty_select':
            inputEl = React.createElement('select', { value: field.value, onChange: handleChange, className: commonClasses },
                React.createElement('option', { value: '' }, 'Выберите специальность'),
                window.SPECIALTIES.map(s => React.createElement('option', { key: s, value: s }, s))
            );
            break;
        case 'quartile_select':
            inputEl = React.createElement('select', { value: field.value, onChange: handleChange, className: commonClasses },
                React.createElement('option', { value: '' }, 'Выберите квартиль'),
                window.QUARTILES.map(q => React.createElement('option', { key: q, value: q }, q))
            );
            break;
        default:
            inputEl = React.createElement('input', {
                type: 'text',
                value: field.value,
                onChange: handleChange,
                className: commonClasses
            });
    }

    const errorEl = showErrors && error ? React.createElement('span', { className: 'text-red-500 text-xs mt-1' }, error) : null;

    return React.createElement('div', { className: 'flex flex-col' },
        labelEl,
        inputEl,
        errorEl
    );
};

/**
 * Компонент для группы повторяющихся полей (с возможностью добавления/удаления).
 * @param {Object} group - { base, label, items, maxIdx }
 * @param {Function} onChange - callback(id, newValue)
 * @param {Function} onAdd - callback(base, maxIdx, section, file, type, label)
 * @param {Function} onRemove - callback(id)
 * @param {boolean} showErrors
 * @param {Function} validate
 * @param {string} section
 * @param {string} file
 */
window.RepeatableGroup = function({ group, onChange, onAdd, onRemove, showErrors, validate, section, file }) {
    const items = [...group.items].sort((a, b) => {
        const m1 = a.id.match(/\d+$/);
        const m2 = b.id.match(/\d+$/);
        return (m1 ? parseInt(m1[0], 10) : 0) - (m2 ? parseInt(m2[0], 10) : 0);
    });
    const sampleType = items[0]?.type || 'string';

    const handleAdd = () => onAdd(group.base, group.maxIdx, section, file, sampleType, group.label);

    const children = [
        React.createElement('div', { key: 'header', className: 'flex justify-between items-center mb-2' },
            React.createElement('h3', { className: 'font-bold text-gray-800 text-sm' }, group.label),
            React.createElement('button', {
                onClick: handleAdd,
                className: 'bg-blue-100 text-blue-700 hover:bg-blue-200 px-3 py-1.5 rounded-md text-xs font-semibold transition-colors shadow-sm'
            }, '+ Добавить пункт')
        )
    ];

    items.forEach(field => {
        const error = validate ? validate(field) : null;
        const itemDiv = React.createElement('div', {
            key: field.id,
            className: `flex space-x-2 sm:space-x-3 items-start bg-white p-2 sm:p-3 rounded-lg border ${showErrors && error ? 'border-red-500 bg-red-50' : 'border-gray-100'} shadow-sm relative group`
        },
            React.createElement('div', { className: 'flex-1 flex flex-col w-full' },
                React.createElement(window.FieldInput, {
                    field: field,
                    onChange: onChange,
                    showErrors: showErrors,
                    validate: validate
                })
            ),
            React.createElement('button', {
                onClick: () => onRemove(field.id),
                className: 'text-gray-400 hover:text-red-500 hover:bg-red-50 p-1.5 rounded self-center transition-colors flex-shrink-0',
                title: 'Удалить'
            },
                React.createElement('svg', { xmlns: 'http://www.w3.org/2000/svg', className: 'h-5 w-5', viewBox: '0 0 20 20', fill: 'currentColor' },
                    React.createElement('path', {
                        fillRule: 'evenodd',
                        clipRule: 'evenodd',
                        d: 'M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z'
                    })
                )
            )
        );
        children.push(itemDiv);
    });

    if (items.length === 0) {
        children.push(React.createElement('p', { key: 'empty', className: 'text-sm text-gray-400 italic text-center py-2' }, 'Нет пунктов. Нажмите добавить.'));
    }

    return React.createElement('div', { className: 'bg-gray-50 p-4 border border-gray-200 rounded-xl flex flex-col space-y-4 shadow-sm' }, ...children);
};

/**
 * Чекбокс с подписью (для флагов).
 */
window.CheckboxField = function({ id, checked, label, onChange }) {
    return React.createElement('div', { className: 'flex items-center space-x-2' },
        React.createElement('input', {
            type: 'checkbox',
            id: id,
            checked: checked,
            onChange: (e) => onChange(id, e.target.checked),
            className: 'h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'
        }),
        React.createElement('label', { htmlFor: id, className: 'text-sm font-medium text-gray-700' }, label)
    );
};