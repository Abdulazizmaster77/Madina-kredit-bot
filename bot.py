from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from flask import Flask
import threading
import os


TOKEN = "8741313549:AAHTbKDD71LXE5PBTRL5NjvnfXAGVucKiJ8"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        ["💳 Kredit olish"],
        ["🧮 Kredit hisoblash"],
        ["☎️ Aloqa operatori"]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    ism = update.effective_user.first_name

    await update.message.reply_text(
        f"Botga xush kelibsiz, {ism}! 👋",
        reply_markup=reply_markup
    )


# KREDIT OLISH
async def kredit(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👤 Ismingizni kiriting:"
    )

    context.user_data["holat"] = "ism"


# KREDIT HISOBLASH
async def hisoblash(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "💰 Kredit summasini kiriting:\n\nMisol: 22.000.000"
    )

    context.user_data["holat"] = "hisob_summa"


# OPERATOR
async def operator(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        """
☎️ Aloqa operatori:

Admin:
@Madina_kredit_hizmati
"""
    )


# ASOSIY XABARLAR
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    # Tugmalar

    if text == "💳 Kredit olish":
        await kredit(update, context)
        return


    if text == "🧮 Kredit hisoblash":
        await hisoblash(update, context)
        return


    if text == "☎️ Aloqa operatori":
        await operator(update, context)
        return



    holat = context.user_data.get("holat")


    # Kredit olish bo'limi

    if holat == "ism":

        context.user_data["ism"] = text

        await update.message.reply_text(
            "📞 Telefon raqamingizni kiriting:"
        )

        context.user_data["holat"] = "telefon"



    elif holat == "telefon":

        context.user_data["telefon"] = text

        await update.message.reply_text(
            "💰 Qancha kredit kerak?"
        )

        context.user_data["holat"] = "kredit_summa"



    elif holat == "kredit_summa":

        context.user_data["kredit"] = text

        await update.message.reply_text(
            "📅 Necha oyga olmoqchisiz?"
        )

        context.user_data["holat"] = "muddat"



    elif holat == "muddat":

        await update.message.reply_text(
            f"""
✅ Ariza qabul qilindi!

👤 Ism: {context.user_data['ism']}
📞 Telefon: {context.user_data['telefon']}
💰 Kredit: {context.user_data['kredit']} so'm
📅 Muddat: {text} oy

Operator tez orada bog'lanadi.
"""
        )

        context.user_data.clear()



    # Kredit hisoblash bo'limi

    elif holat == "hisob_summa":

        summa = text.replace(".", "").replace(",", "").replace(" ", "")

        if not summa.isdigit():

            await update.message.reply_text(
                "❌ Summani faqat raqam bilan kiriting."
            )
            return


        context.user_data["summa"] = int(summa)


        await update.message.reply_text(
            "📅 Kredit muddatini kiriting (oy):"
        )

        context.user_data["holat"] = "hisob_oy"



    elif holat == "hisob_oy":

        if not text.isdigit():

            await update.message.reply_text(
                "❌ Oy sonini kiriting."
            )
            return


        summa = context.user_data["summa"]
        oy = int(text)

        foiz = 24

        jami = summa + (summa * foiz / 100)

        oylik = jami / oy


        await update.message.reply_text(
            f"""
🧮 Kredit hisoblash:

💰 Kredit: {summa:,} so'm
📅 Muddat: {oy} oy
📈 Foiz: {foiz}%

✅ Oylik to'lov:
{int(oylik):,} so'm

Jami to'lov:
{int(jami):,} so'm
"""
        )


        context.user_data.clear()



app = Application.builder().token(TOKEN).build()


app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(filters.TEXT, message)
)


print("Bot ishga tushdi...")


web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "Bot ishlayapti"


def run_web():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port)


threading.Thread(target=run_web).start()

app.run_polling()
