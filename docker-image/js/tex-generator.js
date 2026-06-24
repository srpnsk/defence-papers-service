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
 * Генерирует ZIP-архив с правильной структурой папок и статическими файлами.
 * @param {Array} fields - Массив всех полей формы
 */
window.downloadTexZip = async function(fields) {
    const zip = new JSZip();

    const staticFiles = [
        "assets/Sources/commands.tex",
        "assets/Sources/screenshot_01.png", // заглушка
        "assets/Sources/variables_01.tex",
        "assets/Sources/variables_common.tex",
        "assets/Sources/variables_02.tex",
        "assets/Templates/11_1.tex",
        "assets/Templates/11_2.tex",
        "assets/Templates/11_3.tex",
        "assets/Templates/13.tex",
        "assets/Templates/15.tex",
        "assets/Templates/18_1.tex",
        "assets/Templates/19_2.tex",
        "assets/Templates/20.tex",
        "assets/Templates/21.tex",
        "assets/Templates/2_M.tex",
        "assets/Templates/2_F.tex",
        "assets/Templates/3.tex",
        "assets/Templates/9.tex",
        "assets/01_Before_acceptance.tex",
        "assets/02_Acceptance_panel.tex",
        "assets/style.sty"
    ];

    try {
        // 2. Скачиваем всю статику параллельно
        const downloadPromises = staticFiles.map(async (filePath) => {
            const response = await fetch(`/${filePath}`); // Корректируйте URL под ваш сервер
            if (!response.ok) throw new Error(`Не удалось скачать файл: ${filePath}`);
            const blob = await response.blob();
            
            const cleanArchivePath = filePath.replace(/^assets\//, "");
            
            zip.file(cleanArchivePath, blob);
        });

        // Ждем завершения всех загрузок
        await Promise.all(downloadPromises);

        // 3. Генерируем динамические .tex файлы на основе полей формы
        const uniqueDynamicFiles = [...new Set(fields.map(f => f.file))];
        
        uniqueDynamicFiles.forEach(file => {
            const texContent = window.generateTex(file, fields);
            // Важно: передаем 'file' целиком (например, "Sources/variables_common_input.tex")
            // JSZip сам разберется с вложенными папками
            zip.file(file, texContent);
        });

        // 4. Генерация самого архива и триггер скачивания
        const content = await zip.generateAsync({ type: "blob" });
        
        const url = URL.createObjectURL(content);
        const a = document.createElement('a');
        a.href = url;
        a.download = "thesis_sources.zip";
        document.body.appendChild(a);
        a.click();
        
        // Чистим за собой память
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

    } catch (error) {
        console.error("Ошибка при формировании ZIP-архива:", error);
        alert("Произошла ошибка при сборке архива. Проверьте консоль.");
    }
};

window.compileOnServer = async function(fields) {
    const files = [...new Set(fields.map(f => f.file))];
    
    // Формируем структуру, которую ожидает Питон: {"Sources/vars.tex": "содержимое..."}
    let texFilesContent = {};
    files.forEach(file => {
        const tex = window.generateTex(file, fields);
        // Сохраняем имя файла (например, "Sources/variables_common_input.tex")
        texFilesContent[file] = tex; 
    });

    try {
        const response = await fetch('http://185.11.247.199:8087/api/compile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(texFilesContent)
        });

        if (!response.ok) throw new Error('Ошибка компиляции на сервере');

        // Сервер вернет готовый бинарный файл (ZIP с PDF-документами)
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = "compiled_documents.zip";
        document.body.appendChild(a);
        a.click();
        
        // Очистка
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    } catch (error) {
        console.error(error);
        alert('Не удалось скомпилировать документы: ' + error.message);
    }
};
