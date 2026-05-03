from pydantic import *
from typing import *
from datetime import *

from pydantic import BaseModel, Field

class AuthRequest(BaseModel):
    email: EmailStr
    password: str

class UserInfo(BaseModel):
    user_id: int
    username: str

class UserRegisterRequest(BaseModel):
    # Данные для таблицы Person
    last_name: str = Field(..., max_length=64)
    first_name: str = Field(..., max_length=64)
    second_name: Optional[str] = Field(None, max_length=64)
    degree: Optional[str] = None
    academic_title: Optional[str] = None
    phone_number: Optional[str] = None
    specialty_id: Optional[int] = None
    
    # Данные для таблицы Users
    email: EmailStr  # Используем EmailStr (требует pip install pydantic[email])
    password: str = Field(..., min_length=6)

class ThesisFormData(BaseModel):
    # ========== Диссертационный совет ==========
    DS_number: str
    DS_chairman_name_I: str
    DS_chairman_name_D: str
    DS_chairman_degree: str
    DS_secretary_name: str
    DS_secretary_degree: str

    # ========== Соискатель ==========
    applicant_full_name_I: str
    applicant_short_name_I: str
    applicant_full_name_R: str
    applicant_short_name_R: str
    end_of_postgrad_date: str
    applicant_phone_number: str
    applicant_email: str
    applicant_full_adress: str
    applicant_SNILS: str
    applicant_document: str
    applicant_document_series: str
    applicant_document_number: str

    # ========== Диссертация ==========
    degree_R: str
    thesis_title: str
    applicant_specialty_number: str
    applicant_specialty_title: str
    defence_date: str
    defence_time: str

    # ========== Научный руководитель ==========
    advisor_name_full: str
    advisor_name_short: str
    advisor_degree: str
    advisor_title: str
    advisor_degree_title: str
    advisor_specialty_number: str
    advisor_specialty_title: str
    advisor_main_job: str
    advisor_main_workplace_full: str
    advisor_main_workplace_division: str
    advisor_main_workplace_adress: str
    advisor_email: str
    advisor_phone_number: str

    # ========== Оппонент 1 ==========
    opponent1_name_short: str
    opponent1_name_full_I: str
    opponent1_degree: str
    opponent1_title: str
    opponent1_degree_title: str
    opponent1_specialty_number: str
    opponent1_specialty_title: str
    opponent1_main_job: str
    opponent1_main_workplace_full: str
    opponent1_main_workplace_division: str
    opponent1_main_workplace_adress: str
    opponent1_email: str
    opponent1_phone_number: str

    # ========== Оппонент 2 ==========
    opponent2_name_short: str
    opponent2_name_full_I: str
    opponent2_degree: str
    opponent2_title: str
    opponent2_degree_title: str
    opponent2_specialty_number: str
    opponent2_specialty_title: str
    opponent2_main_job: str
    opponent2_main_workplace_full: str
    opponent2_main_workplace_division: str
    opponent2_main_workplace_adress: str
    opponent2_email: str
    opponent2_phone_number: str

    # ========== Оппонент 3 ==========
    opponent3_name_short: str
    opponent3_name_full_I: str
    opponent3_degree: str
    opponent3_title: str
    opponent3_degree_title: str
    opponent3_specialty_number: str
    opponent3_specialty_title: str
    opponent3_main_job: str
    opponent3_main_workplace_full: str
    opponent3_main_workplace_division: str
    opponent3_main_workplace_adress: str
    opponent3_email: str
    opponent3_phone_number: str

    # ========== 2. Заключение организации ==========
    applicant_department_number: str
    applicant_department_title: str
    applicant_PG_study: str
    applicant_job_organisation: str
    applicant_main_job: str
    applicant_job_department_number: str
    applicant_job_department_title: str
    applicant_addition_job: str
    applicant_addition_job_place: str
    applicant_HE_type: str
    applicant_HE_qualification: str
    applicant_excellency: str
    applicant_HE_end_year: int
    applicant_HE_direction_number: str
    applicant_HE_direction_title: str
    applicant_PG_end_year: int
    applicant_PG_direction_number: str
    applicant_PG_direction_title: str
    applicant_PG_speciality_number: str
    applicant_PG_speciality_title: str
    applicant_speciality_type: str
    applicant_PG_reference_date: str
    seminar_departament_number: str
    seminar_departament_title: str
    seminar_faculty: str
    seminar_protocol_number: str
    seminar_date: str
    achievement: str
    departament_head_degree: str
    departament_head_name: str
    faculty_head_degree: str
    faculty_head_name: str

    # ========== Паспорт специальности ==========
    applicant_speciality_pasport_item_text_1: str
    applicant_speciality_pasport_item_text_2: str
    applicant_speciality_pasport_item_text_3: Optional[str] = ""

    # ========== Задачи ==========
    thesis_tasks_1: str
    thesis_tasks_2: str
    thesis_tasks_3: str
    thesis_tasks_4: Optional[str] = ""
    thesis_tasks_5: Optional[str] = ""
    thesis_tasks_6: Optional[str] = ""
    thesis_tasks_7: Optional[str] = ""
    thesis_tasks_8: Optional[str] = ""

    # ========== Личное участие ==========
    thesis_participation: str

    # ========== Научная новизна ==========
    thesis_novelty_1: str
    thesis_novelty_2: str
    thesis_novelty_3: str
    thesis_novelty_4: Optional[str] = ""
    thesis_novelty_5: Optional[str] = ""
    thesis_novelty_6: Optional[str] = ""

    # ========== Практическая ценность ==========
    thesis_value_1: str
    thesis_value_2: str
    thesis_value_3: str
    thesis_value_4: Optional[str] = ""
    thesis_value_5: Optional[str] = ""
    thesis_value_6: Optional[str] = ""

    # ========== Положения, выносимые на защиту ==========
    thesis_provision_1: str
    thesis_provision_2: str
    thesis_provision_3: str
    thesis_provision_4: Optional[str] = ""
    thesis_provision_5: Optional[str] = ""
    thesis_provision_6: Optional[str] = ""

    # ========== Оценка достоверности результатов ==========
    thesis_reliability: str

    # ========== Статьи соискателя ==========
    applicant_article_1: str
    applicant_article_BD_1: str
    applicant_article_contribution_1: str
    applicant_article_2: str
    applicant_article_BD_2: str
    applicant_article_contribution_2: str
    applicant_article_3: Optional[str] = ""
    applicant_article_BD_3: Optional[str] = ""
    applicant_article_contribution_3: Optional[str] = ""
    applicant_article_4: Optional[str] = ""
    applicant_article_BD_4: Optional[str] = ""
    applicant_article_contribution_4: Optional[str] = ""
    applicant_article_5: Optional[str] = ""
    applicant_article_BD_5: Optional[str] = ""
    applicant_article_contribution_5: Optional[str] = ""
    applicant_article_6: Optional[str] = ""
    applicant_article_BD_6: Optional[str] = ""
    applicant_article_contribution_6: Optional[str] = ""
    applicant_article_7: Optional[str] = ""
    applicant_article_BD_7: Optional[str] = ""
    applicant_article_contribution_7: Optional[str] = ""
    applicant_article_8: Optional[str] = ""
    applicant_article_BD_8: Optional[str] = ""
    applicant_article_contribution_8: Optional[str] = ""
    applicant_article_9: Optional[str] = ""
    applicant_article_BD_9: Optional[str] = ""
    applicant_article_contribution_9: Optional[str] = ""
    applicant_article_10: Optional[str] = ""
    applicant_article_BD_10: Optional[str] = ""
    applicant_article_contribution_10: Optional[str] = ""
    applicant_article_11: Optional[str] = ""
    applicant_article_BD_11: Optional[str] = ""
    applicant_article_contribution_11: Optional[str] = ""
    applicant_article_12: Optional[str] = ""
    applicant_article_BD_12: Optional[str] = ""
    applicant_article_contribution_12: Optional[str] = ""
    applicant_article_13: Optional[str] = ""
    applicant_article_BD_13: Optional[str] = ""
    applicant_article_contribution_13: Optional[str] = ""
    applicant_article_14: Optional[str] = ""
    applicant_article_BD_14: Optional[str] = ""
    applicant_article_contribution_14: Optional[str] = ""
    applicant_article_15: Optional[str] = ""
    applicant_article_BD_15: Optional[str] = ""
    applicant_article_contribution_15: Optional[str] = ""
    applicant_article_16: Optional[str] = ""
    applicant_article_BD_16: Optional[str] = ""
    applicant_article_contribution_16: Optional[str] = ""

    # ========== Конференции соискателя ==========
    applicant_conference_1: str
    applicant_conference_2: str
    applicant_conference_3: Optional[str] = ""
    applicant_conference_4: Optional[str] = ""
    applicant_conference_5: Optional[str] = ""
    applicant_conference_6: Optional[str] = ""
    applicant_conference_7: Optional[str] = ""
    applicant_conference_8: Optional[str] = ""
    applicant_conference_9: Optional[str] = ""
    applicant_conference_10: Optional[str] = ""
    applicant_conference_11: Optional[str] = ""
    applicant_conference_12: Optional[str] = ""
    applicant_conference_13: Optional[str] = ""
    applicant_conference_14: Optional[str] = ""
    applicant_conference_15: Optional[str] = ""
    applicant_conference_16: Optional[str] = ""
    applicant_conference_17: Optional[str] = ""
    applicant_conference_18: Optional[str] = ""
    applicant_conference_19: Optional[str] = ""
    applicant_conference_20: Optional[str] = ""
    applicant_conference_21: Optional[str] = ""
    applicant_conference_22: Optional[str] = ""
    applicant_conference_23: Optional[str] = ""
    applicant_conference_24: Optional[str] = ""
    applicant_conference_25: Optional[str] = ""
    applicant_conference_26: Optional[str] = ""
    applicant_conference_27: Optional[str] = ""
    applicant_conference_28: Optional[str] = ""
    applicant_conference_29: Optional[str] = ""
    applicant_conference_30: Optional[str] = ""

    # ========== Опубликованные тезисы конференций ==========
    applicant_thesis_1: str
    applicant_thesis_2: str
    applicant_thesis_3: Optional[str] = ""
    applicant_thesis_4: Optional[str] = ""
    applicant_thesis_5: Optional[str] = ""
    applicant_thesis_6: Optional[str] = ""
    applicant_thesis_7: Optional[str] = ""
    applicant_thesis_8: Optional[str] = ""
    applicant_thesis_9: Optional[str] = ""
    applicant_thesis_10: Optional[str] = ""
    applicant_thesis_11: Optional[str] = ""
    applicant_thesis_12: Optional[str] = ""
    applicant_thesis_13: Optional[str] = ""
    applicant_thesis_14: Optional[str] = ""
    applicant_thesis_15: Optional[str] = ""
    applicant_thesis_16: Optional[str] = ""
    applicant_thesis_17: Optional[str] = ""
    applicant_thesis_18: Optional[str] = ""
    applicant_thesis_19: Optional[str] = ""
    applicant_thesis_20: Optional[str] = ""
    applicant_thesis_21: Optional[str] = ""
    applicant_thesis_22: Optional[str] = ""
    applicant_thesis_23: Optional[str] = ""
    applicant_thesis_24: Optional[str] = ""
    applicant_thesis_25: Optional[str] = ""
    applicant_thesis_26: Optional[str] = ""
    applicant_thesis_27: Optional[str] = ""
    applicant_thesis_28: Optional[str] = ""
    applicant_thesis_29: Optional[str] = ""
    applicant_thesis_30: Optional[str] = ""

    # ========== РИД ==========
    applicant_RID_1: Optional[str] = ""
    applicant_RID_2: Optional[str] = ""
    applicant_RID_3: Optional[str] = ""
    applicant_RID_4: Optional[str] = ""
    applicant_RID_5: Optional[str] = ""

    # ========== 3. Пояснительная записка ==========
    planed_defence_date: str

    # ========== 9. Сведения о научном руководителе ==========
    advisor_article_1: str
    advisor_article_2: str
    advisor_article_3: str
    advisor_article_4: str
    advisor_article_5: str
    advisor_article_6: str
    advisor_article_7: str
    advisor_article_8: Optional[str] = ""
    advisor_article_9: Optional[str] = ""
    advisor_article_10: Optional[str] = ""
    advisor_article_11: Optional[str] = ""
    advisor_article_12: Optional[str] = ""
    advisor_article_13: Optional[str] = ""
    advisor_article_14: Optional[str] = ""
    advisor_article_15: Optional[str] = ""

    # ========== 11_1. Согласие и данные оппонента 1 ==========
    opponent1_article_1: str
    opponent1_article_2: str
    opponent1_article_3: str
    opponent1_article_4: str
    opponent1_article_5: str
    opponent1_article_6: str
    opponent1_article_7: str
    opponent1_article_8: Optional[str] = ""
    opponent1_article_9: Optional[str] = ""
    opponent1_article_10: Optional[str] = ""
    opponent1_article_11: Optional[str] = ""
    opponent1_article_12: Optional[str] = ""
    opponent1_article_13: Optional[str] = ""
    opponent1_article_14: Optional[str] = ""
    opponent1_article_15: Optional[str] = ""

    # ========== 11_2. Согласие и данные оппонента 2 ==========
    opponent2_article_1: str
    opponent2_article_2: str
    opponent2_article_3: str
    opponent2_article_4: str
    opponent2_article_5: str
    opponent2_article_6: str
    opponent2_article_7: Optional[str] = ""
    opponent2_article_8: Optional[str] = ""
    opponent2_article_9: Optional[str] = ""
    opponent2_article_10: Optional[str] = ""
    opponent2_article_11: Optional[str] = ""
    opponent2_article_12: Optional[str] = ""
    opponent2_article_13: Optional[str] = ""
    opponent2_article_14: Optional[str] = ""
    opponent2_article_15: Optional[str] = ""

    # ========== 11_3. Согласие и данные оппонента 3 ==========
    opponent3_article_1: str
    opponent3_article_2: str
    opponent3_article_3: str
    opponent3_article_4: str
    opponent3_article_5: str
    opponent3_article_6: str
    opponent3_article_7: str
    opponent3_article_8: str
    opponent3_article_9: str
    opponent3_article_10: str
    opponent3_article_11: str
    opponent3_article_12: str
    opponent3_article_13: str
    opponent3_article_14: str
    opponent3_article_15: Optional[str] = ""

    # ========== 18_1. Протокол о создании комиссии ==========
    protocol_18_1_number: str = Field(alias="18_1_protocol_number")
    protocol_18_1_date: str = Field(alias="18_1_protocol_date")
    commission_18_1_chairman_name: str = Field(alias="18_1_commission_chairman_name")
    commission_18_1_chairman_degree_title: str = Field(alias="18_1_commission_chairman_degree_title")
    commission_18_1_member1_name: str = Field(alias="18_1_commission_member1_name")
    commission_18_1_member1_degree_title: str = Field(alias="18_1_commission_member1_degree_title")
    commission_18_1_member2_name: str = Field(alias="18_1_commission_member2_name")
    commission_18_1_member2_degree_title: str = Field(alias="18_1_commission_member2_degree_title")
    vote_results_18_1: int = Field(alias="18_1_vote_results")

    # ========== 19_2. Протокол совета о приёме к защите ==========
    protocol_19_2_number: str = Field(alias="19_2_protocol_number")
    protocol_19_2_date: str = Field(alias="19_2_protocol_date")
    commission_19_2_chairman_name: str = Field(alias="19_2_commission_chairman_name")
    commission_19_2_chairman_degree_title: str = Field(alias="19_2_commission_chairman_degree_title")
    commission_19_2_speaker_name_R: str = Field(alias="19_2_commission_speaker_name_R")
    commission_19_2_speaker_degree: str = Field(alias="19_2_commission_speaker_degree")
    vote_results_19_2: int = Field(alias="19_2_vote_results")

    # ========== 20. Заключение комиссии ДС ==========
    applicant_articles_number_total_W: str = Field(alias="applicant_artciles_number_total_W")
    applicant_articles_number_reviewed_W: str = Field(alias="applicant_artciles_number_rewiewed_W")

    # ========== 21. Скриншот опубликования на сайте МИФИ ==========
    data_publishing_MEPhI: str
    link_screenshot_publishing_MEPhI: str
    link_text_publishing_MEPhI: str

    class Config:
        populate_by_name = True
        extra = "ignore"

