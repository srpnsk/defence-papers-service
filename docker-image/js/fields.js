// js/fields.js
// Генерация всех полей формы на основе параметров

// Базовые статические поля (не зависят от динамических параметров)
window.getBaseFields = function() {
    return [
        // Диссертационный совет
        {id:"DS_number", value:"", type:"string", label:"Номер совета", section:"Диссертационный совет", file:"Sources/variables_common_input.tex", inputType:"text"},
        {id:"DS_chairman_name_I", value:"", type:"string", label:"Председатель совета, Фамилия И.О., в именительном падеже", section:"Диссертационный совет", file:"Sources/variables_common_input.tex", inputType:"text"},
        {id:"DS_chairman_name_D", value:"", type:"string", label:"Председатель совета, Фамилия И.О., в дательном падеже", section:"Диссертационный совет", file:"Sources/variables_common_input.tex", inputType:"text"},
        {id:"DS_chairman_degree", value:"", type:"string", label:"Научная степень председателя совета (кратко)", section:"Диссертационный совет", file:"Sources/variables_common_input.tex", inputType:"degree_select"},
        {id:"DS_secretary_name", value:"", type:"string", label:"Секретарь совета, Фамилия И.О., в именительном падеже", section:"Диссертационный совет", file:"Sources/variables_common_input.tex", inputType:"text"},
        {id:"DS_secretary_degree", value:"", type:"string", label:"Научная степень секретаря совета", section:"Диссертационный совет", file:"Sources/variables_common_input.tex", inputType:"degree_select"},
        {id:"dsmembers", value:"", type:"counter", label:"Количество членов совета по приказу", section:"Диссертационный совет", file:"Sources/variables_common_input.tex", inputType:"number"},

        // Соискатель
        {id:"applicant_full_name_I", value:"", type:"string", label:"Имя соискателя, Фамилия Имя Отчество, в именительном падеже", section:"Соискатель", file:"Sources/variables_common_input.tex", inputType:"text"},
        {id:"applicant_short_name_I", value:"", type:"string", label:"Имя соискателя, Фамилия И.О., в именительном падеже", section:"Соискатель", file:"Sources/variables_common_input.tex", inputType:"text"},
        {id:"applicant_full_name_R", value:"", type:"string", label:"Имя соискателя, Фамилия Имя Отчество, в родительном падеже", section:"Соискатель", file:"Sources/variables_common_input.tex", inputType:"text"},
        {id:"applicant_short_name_R", value:"", type:"string", label:"Имя соискателя, Фамилия И.О., в родительном падеже", section:"Соискатель", file:"Sources/variables_common_input.tex", inputType:"text"},
        {id:"sex", value:"1", type:"counter", label:"Пол соискателя, 1 - мужской, 2 - женский", section:"Соискатель", file:"Sources/variables_common_input.tex", inputType:"sex_select"},
        {id:"end_of_postgrad_date", value:"", type:"string", label:"Дата окончания аспирантуры, \"дд\" месяц год, по приказу", section:"Соискатель", file:"Sources/variables_common_input.tex", inputType:"date"},
        {id:"applicant_phone_number", value:"", type:"string", label:"Телефонный номер соискателя", section:"Соискатель", file:"Sources/variables_common_input.tex", inputType:"tel"},
        {id:"applicant_email", value:"", type:"string", label:"e-mail соискателя", section:"Соискатель", file:"Sources/variables_common_input.tex", inputType:"email"},
        {id:"applicant_full_adress", value:"", type:"string", label:"Адрес соискателя", section:"Соискатель", file:"Sources/variables_common_input.tex", inputType:"text"},
        {id:"applicant_SNILS", value:"", type:"string", label:"СНИЛС соискателя", section:"Соискатель", file:"Sources/variables_common_input.tex", inputType:"text"},
        {id:"applicant_document", value:"паспорт", type:"string", label:"Тип документа, удостоверяющего личность (напр. паспорт)", section:"Соискатель", file:"Sources/variables_common_input.tex", inputType:"doc_select"},
        {id:"applicant_document_series", value:"", type:"string", label:"Серия документа, удостоверяющего личность", section:"Соискатель", file:"Sources/variables_common_input.tex", inputType:"text"},
        {id:"applicant_document_number", value:"", type:"string", label:"Номер документа, удостоверяющего личность", section:"Соискатель", file:"Sources/variables_common_input.tex", inputType:"text"},

        // Диссертация
        {id:"degree_R", value:"", type:"string", label:"Степень, на которую претендует соискатель, в родительном падеже", section:"Диссертация", file:"Sources/variables_common_input.tex", inputType:"degree_select"},
        {id:"thesis_title", value:"", type:"string", label:"Название диссертации", section:"Диссертация", file:"Sources/variables_common_input.tex", inputType:"text"},
        {id:"applicant_specialty_number", value:"", type:"string", label:"Номер специальности, по которой планируется защита", section:"Диссертация", file:"Sources/variables_common_input.tex", inputType:"text"},
        {id:"applicant_specialty_title", value:"", type:"string", label:"Название специальности, по которой планируется защита", section:"Диссертация", file:"Sources/variables_common_input.tex", inputType:"text"},
        {id:"defence_date", value:"", type:"string", label:"Дата защиты", section:"Диссертация", file:"Sources/variables_common_input.tex", inputType:"date"},
        {id:"defence_time", value:"", type:"string", label:"Время защиты", section:"Диссертация", file:"Sources/variables_common_input.tex", inputType:"time"},

        // Научный руководитель
        {id:"advisor_name_full", value:"", type:"string", label:"Имя научного руководителя, Фамилия Имя Отчество, в именительном падеже", section:"Научный руководитель", file:"Sources/variables_common_input.tex", inputType:"text"},
        {id:"advisor_name_short", value:"", type:"string", label:"Имя научного руководителя, Фамилия И.О., в именительном падеже", section:"Научный руководитель", file:"Sources/variables_common_input.tex", inputType:"text"},
        {id:"advisor_degree", value:"", type:"string", label:"Научная степень научного руководителя", section:"Научный руководитель", file:"Sources/variables_common_input.tex", inputType:"degree_select"},
        {id:"advisor_title", value:"", type:"string", label:"Звание научного руководителя, \"учёного звания нет\" если нет", section:"Научный руководитель", file:"Sources/variables_common_input.tex", inputType:"title_select"},
        {id:"advisor_degree_title", value:"", type:"string", label:"Научная степень и звание вместе в формате \"степень, звание\" или \"степень\" (если звания нет)", section:"Научный руководитель", file:"Sources/variables_common_input.tex", inputType:"text"},
        {id:"advisor_specialty_number", value:"", type:"string", label:"Номер специальности, по которой защищался научный руководитель", section:"Научный руководитель", file:"Sources/variables_common_input.tex", inputType:"text"},
        {id:"advisor_specialty_title", value:"", type:"string", label:"Название специальности, по которой защищался научный руководитель", section:"Научный руководитель", file:"Sources/variables_common_input.tex", inputType:"text"},
        {id:"advisor_main_job", value:"", type:"string", label:"Основная должность научного руководителя (по трудовой)", section:"Научный руководитель", file:"Sources/variables_common_input.tex", inputType:"text"},
        {id:"advisor_main_workplace_full", value:"", type:"string", label:"Основное место работы научного руководителя (по трудовой)", section:"Научный руководитель", file:"Sources/variables_common_input.tex", inputType:"text"},
        {id:"advisor_main_workplace_division", value:"", type:"string", label:"Подарзделение, в котором работает научный руководитель (напр., кафедра)", section:"Научный руководитель", file:"Sources/variables_common_input.tex", inputType:"text"},
        {id:"advisor_main_workplace_adress", value:"", type:"string", label:"Рабочий адрес научного руководителя", section:"Научный руководитель", file:"Sources/variables_common_input.tex", inputType:"text"},
        {id:"advisor_email", value:"", type:"string", label:"e-mail научного руководителя", section:"Научный руководитель", file:"Sources/variables_common_input.tex", inputType:"email"},
        {id:"advisor_phone_number", value:"", type:"string", label:"Телефон научного руководителя", section:"Научный руководитель", file:"Sources/variables_common_input.tex", inputType:"tel"}
    ];
};

