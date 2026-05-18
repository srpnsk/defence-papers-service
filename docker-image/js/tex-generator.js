// js/tex-generator.js
// Генерация содержимого .tex файлов и упаковка в ZIP

/**
 * Генерирует TeX-код для одного .tex файла.
 * @param {string} file - Имя файла (например, "Sources/variables_common_input.tex")
 * @param {Array} fields - Массив всех полей формы
 * @returns {string} TeX-код
 */
window.generateTex = function(file, fields) {
    const fileFields = fields.filter(f => f.file === file);
    let mapBySection = {};
    fileFields.forEach(f => {
        if (!mapBySection[f.section]) mapBySection[f.section] = [];
        mapBySection[f.section].push(f);
    });

    let tex = '';
    for (const section in mapBySection) {
        tex += `% ${section}\n`;
        mapBySection[section].forEach(f => {
            // Очищаем значение от тильд (на всякий случай)
            const cleanValue = String(f.value || "").replace(/~/g, ' ');
            if (f.type === 'string') {
                tex += `\\setkomavar{${f.id}}{${cleanValue}} % ${f.label}\n`;
            } else {
                tex += `\\setcounter{${f.id}}{${cleanValue}} % ${f.label}\n`;
            }
        });
        tex += '\n';
    }
    return tex;
};

/**
 * Генерирует ZIP-архив со всеми .tex файлами и инициирует его скачивание.
 * @param {Array} fields - Массив всех полей формы
 */
window.downloadTexZip = function(fields) {
    const files = [...new Set(fields.map(f => f.file))];
    const zip = new JSZip();
    files.forEach(file => {
        const tex = window.generateTex(file, fields);
        zip.file(file.split('/').pop(), tex);
    });
    zip.generateAsync({ type: "blob" }).then(function(content) {
        const url = URL.createObjectURL(content);
        const a = document.createElement('a');
        a.href = url;
        a.download = "tex_sources.zip";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });
};