class PersonBase(BaseModel):
    last_name: str
    first_name: str
    second_name: Optional[str] = None
    degree: Optional[str] = None
    academic_title: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    specialty_id: Optional[int] = None

class PersonCreate(PersonBase):
    pass

class PersonUpdate(BaseModel):
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    second_name: Optional[str] = None
    degree: Optional[str] = None
    academic_title: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    specialty_id: Optional[int] = None

class PersonOut(PersonBase):
    id: int
    class Config: from_attributes = True

# ---------- Organization ----------
class OrganizationBase(BaseModel):
    full_name: str
    short_name: str
    address: str

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationUpdate(BaseModel):
    full_name: Optional[str] = None
    short_name: Optional[str] = None
    address: Optional[str] = None

class OrganizationOut(OrganizationBase):
    id: int
    class Config: from_attributes = True

# ---------- Specialty ----------
class SpecialtyBase(BaseModel):
    code: str
    name: str

class SpecialtyCreate(SpecialtyBase):
    pass

class SpecialtyUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None

class SpecialtyOut(SpecialtyBase):
    id: int
    class Config: from_attributes = True

# ---------- Dissertation Council ----------
class CouncilBase(BaseModel):
    number: str
    organization_id: int
    chairman_id: int
    secretary_id: int
    members_count_total: int

