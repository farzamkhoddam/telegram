from datetime import datetime
from dateutil.relativedelta import relativedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from typing import Final
from json import dumps
import os
from dotenv import load_dotenv
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
    ApplicationBuilder,
    CallbackQueryHandler,
    InvalidCallbackData,
)
from sheet import append_values
from calculator import (
    ClientMarital,
    IELTSScore,
    WorkExperience,
    AustralianWorkExperience,
    ClientDegree,
    UniSections,
    BooleanAnswer,
    AllowedKeys,
    calculate_client_score,
)

load_dotenv()  # This loads the variables from .env

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")
(
    BIRTH_DATE,
    MARITAL_STATUS,
    MARITAL_PATH,
    FIELD_OF_STUDY,
    DOES_PARTNER_HAVE_ASSESSMENT,
    UNI_SECTION,
    DEGREE,
    AUSTRALIAN_EDUCATION_QUALIFICATION_RELATED,
    AUSTRALIAN_EDUCATION_PATH,
    DESIGNATED_REGIONAL_AREA_STUDY,
    SPECIALIST_EDUCATIONAL_QUALIFICATION,
    ACCREDITED_COMMUNITY_LANGUAGE,
    WORK_EXPERIENCE_OVERSEAS,
    AUSTRALIAN_WORK_EXPERIENCE,
    ENGLISH_SKILL,
    PROFESSIONAL_YEAR_IN_AUSTRALIA,
    FINAL_STEP,
) = range(17)


############## Commands ##############
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Welcome! Use /survey to start the survey.",
    )


async def survey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="نام و نام خانوادگی:"
    )

    return BIRTH_DATE


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Survey cancelled."
    )
    return ConversationHandler.END


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"update {update} caused the following error {context.error}")


##############


############## Survey Questions ##############
async def birth_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # if "invalid_birthdate" in context.user_data:
    #     # del context.user_data["invalid_birthdate"]
    #     context.user_data[AllowedKeys.birth_date] = update.message.text
    #     return MARITAL_STATUS
    # context.user_data[AllowedKeys.full_name] = update.message.text
    context.user_data[AllowedKeys.full_name.value] = update.message.text
    context.user_data[AllowedKeys.state.value] = AllowedKeys.birth_date.value
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="تاریخ تولد میلادی:(2006-06-18)"
    )
    return MARITAL_STATUS


async def birth_date_retry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="تاریخ تولد میلادی:(2006-06-18)"
    )
    return MARITAL_STATUS