// Поля одного оппонента (индекс 1..N)
window.getOpponentFields = function(idx) {
    return [
        {id:`opponent${idx}_name_short`, value:"", type:"string", label:`Имя оппонента, Фамилия И.О., в именительном падеже`, section:`Оппонент ${idx}`, file:"Sources/variables_common_input.tex", inputType:"text"},
        {id:`opponent${idx}_name_full_I`, value:"", type:"string", label:`Имя оппонента, Фамилия Имя Отчество, в именительном падеже`, section:`Оппонент ${idx}`, file:"Sources/variables_common_input.tex", inputType:"text"},
        {id:`opponent${idx}_degree`, value:"", type:"string", label:`Научная степень оппонента`, section:`Оппонент ${idx}`, file:"Sources/variables_common_input.tex", inputType:"degree_select"},
        {id:`opponent${idx}_title`, value:"", type:"string", label:`Звание оппонента, \"учёного звания нет\" если нет`, section:`Оппонент ${idx}`, file:"Sources/variables_common_input.tex", inputType:"title_select"},
        {id:`opponent${idx}_degree_title`, value:"", type:"string", label:`Научная степень и звание вместе в формате \"степень, звание\" или \"степень\" (если звания нет)`, section:`Оппонент ${idx}`, file:"Sources/variables_common_input.tex", inputType:"text"},
        {id:`opponent${idx}_specialty_number`, value:"", type:"string", label:`Номер специальности, по которой защищался оппонент`, section:`Оппонент ${idx}`, file:"Sources/variables_common_input.tex", inputType:"text"},
        {id:`opponent${idx}_specialty_title`, value:"", type:"string", label:`Название специальности, по которой защищался оппонент`, section:`Оппонент ${idx}`, file:"Sources/variables_common_input.tex", inputType:"text"},
        {id:`opponent${idx}_main_job`, value:"", type:"string", label:`Основная должность оппонента (по трудовой)`, section:`Оппонент ${idx}`, file:"Sources/variables_common_input.tex", inputType:"text"},
        {id:`opponent${idx}_main_workplace_full`, value:"", type:"string", label:`Основное место работы оппонента (по трудовой)`, section:`Оппонент ${idx}`, file:"Sources/variables_common_input.tex", inputType:"text"},
        {id:`opponent${idx}_main_workplace_division`, value:"", type:"string", label:`Подразделение, в котором работает оппонент (напр., кафедра)`, section:`Оппонент ${idx}`, file:"Sources/variables_common_input.tex", inputType:"text"},
        {id:`opponent${idx}_main_workplace_adress`, value:"", type:"string", label:`Рабочий адрес оппонента`, section:`Оппонент ${idx}`, file:"Sources/variables_common_input.tex", inputType:"text"},
        {id:`opponent${idx}_email`, value:"", type:"string", label:`e-mail оппонента`, section:`Оппонент ${idx}`, file:"Sources/variables_common_input.tex", inputType:"email"},
        {id:`opponent${idx}_phone_number`, value:"", type:"string", label:`Телефон оппонента`, section:`Оппонент ${idx}`, file:"Sources/variables_common_input.tex", inputType:"tel"}
    ];
};