class CouncilCreate(CouncilBase):
    pass

class CouncilUpdate(BaseModel):
    number: Optional[str] = None
    organization_id: Optional[int] = None
    chairman_id: Optional[int] = None
    secretary_id: Optional[int] = None
    members_count_total: Optional[int] = None

class CouncilOut(CouncilBase):
    id: int
    class Config: from_attributes = True

# ---------- Applicant Details ----------
class ApplicantDetailsBase(BaseModel):
    snils: str
    passport_type: str
    passport_series: str
    passport_number: str
    home_address: str
    sex: int  # smallint, 1/0
    birth_date: date
    is_postgrad_completed: bool = False
    postgrad_end_date: Optional[date] = None

class ApplicantDetailsCreate(ApplicantDetailsBase):
    person_id: int

class ApplicantDetailsUpdate(BaseModel):
    snils: Optional[str] = None
    passport_type: Optional[str] = None
    passport_series: Optional[str] = None
    passport_number: Optional[str] = None
    home_address: Optional[str] = None
    sex: Optional[int] = None
    birth_date: Optional[date] = None
    is_postgrad_completed: Optional[bool] = None
    postgrad_end_date: Optional[date] = None

class ApplicantDetailsOut(ApplicantDetailsBase):
    person_id: int
    class Config: from_attributes = True