async def marital_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Parse the string using the specified format
        date_object = datetime.strptime(update.message.text, "%Y-%m-%d").date()
        today = datetime.today()
        age = relativedelta(today, date_object).years
        context.user_data[AllowedKeys.birth_date.value] = date_object
        context.user_data[AllowedKeys.state.value] = AllowedKeys.marital_status.value
        # context.user_data["birth_date"] = update.message.text
        keyboard = [
            [
                InlineKeyboardButton("مجرد", callback_data=ClientMarital.Single.value),
                InlineKeyboardButton(
                    "متاهل", callback_data=ClientMarital.Married.value
                ),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="وضعیت تاهل:",
            reply_markup=reply_markup,
        )
        return MARITAL_PATH
    except ValueError:
        keyboard = [
            [
                InlineKeyboardButton("تلاش مجدد", callback_data="retry"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="تاریخ تولد غلط است",
            reply_markup=reply_markup,
        )
        return BIRTH_DATE


async def is_partner_competent_english_speaker(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    try:
        await query.answer()
    except InvalidCallbackData:
        await query.answer("This button is no longer valid.")
        await query.edit_message_text("This poll has been closed or deleted.")
    context.user_data[AllowedKeys.marital_status.value] = query.data
    context.user_data[AllowedKeys.state.value] = (
        AllowedKeys.is_partner_competent_english_speaker.value
    )
    keyboard = [
        [
            InlineKeyboardButton(
                "بله",
                callback_data=BooleanAnswer.Yes.value,
            ),
            InlineKeyboardButton(
                "خیر",
                callback_data=BooleanAnswer.No.value,
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="آیا همسر شما می تواند حداقل آیلتس 6 یا معادل آن را دریافت کند؟",
        reply_markup=reply_markup,
    )
    return DOES_PARTNER_HAVE_ASSESSMENT


async def does_partner_have_assessment(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    try:
        await query.answer()
    except InvalidCallbackData:
        await query.answer("This button is no longer valid.")
        await query.edit_message_text("This poll has been closed or deleted.")
    context.user_data[AllowedKeys.is_partner_competent_english_speaker.value] = (
        query.data
    )
    context.user_data[AllowedKeys.state.value] = (
        AllowedKeys.does_partner_have_assessment.value
    )
    keyboard = [
        [
            InlineKeyboardButton(
                "بله",
                callback_data=BooleanAnswer.Yes.value,
            ),
            InlineKeyboardButton(
                "خیر",
                callback_data=BooleanAnswer.No.value,
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="آیا همسر شما اسسمنت مدارک دارد؟",
        reply_markup=reply_markup,
    )
    return FIELD_OF_STUDY


async def field_of_study(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()
    state = context.user_data.get(AllowedKeys.state.value, None)
    if state == AllowedKeys.marital_status.value:
        context.user_data[AllowedKeys.marital_status.value] = query.data
        # context.user_data[AllowedKeys.is_partner_competent_english_speaker.value] = BooleanAnswer.No.value
        # context.user_data[AllowedKeys.does_partner_have_assessment.value] = (
        #     BooleanAnswer.No.value
        # )
    elif state == AllowedKeys.does_partner_have_assessment.value:
        context.user_data[AllowedKeys.does_partner_have_assessment.value] = query.data
    context.user_data[AllowedKeys.state.value] = AllowedKeys.field_of_study.value

    # context.user_data["marital_status"] = query.data
    # await query.edit_message_text(f"you chose {query.data}")
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="رشته تحصیلی:"
    )
    return UNI_SECTION


async def uni_section(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[AllowedKeys.field_of_study.value] = update.message.text
    context.user_data[AllowedKeys.state.value] = AllowedKeys.uni_section.value
    # context.user_data["field_of_study"] = update.message.text
    keyboard = [
        [
            InlineKeyboardButton("سکشن 1", callback_data=UniSections.Section1.value),
            InlineKeyboardButton("سکشن 2", callback_data=UniSections.Section2.value),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="سکشن دانشگاه:",
        reply_markup=reply_markup,
    )
    return DEGREE


async def degree(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data[AllowedKeys.uni_section.value] = query.data
    context.user_data[AllowedKeys.state.value] = AllowedKeys.degree.value
    # await query.edit_message_text(f"You chose {query.data}")
    keyboard = [
        [
            InlineKeyboardButton("دیپلم", callback_data=ClientDegree.Diploma.value),
            InlineKeyboardButton(
                "لیسانس", callback_data=ClientDegree.Bachelorsdegree.value
            ),
            InlineKeyboardButton(
                "فوق لیسانس", callback_data=ClientDegree.Mastersdegree.value
            ),
            InlineKeyboardButton("دکترا", callback_data=ClientDegree.Doctorate.value),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="آخرین مدرک تحصیلی و دانشگاهی:",
        reply_markup=reply_markup,
    )
    return AUSTRALIAN_EDUCATION_QUALIFICATION_RELATED


async def australian_education_qualification_related(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()
    context.user_data[AllowedKeys.degree.value] = query.data
    context.user_data[AllowedKeys.state.value] = (
        AllowedKeys.australian_educational_qualification.value
    )
    # await query.edit_message_text(f"You chose {query.data}")
    keyboard = [
        [
            InlineKeyboardButton(
                "بله",
                callback_data=BooleanAnswer.Yes.value,
            ),
            InlineKeyboardButton(
                "خیر",
                callback_data=BooleanAnswer.No.value,
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="آیا دو سال یا بیشتر بصورت تمام وقت در استرالیا تحصیل کرده اید؟",
        reply_markup=reply_markup,
    )
    return AUSTRALIAN_EDUCATION_PATH


async def designated_regional_area_study(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()
    context.user_data[AllowedKeys.australian_educational_qualification.value] = (
        query.data
    )
    context.user_data[AllowedKeys.state.value] = (
        AllowedKeys.designated_regional_area_study.value
    )
    keyboard = [
        [
            InlineKeyboardButton(
                "بله",
                callback_data=BooleanAnswer.Yes.value,
            ),
            InlineKeyboardButton(
                "خیر",
                callback_data=BooleanAnswer.No.value,
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="آیا در مناطق کم جمعیت استرالیا به مدت حداقل دو سال تحصیل کرده اید؟",
        reply_markup=reply_markup,
    )
    return SPECIALIST_EDUCATIONAL_QUALIFICATION


async def specialist_educational_qualification(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()
    context.user_data[AllowedKeys.designated_regional_area_study.value] = query.data
    context.user_data[AllowedKeys.state.value] = (
        AllowedKeys.specialist_educational_qualification.value
    )
    # await query.edit_message_text(f"You chose {query.data}")
    keyboard = [
        [
            InlineKeyboardButton(
                "بله",
                callback_data=BooleanAnswer.Yes.value,
            ),
            InlineKeyboardButton(
                "خیر",
                callback_data=BooleanAnswer.No.value,
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="آیا دو سال در رشته های خاص تخصصی در پایه های فوق لیسانس (تحقیقی) و یا دکترا تحصیل کرده اید؟",
        reply_markup=reply_markup,
    )
    return ACCREDITED_COMMUNITY_LANGUAGE


async def accredited_community_language(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()
    state = context.user_data.get(AllowedKeys.state.value, None)
    if state == AllowedKeys.australian_educational_qualification.value:
        context.user_data[AllowedKeys.australian_educational_qualification.value] = (
            query.data
        )
        # context.user_data[AllowedKeys.designated_regional_area_study.value] = BooleanAnswer.No.value
        # context.user_data[AllowedKeys.specialist_educational_qualification.value] = (
        #     BooleanAnswer.No.value
        # )

    elif state == AllowedKeys.specialist_educational_qualification.value:
        context.user_data[AllowedKeys.specialist_educational_qualification.value] = (
            query.data
        )
    context.user_data[AllowedKeys.state.value] = (
        AllowedKeys.accredited_community_language.value
    )
    keyboard = [
        [
            InlineKeyboardButton(
                "بله",
                callback_data=BooleanAnswer.Yes.value,
            ),
            InlineKeyboardButton(
                "خیر",
                callback_data=BooleanAnswer.No.value,
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="آیا گواهینامه زبان ناتی دارید؟",
        reply_markup=reply_markup,
    )
    return WORK_EXPERIENCE_OVERSEAS


async def work_experience_overseas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data[AllowedKeys.accredited_community_language.value] = query.data
    context.user_data[AllowedKeys.state.value] = (
        AllowedKeys.work_experience_overseas.value
    )
    # await query.edit_message_text(f"You chose {query.data}")
    keyboard = [
        [
            InlineKeyboardButton(
                "زیر یک سال",
                callback_data=WorkExperience.BelowOneYear.value,
            ),
            InlineKeyboardButton(
                "یک تا سه سال",
                callback_data=WorkExperience.OneToThreeYears.value,
            ),
            InlineKeyboardButton(
                "سه تا پنج سال",
                callback_data=WorkExperience.ThreeToFiveYears.value,
            ),
            InlineKeyboardButton(
                "پنج تا هشت سال",
                callback_data=WorkExperience.FiveToEightYears.value,
            ),
            InlineKeyboardButton(
                "بیشتر از هشت سال",
                callback_data=WorkExperience.MoreThan8Years.value,
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="چند سال خارج از استرالیا سابقه کار دارید؟",
        reply_markup=reply_markup,
    )
    return AUSTRALIAN_WORK_EXPERIENCE


async def australian_work_experience(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()
    context.user_data[AllowedKeys.work_experience_overseas.value] = query.data
    context.user_data[AllowedKeys.state.value] = (
        AllowedKeys.australian_work_experience.value
    )
    # await query.edit_message_text(f"You chose {query.data}")
    keyboard = [
        [
            InlineKeyboardButton(
                "زیر یک سال",
                callback_data=AustralianWorkExperience.BelowOneYear.value,
            ),
            InlineKeyboardButton(
                "یک تا سه سال",
                callback_data=AustralianWorkExperience.OneToThreeYears.value,
            ),
            InlineKeyboardButton(
                "سه تا پنج سال",
                callback_data=AustralianWorkExperience.ThreeToFiveYears.value,
            ),
            InlineKeyboardButton(
                "پنج تا هشت سال",
                callback_data=AustralianWorkExperience.FiveToEightYears.value,
            ),
            InlineKeyboardButton(
                "بیشتر از هشت سال",
                callback_data=AustralianWorkExperience.MoreThan8Years.value,
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="چند سال داخل استرالیا سابقه کار دارید؟",
        reply_markup=reply_markup,
    )
    return ENGLISH_SKILL


async def english_skill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data[AllowedKeys.australian_work_experience.value] = query.data
    context.user_data[AllowedKeys.state.value] = AllowedKeys.english_skill.value
    # await query.edit_message_text(f"You chose {query.data}")
    keyboard = [
        [
            InlineKeyboardButton(
                "6",
                callback_data=IELTSScore.Six.value,
            ),
            InlineKeyboardButton(
                "7",
                callback_data=IELTSScore.Seven.value,
            ),
            InlineKeyboardButton(
                "8",
                callback_data=IELTSScore.Eight.value,
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="نمره آزمون ایلتس یا معادل آن در سازمان های مشابه:",
        reply_markup=reply_markup,
    )
    return PROFESSIONAL_YEAR_IN_AUSTRALIA


async def professional_year_in_australia(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()
    context.user_data[AllowedKeys.english_skill.value] = query.data
    context.user_data[AllowedKeys.state.value] = (
        AllowedKeys.professional_year_in_australia.value
    )
    # await query.edit_message_text(f"You chose {query.data}")
    keyboard = [
        [
            InlineKeyboardButton(
                "بله",
                callback_data=BooleanAnswer.Yes.value,
            ),
            InlineKeyboardButton(
                "خیر",
                callback_data=BooleanAnswer.No.value,
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="آیا یکسال یا بیشتر در استرالیا سابقه کار حرفه ای در رشته های مرتبط داشته اید؟",
        reply_markup=reply_markup,
    )
    return FINAL_STEP


async def final_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data[AllowedKeys.professional_year_in_australia.value] = query.data
    final_score = calculate_client_score(context.user_data)
    # await query.edit_message_text(f"You chose {query.data}")
    response = (
        f"نام و نام خانوادگی: {context.user_data[AllowedKeys.full_name.value]}\n"
        + f"تاریخ تولد: {context.user_data[AllowedKeys.birth_date.value]}\n"
        + f"وضعیت تاهل: {context.user_data[AllowedKeys.marital_status.value]}\n"
        + f"همسر شما می تواند حداقل آیلتس 6 یا معادل آن را دریافت کند: {context.user_data.get(AllowedKeys.is_partner_competent_english_speaker.value,BooleanAnswer.No.value)}\n"
        + f"همسر شما اسسمنت مدارک دارد: {context.user_data.get(AllowedKeys.does_partner_have_assessment.value,BooleanAnswer.No.value)}\n"
        + f"رشته تحصیلی: {context.user_data[AllowedKeys.field_of_study.value]}\n"
        + f"سکشن دانشگاه: {context.user_data[AllowedKeys.uni_section.value]}\n"
        + f"آخرین مدرک تحصیلی و دانشگاهی: {context.user_data[AllowedKeys.degree.value]}\n"
        + f"آیا دو سال یا بیشتر بصورت تمام وقت در استرالیا تحصیل کرده اید: {context.user_data[AllowedKeys.australian_educational_qualification.value]}\n"
        + f"در مناطق کم جمعیت استرالیا به مدت حداقل دو سال تحصیل کرده اید: {context.user_data.get(AllowedKeys.designated_regional_area_study.value,BooleanAnswer.No.value)}\n"
        + f"دو سال در رشته های خاص تخصصی در پایه های فوق لیسانس (تحقیقی) و یا دکترا تحصیل کرده اید: {context.user_data.get(AllowedKeys.specialist_educational_qualification.value,BooleanAnswer.No.value)}\n"
        + f"آیا گواهینامه زبان ناتی دارید:{context.user_data[AllowedKeys.accredited_community_language.value]}\n"
        + f"چند سال خارج از استرالیا سابقه کار دارید:{context.user_data[AllowedKeys.work_experience_overseas.value]}\n"
        + f"چند سال داخل استرالیا سابقه کار دارید: {context.user_data[AllowedKeys.australian_work_experience.value]}\n"
        + f"نمره آزمون ایلتس یا معادل آن در سازمان های مشابه: {context.user_data[AllowedKeys.english_skill.value]}\n"
        + f"آیا یکسال یا بیشتر در استرالیا سابقه کار حرفه ای در رشته های مرتبط داشته اید: {context.user_data[AllowedKeys.professional_year_in_australia.value]}\n"
        + f"نمره نهایی = {final_score}"
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"ممنون که فرم را پر کردید!\nجواب های شما:\n{response}",
    )
    values = [
        [
            update._effective_user.id,
            context.user_data.get(AllowedKeys.full_name.value),
            dumps(context.user_data.get(AllowedKeys.birth_date.value), default=str),
            context.user_data.get(AllowedKeys.marital_status.value),
            context.user_data.get(
                AllowedKeys.is_partner_competent_english_speaker.value,
                BooleanAnswer.No.value,
            ),
            context.user_data.get(
                AllowedKeys.does_partner_have_assessment.value, BooleanAnswer.No.value
            ),
            context.user_data.get(AllowedKeys.field_of_study.value),
            context.user_data.get(AllowedKeys.uni_section.value),
            context.user_data.get(AllowedKeys.degree.value),
            context.user_data.get(
                AllowedKeys.australian_educational_qualification.value
            ),
            context.user_data.get(
                AllowedKeys.designated_regional_area_study.value, BooleanAnswer.No.value
            ),
            context.user_data.get(
                AllowedKeys.specialist_educational_qualification.value,
                BooleanAnswer.No.value,
            ),
            context.user_data.get(AllowedKeys.accredited_community_language.value),
            context.user_data.get(AllowedKeys.work_experience_overseas.value),
            context.user_data.get(AllowedKeys.australian_work_experience.value),
            context.user_data.get(AllowedKeys.english_skill.value),
            context.user_data.get(AllowedKeys.professional_year_in_australia.value),
            final_score
        ]
    ]
    append_values(values)
    return ConversationHandler.END


##############


############## Response handler ##############
async def handle_responses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"In order to know your immigration score, run /survey and take the test",
    )


##############


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("survey", survey)],
        states={
            BIRTH_DATE: [
                CallbackQueryHandler(
                    birth_date_retry, pattern="^" + "retry|retryy" + "$"
                ),
                MessageHandler(filters.TEXT, birth_date),
            ],
            MARITAL_STATUS: [MessageHandler(filters.TEXT, marital_status)],
            MARITAL_PATH: [
                CallbackQueryHandler(
                    field_of_study,
                    pattern="^" + f"{ClientMarital.Single.value}" + "$",
                ),
                CallbackQueryHandler(
                    is_partner_competent_english_speaker,
                    pattern="^" + f"{ClientMarital.Married.value}" + "$",
                ),
            ],
            DOES_PARTNER_HAVE_ASSESSMENT: [
                CallbackQueryHandler(
                    does_partner_have_assessment,
                    pattern="^"
                    + "|".join(member.value for member in BooleanAnswer)
                    + "$",
                )
            ],
            FIELD_OF_STUDY: [
                CallbackQueryHandler(
                    field_of_study,
                    pattern="^"
                    + "|".join(member.value for member in BooleanAnswer)
                    + "$",
                ),
            ],
            UNI_SECTION: [MessageHandler(filters.TEXT, uni_section)],
            DEGREE: [
                CallbackQueryHandler(
                    degree,
                    pattern="^"
                    + "|".join(member.value for member in UniSections)
                    + "$",
                )
            ],
            AUSTRALIAN_EDUCATION_QUALIFICATION_RELATED: [
                CallbackQueryHandler(
                    australian_education_qualification_related,
                    pattern="^"
                    + "|".join(member.value for member in ClientDegree)
                    + "$",
                )
            ],
            AUSTRALIAN_EDUCATION_PATH: [
                CallbackQueryHandler(
                    accredited_community_language,
                    pattern="^" + f"{BooleanAnswer.No.value}" + "$",
                ),
                CallbackQueryHandler(
                    designated_regional_area_study,
                    pattern="^" + f"{BooleanAnswer.Yes.value}" + "$",
                ),
            ],
            SPECIALIST_EDUCATIONAL_QUALIFICATION: [
                CallbackQueryHandler(
                    specialist_educational_qualification,
                    pattern="^"
                    + "|".join(member.value for member in BooleanAnswer)
                    + "$",
                ),
            ],
            ACCREDITED_COMMUNITY_LANGUAGE: [
                CallbackQueryHandler(
                    accredited_community_language,
                    pattern="^"
                    + "|".join(member.value for member in BooleanAnswer)
                    + "$",
                )
            ],
            WORK_EXPERIENCE_OVERSEAS: [
                CallbackQueryHandler(
                    work_experience_overseas,
                    pattern="^"
                    + "|".join(member.value for member in BooleanAnswer)
                    + "$",
                )
            ],
            AUSTRALIAN_WORK_EXPERIENCE: [
                CallbackQueryHandler(
                    australian_work_experience,
                    pattern="^"
                    + "|".join(member.value for member in WorkExperience)
                    + "$",
                )
            ],
            ENGLISH_SKILL: [
                CallbackQueryHandler(
                    english_skill,
                    pattern="^"
                    + "|".join(member.value for member in AustralianWorkExperience)
                    + "$",
                )
            ],
            PROFESSIONAL_YEAR_IN_AUSTRALIA: [
                CallbackQueryHandler(
                    professional_year_in_australia,
                    pattern="^" + "|".join(member.value for member in IELTSScore) + "$",
                )
            ],
            FINAL_STEP: [
                CallbackQueryHandler(
                    final_step,
                    pattern="^"
                    + "|".join(member.value for member in BooleanAnswer)
                    + "$",
                )
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_error_handler(error)
    app.add_handler(conv_handler)
    # app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_responses))
    app.run_polling()


if __name__ == "__main__":
    main()