// Универсальная генерация статей (для руководителя или оппонентов)
window.getArticleFields = function(prefix, count, section, labelPrefix) {
    const arr = [];
    for (let i = 1; i <= count; i++) {
        arr.push({id:`${prefix}_article_${i}`, value:"", type:"string", label:`${labelPrefix} № ${i}`, section:section, file:"Sources/variables_01_input.tex", inputType:"text"});
    }
    return arr;
};

// Главная функция: собирает полный массив полей формы в соответствии с переданными параметрами
window.buildAllFields = function(params) {
    const p = params;
    let fields = window.getBaseFields();

    // Оппоненты
    for (let i = 1; i <= p.opponentCount; i++) {
        fields = fields.concat(window.getOpponentFields(i));
    }

    // 2. Заключение организации
    fields.push({id:"applicant_department_number", value:"", type:"string", label:"Номер кафедры соискателя", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"text"});
    fields.push({id:"applicant_department_title", value:"", type:"string", label:"Название кафедры соискателя", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"text"});
    fields.push({id:"applicant_PG_study", value:"", type:"string", label:"Где учился в аспирантуре", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"text"});
    fields.push({id:"applicant_job_organisation", value:"", type:"string", label:"Место работы соискателя", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"text"});
    fields.push({id:"applicant_main_job", value:"", type:"string", label:"Должность соискателя, в родительном падеже", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"text"});
    fields.push({id:"applicant_job_department_number", value:"", type:"string", label:"Номер кафедры, где работает соискатель", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"text"});
    fields.push({id:"applicant_job_department_title", value:"", type:"string", label:"Название кафедры, где работает соискателя", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"text"});
    // Флаг совместительства
    fields.push({id:"aajob", value:p.hasAdditionalJob?"1":"0", type:"counter", label:"Флаг наличия работы по совместительству у соискателя, 0 если нет, 1 если есть", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"number"});
    if (p.hasAdditionalJob) {
        fields.push({id:"applicant_addition_job", value:"", type:"string", label:"Должность соискателя по совместительству, в родительном падеже", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"text"});
        fields.push({id:"applicant_addition_job_place", value:"", type:"string", label:"Место работы соискателя по совместительству", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"text"});
    }
    // Образование
    fields.push({id:"applicant_HE_type", value:"", type:"string", label:"Высшее образование соискателем и где получено", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"text"});
    fields.push({id:"applicant_HE_qualification", value:"", type:"string", label:"Степень соискателя по высшему образование (напр., магистр)", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"degree_select"});
    fields.push({id:"applicant_excellency", value:p.hasHonorsDiploma?"с отличием":"", type:"string", label:"Указание на диплом с отличием (ничего не пишется, если нет)", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"text"});
    fields.push({id:"applicant_HE_end_year", value:"", type:"string", label:"Год завершения соискателем высшего образования", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"number"});
    fields.push({id:"applicant_HE_direction_number", value:"", type:"string", label:"Номер специальности, по которой соискатель получил высшее образование", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"text"});
    fields.push({id:"applicant_HE_direction_title", value:"", type:"string", label:"Название специальности, по которой соискатель получил высшее образование", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"text"});
    fields.push({id:"applicant_PG_end_year", value:"", type:"string", label:"Год окончания соискателем аспирантуры", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"number"});
    fields.push({id:"applicant_PG_direction_number", value:"", type:"string", label:"Номер направления, по которому соискатель закончил аспирантуру", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"text"});
    fields.push({id:"applicant_PG_direction_title", value:"", type:"string", label:"Название направления, по которому соискатель закончил аспирантуру", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"text"});
    fields.push({id:"applicant_PG_speciality_number", value:"", type:"string", label:"Номер специальности, по которой соискатель закончил аспирантуру", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"text"});
    fields.push({id:"applicant_PG_speciality_title", value:"", type:"string", label:"Название специальности, по которой соискатель закончил аспирантуру", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"text"});
    fields.push({id:"applicant_speciality_type", value:"", type:"string", label:"Раздел наук паспорта специальности", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"text"});
    // Флаг наличия диплома аспирантуры
    fields.push({id:"aadiploma", value:p.hasPostgradDiploma?"1":"0", type:"counter", label:"Флаг диплома об окончании аспирантуры, 1 - если есть", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"number"});
    if (p.hasPostgradDiploma) {
        fields.push({id:"applicant_PG_reference_date", value:"", type:"string", label:"Дата выдачи справки об окончании соискателем аспирантуры", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"date"});
    }
    // Семинар
    fields.push({id:"seminar_departament_number", value:"", type:"string", label:"Номер кафедры, проводящей семинар", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"text"});
    fields.push({id:"seminar_departament_title", value:"", type:"string", label:"Название кафедры, проводящей семинар", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"text"});
    fields.push({id:"seminar_faculty", value:"", type:"string", label:"Название института, проводящего семинар, в родительном падеже", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"text"});
    fields.push({id:"seminar_protocol_number", value:"", type:"string", label:"Номер протокола семинара", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"text"});
    fields.push({id:"seminar_date", value:"", type:"string", label:"Дата протокола семинара", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"date"});
    fields.push({id:"zakltotal", value:"", type:"counter", label:"Присутствовало на семинаре", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"number"});
    fields.push({id:"zaklyes", value:"", type:"counter", label:"Проголосовавших \"за\"", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"number"});
    fields.push({id:"zaklno", value:"", type:"counter", label:"Проголосовавших \"против\"", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"number"});
    fields.push({id:"zaklun", value:"", type:"counter", label:"Воздержавшихся", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"number"});
    fields.push({id:"achievement", value:"", type:"string", label:"За что присуждается степень", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"text"});
    fields.push({id:"departament_head_degree", value:"", type:"string", label:"Научная степень заведующего кафедрой, на которой проходил семинар", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"degree_select"});
    fields.push({id:"departament_head_name", value:"", type:"string", label:"Фамилия И.О. заведующего кафедрой, на которой проходил семинар", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"text"});
    fields.push({id:"faculty_head_degree", value:"", type:"string", label:"Научная степень директора института, на котором проходил семинар", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"degree_select"});
    fields.push({id:"faculty_head_name", value:"", type:"string", label:"Фамилия И.О. директора института, на котором проходил семинар", section:"2 Заключение организации", file:"Sources/variables_01_input.tex", inputType:"text"});

    // Паспорт специальности
    fields.push({id:"apitem", value:"1", type:"counter", label:"Номер пункта паспорта специальности, которому соответствует работа", section:"Паспорт специальности", file:"Sources/variables_01_input.tex", inputType:"number"});
    for (let i = 1; i <= p.specialtyItemCount; i++) {
        fields.push({id:`applicant_speciality_pasport_item_text_${i}`, value:"", type:"string", label:`Содержание пункта паспорта специальности (пункт ${i})`, section:"Паспорт специальности", file:"Sources/variables_01_input.tex", inputType:"text"});
    }

    // Задачи
    fields.push({id:"atasksnumber", value:String(p.taskCount+1), type:"counter", label:"Счётчик задач (количество + 1)", section:"Задачи", file:"Sources/variables_01_input.tex", inputType:"number"});
    for (let i = 1; i <= p.taskCount; i++) {
        fields.push({id:`thesis_tasks_${i}`, value:"", type:"string", label:`Задача № ${i}`, section:"Задачи", file:"Sources/variables_01_input.tex", inputType:"text"});
    }

    // Личное участие
    fields.push({id:"thesis_participation", value:"", type:"string", label:"Личное участие соискателя в получении результатов", section:"Личное участие", file:"Sources/variables_01_input.tex", inputType:"text"});

    // Научная новизна
    fields.push({id:"anoveltynumber", value:String(p.noveltyCount+1), type:"counter", label:"Счётчик пунктов научной новизны (количество + 1)", section:"Научная новизна", file:"Sources/variables_01_input.tex", inputType:"number"});
    for (let i = 1; i <= p.noveltyCount; i++) {
        fields.push({id:`thesis_novelty_${i}`, value:"", type:"string", label:`Пункт научной новизны № ${i}`, section:"Научная новизна", file:"Sources/variables_01_input.tex", inputType:"text"});
    }

    // Практическая ценность
    fields.push({id:"avaluenumber", value:String(p.valueCount+1), type:"counter", label:"Счётчик пунктов практической ценности (количество + 1)", section:"Практическая ценность", file:"Sources/variables_01_input.tex", inputType:"number"});
    for (let i = 1; i <= p.valueCount; i++) {
        fields.push({id:`thesis_value_${i}`, value:"", type:"string", label:`Пункт практической ценности № ${i}`, section:"Практическая ценность", file:"Sources/variables_01_input.tex", inputType:"text"});
    }

    // Положения
    fields.push({id:"aprovisionnumber", value:String(p.provisionCount+1), type:"counter", label:"Счётчик положений (количество + 1)", section:"Положения, выносимые на защиту", file:"Sources/variables_01_input.tex", inputType:"number"});
    for (let i = 1; i <= p.provisionCount; i++) {
        fields.push({id:`thesis_provision_${i}`, value:"", type:"string", label:`Положение № ${i}`, section:"Положения, выносимые на защиту", file:"Sources/variables_01_input.tex", inputType:"text"});
    }

    // Оценка достоверности
    fields.push({id:"thesis_reliability", value:"", type:"string", label:"Формулировка достоверности результатов", section:"Оценка достоверности результатов", file:"Sources/variables_01_input.tex", inputType:"text"});

    // Квартильные счётчики и статьи соискателя
    fields.push({id:"aanumber", value:String(p.articlesCount), type:"counter", label:"Общее количество статей соискателя", section:"Статьи соискателя", file:"Sources/variables_01_input.tex", inputType:"number"});
    // Автоматические счётчики квартилей – для начала заполняются нулями, в интерфейсе будут вычисляться
    fields.push({id:"aaq", value:"0", type:"counter", label:"Q1", section:"Статьи соискателя", file:"Sources/variables_01_input.tex", inputType:"number"});
    fields.push({id:"aaqq", value:"0", type:"counter", label:"Q2", section:"Статьи соискателя", file:"Sources/variables_01_input.tex", inputType:"number"});
    fields.push({id:"aaqqq", value:"0", type:"counter", label:"Q3", section:"Статьи соискателя", file:"Sources/variables_01_input.tex", inputType:"number"});
    fields.push({id:"aak", value:"0", type:"counter", label:"K1", section:"Статьи соискателя", file:"Sources/variables_01_input.tex", inputType:"number"});
    fields.push({id:"aakk", value:"0", type:"counter", label:"K2", section:"Статьи соискателя", file:"Sources/variables_01_input.tex", inputType:"number"});
    fields.push({id:"aakkk", value:"0", type:"counter", label:"K3", section:"Статьи соискателя", file:"Sources/variables_01_input.tex", inputType:"number"});
    fields.push({id:"aarid", value:"0", type:"counter", label:"РИД", section:"Статьи соискателя", file:"Sources/variables_01_input.tex", inputType:"number"});
    fields.push({id:"aat", value:"0", type:"counter", label:"Тезисы", section:"Статьи соискателя", file:"Sources/variables_01_input.tex", inputType:"number"});
    fields.push({id:"acon", value:"0", type:"counter", label:"Конференции", section:"Статьи соискателя", file:"Sources/variables_01_input.tex", inputType:"number"});

    for (let i = 1; i <= p.articlesCount; i++) {
        fields.push({id:`applicant_article_${i}`, value:"", type:"string", label:`Библиографическая ссылка на статью № ${i}`, section:"Статьи соискателя", file:"Sources/variables_01_input.tex", inputType:"text"});
        fields.push({id:`applicant_article_BD_${i}`, value:"", type:"string", label:`Квартили статьи № ${i}`, section:"Статьи соискателя", file:"Sources/variables_01_input.tex", inputType:"quartile_select"});
        fields.push({id:`applicant_article_contribution_${i}`, value:"", type:"string", label:`Личный вклад автора в статью № ${i}`, section:"Статьи соискателя", file:"Sources/variables_01_input.tex", inputType:"text"});
    }

    // Конференции
    fields.push({id:"acon", value:String(p.conferencesCount), type:"counter", label:"Количество конференций", section:"Конференции соискателя", file:"Sources/variables_01_input.tex", inputType:"number"});
    for (let i = 1; i <= p.conferencesCount; i++) {
        fields.push({id:`applicant_conference_${i}`, value:"", type:"string", label:`Название конференции № ${i}`, section:"Конференции соискателя", file:"Sources/variables_01_input.tex", inputType:"text"});
        fields.push({id:`applicant_conference_city_${i}`, value:"", type:"string", label:`Город проведения конференции № ${i}`, section:"Конференции соискателя", file:"Sources/variables_01_input.tex", inputType:"text"});
        fields.push({id:`applicant_conference_year_${i}`, value:"", type:"string", label:`Год проведения конференции № ${i}`, section:"Конференции соискателя", file:"Sources/variables_01_input.tex", inputType:"number"});
        fields.push({id:`applicant_thesis_${i}`, value:"", type:"string", label:`Библиографическая ссылка на тезисы конференции № ${i}`, section:"Тезисы соискателя", file:"Sources/variables_01_input.tex", inputType:"text"});
    }

    // РИД (1-5)
    for (let i = 1; i <= 5; i++) {
        fields.push({id:`applicant_RID_${i}`, value:"", type:"string", label:`Библиографическая ссылка на РИД № ${i}`, section:"РИД", file:"Sources/variables_01_input.tex", inputType:"text"});
    }

    // Статьи научного руководителя
    fields.push({id:"aanumber_advisor", value:String(p.advisorArticlesCount), type:"counter", label:"Счётчик статей руководителя за 5 лет", section:"Руководитель: статьи", file:"Sources/variables_01_input.tex", inputType:"number"});
    fields = fields.concat(window.getArticleFields("advisor", p.advisorArticlesCount, "Руководитель: статьи", "Статья руководителя"));

    // Статьи оппонентов
    for (let i = 1; i <= p.opponentCount; i++) {
        fields.push({id:`opponent${i}_aanumber`, value:String(p.opponentArticlesCount), type:"counter", label:`Счётчик статей оппонента ${i} за 5 лет`, section:`Оппонент ${i}: статьи`, file:"Sources/variables_01_input.tex", inputType:"number"});
        fields = fields.concat(window.getArticleFields(`opponent${i}`, p.opponentArticlesCount, `Оппонент ${i}: статьи`, `Статья оппонента ${i}`));
    }

    // 18_1 Протокол о создании комиссии
    fields.push({id:"18_1_protocol_number", value:"", type:"string", label:"Номер протокола о создании комиссии", section:"18_1 Протокол комиссии", file:"Sources/variables_02_input.tex", inputType:"text"});
    fields.push({id:"18_1_protocol_date", value:"", type:"string", label:"Дата протокола о создании комиссии", section:"18_1 Протокол комиссии", file:"Sources/variables_02_input.tex", inputType:"date"});
    fields.push({id:"dsoffkom", value:p.commissionOffline, type:"counter", label:"Количество членов совета очно", section:"18_1 Протокол комиссии", file:"Sources/variables_02_input.tex", inputType:"number"});
    fields.push({id:"dsonkom", value:p.commissionOnline, type:"counter", label:"Количество членов совета онлайн", section:"18_1 Протокол комиссии", file:"Sources/variables_02_input.tex", inputType:"number"});
    const totalKom = Number(p.commissionOffline) + Number(p.commissionOnline);
    for (let i = 1; i <= totalKom; i++) {
        fields.push({id:`18_1_member${i}_name`, value:"", type:"string", label:`Член комиссии ${i} (ФИО)`, section:"18_1 Протокол комиссии", file:"Sources/variables_02_input.tex", inputType:"text"});
        fields.push({id:`18_1_member${i}_degree`, value:"", type:"string", label:`Научная степень и звание члена ${i}`, section:"18_1 Протокол комиссии", file:"Sources/variables_02_input.tex", inputType:"text"});
    }
    fields.push({id:"18_1_vote_results", value:"", type:"counter", label:"Количество голосов \"за\"", section:"18_1 Протокол комиссии", file:"Sources/variables_02_input.tex", inputType:"number"});

    // 19_2 Протокол совета о приёме к защите
    fields.push({id:"19_2_protocol_number", value:"", type:"string", label:"Номер протокола о приёме к защите", section:"19_2 Протокол защиты", file:"Sources/variables_02_input.tex", inputType:"text"});
    fields.push({id:"19_2_protocol_date", value:"", type:"string", label:"Дата протокола о приёме к защите", section:"19_2 Протокол защиты", file:"Sources/variables_02_input.tex", inputType:"date"});
    fields.push({id:"dsoffacc", value:p.defenceOffline, type:"counter", label:"Количество членов совета очно", section:"19_2 Протокол защиты", file:"Sources/variables_02_input.tex", inputType:"number"});
    fields.push({id:"dsonacc", value:p.defenceOnline, type:"counter", label:"Количество членов совета онлайн", section:"19_2 Протокол защиты", file:"Sources/variables_02_input.tex", inputType:"number"});
    const totalAcc = Number(p.defenceOffline) + Number(p.defenceOnline);
    for (let i = 1; i <= totalAcc; i++) {
        fields.push({id:`19_2_member${i}_name`, value:"", type:"string", label:`Член совета ${i} (ФИО)`, section:"19_2 Протокол защиты", file:"Sources/variables_02_input.tex", inputType:"text"});
        fields.push({id:`19_2_member${i}_degree`, value:"", type:"string", label:`Научная степень и звание члена ${i}`, section:"19_2 Протокол защиты", file:"Sources/variables_02_input.tex", inputType:"text"});
    }
    fields.push({id:"19_2_vote_results", value:"", type:"counter", label:"Количество голосов \"за\"", section:"19_2 Протокол защиты", file:"Sources/variables_02_input.tex", inputType:"number"});

    // Заключение комиссии ДС
    fields.push({id:"applicant_artciles_number_total_W", value:"", type:"string", label:"Число публикаций соискателя, прописью, дательный падеж", section:"20 Заключение комиссии ДС", file:"Sources/variables_02_input.tex", inputType:"text"});
    fields.push({id:"applicant_artciles_number_rewiewed_W", value:"", type:"string", label:"Число основных статей соискателя, по которым проводится защита, прописью, родительный падеж", section:"20 Заключение комиссии ДС", file:"Sources/variables_02_input.tex", inputType:"text"});

    // 21 Публикация на сайте МИФИ
    fields.push({id:"data_publishing_MEPhI", value:"", type:"string", label:"Дата публикации объявления о защите на сайте МИФИ", section:"21 Публикация", file:"Sources/variables_02_input.tex", inputType:"text"});
    fields.push({id:"link_screenshot_publishing_MEPhI", value:"", type:"string", label:"Ссылка на страницу опубликования диссертации", section:"21 Публикация", file:"Sources/variables_02_input.tex", inputType:"text"});
    fields.push({id:"link_text_publishing_MEPhI", value:"", type:"string", label:"Ссылка на текст диссертации", section:"21 Публикация", file:"Sources/variables_02_input.tex", inputType:"text"});

    return fields;
};