# ---------- Employment History ----------
class EmploymentBase(BaseModel):
    person_id: int
    organization_id: int
    position: Optional[str] = None
    division: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    is_additional: bool = False

class EmploymentCreate(EmploymentBase):
    pass

class EmploymentUpdate(BaseModel):
    organization_id: Optional[int] = None
    position: Optional[str] = None
    division: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_additional: Optional[bool] = None

class EmploymentOut(EmploymentBase):
    id: int
    class Config: from_attributes = True

# ---------- Education History ----------
class EducationBase(BaseModel):
    person_id: int
    edu_level: Optional[str] = None
    end_year: Optional[int] = None
    is_honors: bool = False
    qualification: Optional[str] = None
    reference_date: Optional[date] = None
    organization_id: Optional[int] = None
    specialty_id: Optional[int] = None

class EducationCreate(EducationBase):
    pass

class EducationUpdate(BaseModel):
    edu_level: Optional[str] = None
    end_year: Optional[int] = None
    is_honors: Optional[bool] = None
    qualification: Optional[str] = None
    reference_date: Optional[date] = None
    organization_id: Optional[int] = None
    specialty_id: Optional[int] = None

class EducationOut(EducationBase):
    id: int
    class Config: from_attributes = True

# ---------- Achievement ----------
class AchievementBase(BaseModel):
    person_id: int
    type: int  # 1 - статья, 2 - РИД, 3 - конференция/тезисы
    text_content: str
    year: int
    city_id: Optional[int] = None
    quartile: Optional[str] = None

