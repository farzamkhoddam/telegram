from datetime import datetime
from enum import Enum
from dateutil.relativedelta import relativedelta


class AllowedKeys(Enum):
    state = ("state",)
    full_name = "full_name"
    birth_date = "birth_date"
    marital_status = "marital_status"
    field_of_study = "field_of_study"
    is_partner_competent_english_speaker = ("is_partner_competent_english_speaker",)
    does_partner_have_assessment = ("does_partner_have_assessment",)
    english_skill = "english_skill"
    work_experience_overseas = "work_experience_overseas"
    australian_work_experience = "australian_work_experience"
    uni_section = "uni_section"
    degree = "degree"
    australian_educational_qualification = "australian_educational_qualification"
    designated_regional_area_study = "designated_regional_area_study"
    specialist_educational_qualification = "specialist_educational_qualification"
    professional_year_in_australia = "professional_year_in_australia"
    accredited_community_language = "accredited_community_language"


class ClientMarital(Enum):
    Single = "single"
    Married = "married"


class IELTSScore(Enum):
    Six = "6"
    Seven = "7"
    Eight = "8"


class WorkExperience(Enum):
    BelowOneYear = "below_1_year"
    OneToThreeYears = "1_to_3_years"
    ThreeToFiveYears = "3_to_5_years"
    FiveToEightYears = "5_to_8_years"
    MoreThan8Years = "more_than_8_years"


class AustralianWorkExperience(Enum):
    BelowOneYear = "below_1_year"
    OneToThreeYears = "1_to_3_years"
    ThreeToFiveYears = "3_to_5_years"
    FiveToEightYears = "5_to_8_years"
    MoreThan8Years = "more_than_8_years"


class ClientDegree(Enum):
    Diploma = "diploma"
    Bachelorsdegree = "bachelor"
    Mastersdegree = "master"
    Doctorate = "doctorate"


# class UniSections(Enum):
#     Section1 = "section_1"
#     Section2 = "Section_2"


class UniSections(Enum):
    Section1 = "section_1"
    Section2 = "section_2"
    IDontKnow = "i_dont_know"


class BooleanAnswer(Enum):
    Yes = "yes"
    No = "no"


def calculate_age(birthday):
    today = datetime.today()
    age = relativedelta(today, birthday).years
    return age


def calculate_client_score(user_data):
    final_score = 0
    has_empty_field = False

    # /////////// age//////////////
    birthday = user_data.get(AllowedKeys.birth_date.value) or datetime.now()
    client_age = calculate_age(birthday)
    if 18 <= client_age < 25:
        final_score += 25
    elif 25 <= client_age < 33:
        final_score += 30
    elif 33 <= client_age < 40:
        final_score += 25
    elif 40 <= client_age < 45:
        final_score += 15
    # ///////////// marital ////////////////////////
    if user_data.get(AllowedKeys.marital_status.value) == ClientMarital.Single:
        final_score += 10
    elif (
        user_data.get(AllowedKeys.is_partner_competent_english_speaker.value)
        == BooleanAnswer.Yes.value
    ):
        final_score += 5
    if (
        user_data.get(AllowedKeys.does_partner_have_assessment.value)
        == BooleanAnswer.Yes.value
    ):
        final_score += 5

    # /////////// English Language ///////////////////////
    if user_data.get(AllowedKeys.english_skill.value) == IELTSScore.Seven.value:
        final_score += 10
    elif user_data.get(AllowedKeys.english_skill.value) == IELTSScore.Eight.value:
        final_score += 20

    # ///////////  Overseas Work Experience /////////////////
    if (
        user_data.get(AllowedKeys.work_experience_overseas.value)
        == WorkExperience.ThreeToFiveYears.value
    ):
        final_score += 5
    elif (
        user_data.get(AllowedKeys.work_experience_overseas.value)
        == WorkExperience.FiveToEightYears.value
    ):
        final_score += 10
    elif (
        user_data.get(AllowedKeys.work_experience_overseas.value)
        == WorkExperience.MoreThan8Years.value
    ):
        final_score += 15

    # ///////////  Australian Work Experience /////////////////
    if (
        user_data.get(AllowedKeys.australian_work_experience.value)
        == AustralianWorkExperience.OneToThreeYears.value
    ):
        final_score += 5
    elif (
        user_data.get(AllowedKeys.australian_work_experience.value)
        == AustralianWorkExperience.ThreeToFiveYears.value
    ):
        final_score += 10
    elif (
        user_data.get(AllowedKeys.australian_work_experience.value)
        == AustralianWorkExperience.FiveToEightYears.value
    ):
        final_score += 15
    elif (
        user_data.get(AllowedKeys.australian_work_experience.value)
        == AustralianWorkExperience.MoreThan8Years.value
    ):
        final_score += 20

    # /////////// degree /////////////////
    if user_data.get(AllowedKeys.uni_section.value) in (
        UniSections.Section1.value,
        UniSections.IDontKnow.value,
    ):
        if user_data.get("degree") == ClientDegree.Diploma.value:
            final_score += 10
        elif user_data.get("degree") == ClientDegree.Bachelorsdegree.value:
            final_score += 15
        elif user_data.get("degree") == ClientDegree.Mastersdegree.value:
            final_score += 15
        elif user_data.get("degree") == ClientDegree.Doctorate.value:
            final_score += 20
    elif user_data.get(AllowedKeys.uni_section.value) == UniSections.Section2:
        if user_data.get("degree") == ClientDegree.Diploma.value:
            final_score += 10
        elif user_data.get("degree") == ClientDegree.Bachelorsdegree.value:
            final_score += 10
        elif user_data.get("degree") == ClientDegree.Mastersdegree.value:
            final_score += 15
        elif user_data.get("degree") == ClientDegree.Doctorate.value:
            final_score += 15

    if user_data.get(AllowedKeys.australian_educational_qualification.value) == BooleanAnswer.Yes.value:
        # /////////// australian_educational_qualification /////////////////
        final_score += 5
    # /////////// designated_regional_area_study /////////////////
    if (
        user_data.get(AllowedKeys.designated_regional_area_study.value)
        == BooleanAnswer.Yes.value
    ):
        final_score += 5
    # /////////// specialist_educational_qualification /////////////////
    if (
        user_data.get(AllowedKeys.specialist_educational_qualification.value)
        == BooleanAnswer.Yes.value
    ):
        final_score += 10
    # /////////// professional_year_in_australia /////////////////
    if (
        user_data.get(AllowedKeys.professional_year_in_australia.value)
        == BooleanAnswer.Yes.value
    ):
        final_score += 5
    # /////////// accredited_community_language /////////////////
    if (
        user_data.get(AllowedKeys.accredited_community_language.value)
        == BooleanAnswer.Yes.value
    ):
        final_score += 5

    return final_score