class AchievementCreate(AchievementBase):
    pass

class AchievementUpdate(BaseModel):
    type: Optional[int] = None
    text_content: Optional[str] = None
    year: Optional[int] = None
    city_id: Optional[int] = None
    quartile: Optional[str] = None

class AchievementOut(AchievementBase):
    id: int
    class Config: from_attributes = True

# ---------- Thesis Official Opponent ----------
class OpponentBase(BaseModel):
    thesis_id: int
    person_id: int
    order_index: int = 1

class OpponentCreate(OpponentBase):
    pass

class OpponentOut(OpponentBase):
    id: int
    class Config: from_attributes = True

# ---------- Thesis Participation (роли) ----------
class ParticipationBase(BaseModel):
    thesis_id: int
    person_id: int
    role: str  # 'author', 'supervisor', 'commission_chairman_18_1', etc.
    order_index: int = 1

class ParticipationCreate(ParticipationBase):
    pass

class ParticipationOut(ParticipationBase):
    id: int
    class Config: from_attributes = True

# ---------- DS Event ----------
class DsEventBase(BaseModel):
    thesis_id: int
    event_type: str
    protocol_number: str
    protocol_date: date
    votes_total: Optional[int] = None
    votes_yes: Optional[int] = None
    votes_no: Optional[int] = None
    votes_abstain: Optional[int] = None
    present_offline: int = 0
    present_online: int = 0

class DsEventCreate(DsEventBase):
    pass

class DsEventUpdate(BaseModel):
    event_type: Optional[str] = None
    protocol_number: Optional[str] = None
    protocol_date: Optional[date] = None
    votes_total: Optional[int] = None
    votes_yes: Optional[int] = None
    votes_no: Optional[int] = None
    votes_abstain: Optional[int] = None
    present_offline: Optional[int] = None
    present_online: Optional[int] = None

class DsEventOut(DsEventBase):
    id: int
    class Config: from_attributes = True

# ---------- Thesis (основная) ----------
class ThesisBase(BaseModel):
    applicant_id: int
    council_id: int
    title: str
    science_branch: str
    target_degree: str
    planned_defence_date: Optional[date] = None
    defence_date_time: Optional[datetime] = None
    website_publish_date: Optional[date] = None
    website_link: Optional[str] = None
    dissertation_text_link: Optional[str] = None
    achievement_summary: Optional[str] = None
    reliability_text: Optional[str] = None
    personal_participation: Optional[str] = None
    specialty_id: int

class ThesisCreate(ThesisBase):
    pass

class ThesisUpdate(BaseModel):
    applicant_id: Optional[int] = None
    council_id: Optional[int] = None
    title: Optional[str] = None
    science_branch: Optional[str] = None
    target_degree: Optional[str] = None
    planned_defence_date: Optional[date] = None
    defence_date_time: Optional[datetime] = None
    website_publish_date: Optional[date] = None
    website_link: Optional[str] = None
    dissertation_text_link: Optional[str] = None
    achievement_summary: Optional[str] = None
    reliability_text: Optional[str] = None
    personal_participation: Optional[str] = None
    specialty_id: Optional[int] = None

class ThesisOut(ThesisBase):
    id: int
    class Config: from_attributes = True
