import os, telebot, sqlite3, random, hashlib
from telebot import types

BOT_TOKEN = os.getenv("BOT_TOKEN") or "8898773489:AAHrtseaLsiv117yl_CCROOxOvW-zsw1oOQ@BotFather"
ADMIN_ID = int(os.getenv("ADMIN_ID") or "7093374788") # راح تجيبه من @userinfobot
ADMIN_USERNAME = "Aa151000" # @Ahvfg0555bot
BOT_USERNAME = "Ahvfg0555bot" # @Aa151000

bot = telebot.TeleBot(BOT_TOKEN)
conn = sqlite3.connect('bot.db', check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users 
(user_id INTEGER PRIMARY KEY, tg_username TEXT, custom_id TEXT, password TEXT, balance REAL DEFAULT 0, logged INTEGER DEFAULT 0, total_buy INTEGER DEFAULT 0)''')
c.execute('''CREATE TABLE IF NOT EXISTS numbers 
(id INTEGER PRIMARY KEY AUTOINCREMENT, country TEXT, service TEXT, number TEXT, code TEXT, price REAL, is_used INTEGER DEFAULT 0, full TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS orders 
(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, number_id INTEGER, status TEXT)''')
conn.commit()

def hash_pw(p): return hashlib.sha256(p.encode()).hexdigest()
user_states = {}

PRICES = {
    "whatsapp_sa": 5,
    "whatsapp_eg": 5,
    "whatsapp_all": 10,
    "telegram": 10,
    "followers": 15,
    "offer_12": 20,
    "offer_whatsapp": 5
}

def main_menu():
    m = types.InlineKeyboardMarkup(row_width=2)
    m.add(
        types.InlineKeyboardButton("🔥 عروض واتساب 5 روبل ✅", callback_data="offer_whatsapp"),
        types.InlineKeyboardButton("📱 واتساب 5-10 روبل", callback_data="buy_whatsapp"),
        types.InlineKeyboardButton("✈️ تليجرام 10 روبل", callback_data="buy_telegram"),
        types.InlineKeyboardButton("👥 متابعين 15 روبل", callback_data="buy_followers"),
        types.InlineKeyboardButton("🎁 عرض 12 رقم 20 روبل", callback_data="offer_12"),
        types.InlineKeyboardButton("🌍 كل الدول + الأصفار", callback_data="countries"),
        types.InlineKeyboardButton("💰 رصيدي", callback_data="balance"),
        types.InlineKeyboardButton("👤 حسابي: Aa151000", callback_data="account"),
        types.InlineKeyboardButton("🎧 تواصل مع الدعم @Aa151000", url="https://t.me/Aa151000"),
    )
    return m

@bot.message_handler(commands=['start'])
def start(msg):
    uid = msg.from_user.id
    c.execute("SELECT * FROM users WHERE user_id=?", (uid,))
    user = c.fetchone()
    
    if not user:
        bot.send_message(msg.chat.id, f"@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحبا بك في بوت الارقام الوهمية.")
        {msg.from_user.first_name} 👋 في بوت @{BOT_USERNAME}\n\nالبوت شغال 24 ساعة 🟢\n\nالخطوة 1: اختر اسم لحسابك الخاص (مثلا: albraa123)")
        user_states[uid] = "wait_custom_id"
        return

    if not user[2] or user[2] == "":
        bot.send_message(msg.chat.id, "اختر اسم لحسابك الخاص:")
        user_states[uid] = "wait_custom_id"
    elif not user[3]:
        bot.send_message(msg.chat.id, f"حسابك: {user[2]}\nالآن اختر كلمة مرور:")
        user_states[uid] = "wait_password"
    elif user[5] == 0:
        bot.send_message(msg.chat.id, f"أهلا بعودتك @{msg.from_user.username}\nحسابك: {user[2]}\n\nأدخل كلمة مرورك:")
        user_states[uid] = "wait_login"
    else:
        bot.send_message(msg.chat.id, f"""
أهلا بك يا {msg.from_user.first_name} 👋

👤 حسابك الخاص: {user[2]}
💰 رصيدك: {user[4]} روبل
🔢 مشترياتك: {user[6]}
🤖 البوت: @{BOT_USERNAME}
👑 الدعم: @Aa151000

اختر الخدمة:
""", reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.from_user.id in user_states)
def state_handler(msg):
    uid = msg.from_user.id
    state = user_states[uid]
    text = msg.text.strip()
    
    if state == "wait_custom_id":
        c.execute("SELECT * FROM users WHERE custom_id=?", (text,))
        if c.fetchone():
            bot.send_message(msg.chat.id, "❌ الاسم محجوز، اختر اسم ثاني:")
            return
        tg_user = msg.from_user.username or "بدون"
        c.execute("INSERT OR REPLACE INTO users (user_id, tg_username, custom_id, password, balance, logged) VALUES (?,?,?,?,?,?)",
                  (uid, tg_user, text, "", 0, 0))
        conn.commit()
        bot.send_message(msg.chat.id, f"✅ تم حجز اسم حسابك: {text}\n\nالخطوة 2: اختر كلمة مرور:")
        user_states[uid] = "wait_password"
        
    elif state == "wait_password":
        pw = hash_pw(text)
        c.execute("UPDATE users SET password=?, logged=1 WHERE user_id=?", (pw, uid))
        conn.commit()
        del user_states[uid]
        c.execute("SELECT * FROM users WHERE user_id=?", (uid,))
        user = c.fetchone()
        bot.send_message(msg.chat.id, f"✅ تم إنشاء حسابك!\n\n👤 حسابك: {user[2]}\n💰 رصيدك: {user[4]} روبل\n\nللشحن تواصل مع @Aa151000 وقل له اشحن حساب {user[2]}", reply_markup=main_menu())
        
    elif state == "wait_login":
        pw = hash_pw(text)
        c.execute("SELECT * FROM users WHERE user_id=? AND password=?", (uid, pw))
        if c.fetchone():
            c.execute("UPDATE users SET logged=1 WHERE user_id=?", (uid,))
            conn.commit()
            del user_states[uid]
            bot.send_message(msg.chat.id, "✅ تم تسجيل الدخول", reply_markup=main_menu())
        else:
            bot.send_message(msg.chat.id, "❌😭 كلمة مرور خطأ:")

@bot.message_handler(content_types=['document'])
def handle_file(msg):
    if msg.from_user.id != ADMIN_ID: return
    file = bot.get_file(msg.document.file_id)
    data = bot.download_file(file.file_path).decode('utf-8')
    added = 0
    for line in data.splitlines():
        if not line.strip() or line.startswith('#'): continue
        try:
            parts = [x.strip() for x in line.split(',')]
            country, service, number, code = parts[:4]
            price = float(parts[4]) if len(parts) > 4 else 5
            full = number
            c.execute("INSERT INTO numbers (country, service, number, code, price, full) VALUES (?,?,?,?,?,?)",
                      (country, service, number, code, price, full))
            added += 1
        except: pass
    conn.commit()
    bot.reply_to(msg, f"✅ يا @Aa151000 تم إضافة {added} رقم\nالبوت @{BOT_USERNAME} جاهز")

@bot.callback_query_handler(func=lambda x: True)
def callbacks(call):
    uid = call.from_user.id
    c.execute("SELECT * FROM users WHERE user_id=?", (uid,))
    user = c.fetchone()
    if not user or user[5]==0:
        bot.answer_callback_query(call.id, "سجل /start")
        return

    if call.data.startswith("buy_") or call.data.startswith("offer_"):
        if call.data == "offer_whatsapp":
            service, price = "whatsapp", 5
        elif call.data == "buy_whatsapp":
            service, price = "whatsapp", 10
        elif call.data == "buy_telegram":
            service, price = "telegram", 10
        elif call.data == "buy_followers":
            service, price = "followers", 15
        elif call.data == "offer_12":
            if user[4] < 20:
                bot.send_message(call.message.chat.id, f"❌ رصيدك {user[4]}، العرض 20 روبل\nتواصل مع @Aa151000 للشحن: اشحن حساب {user[2]} بـ 50")
                return
            c.execute("UPDATE users SET balance=balance-20 WHERE user_id=?", (uid,))
            conn.commit()
            bot.send_message(call.message.chat.id, f"✅ تم تفعيل عرض 12 رقم، تواصل مع @Aa151000 لاستلامها")
            return
        else:
            service, price = "whatsapp", 5

        c.execute("SELECT * FROM numbers WHERE service=? AND is_used=0 LIMIT 1", (service,))
        num = c.fetchone()
        if not num:
            bot.send_message(call.message.chat.id, f"❌ لا يوجد أرقام {service}، خلي الأدمن @Aa151000 يرسل ملف")
            return
        if user[4] < price:
            bot.send_message(call.message.chat.id, f"❌ رصيدك {user[4]} روبل، السعر {price}\n\n💳 للشحن: راسل @Aa151000\nقل: اشحن حساب {user[2]} بـ 100")
            return
        
        c.execute("UPDATE users SET balance=balance-?, total_buy=total_buy+1 WHERE user_id=?", (price, uid))
        c.execute("UPDATE numbers SET is_used=1 WHERE id=?", (num[0],))
        c.execute("INSERT INTO orders (user_id, number_id, status) VALUES (?,?,?)", (uid, num[0], "waiting"))
        conn.commit()
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔄 تحديث الكود - يطلع الكود فورا", callback_data=f"refresh_{num[0]}"))
        
        bot.send_message(call.message.chat.id, f"""
✅ تم الشراء - خصم تلقائي {price} روبل

👤 حسابك: {user[2]}
🌍 الدولة: {num[1]}
📱 الرقم: `{num[3]}`
💰 باقي رصيدك: {user[4]-price} روبل
👑 الدعم: @Aa151000

1- انسخ الرقم وحطه في الواتساب
2- اطلب الكود
3- اضغط تحديث الكود 👇
""", reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("refresh_"):
        nid = int(call.data.split("_")[1])
        c.execute("SELECT * FROM numbers WHERE id=?", (nid,))
        num = c.fetchone()
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔄 تحديث مرة أخرى", callback_data=f"refresh_{nid}"))
        markup.add(types.InlineKeyboardButton("🎧 دعم @Aa151000", url="https://t.me/Aa151000"))
        bot.send_message(call.message.chat.id, f"🔑 كودك: `{num[4]}`\n📱 للرقم: {num[3]}\n✅ انسخه للواتساب", reply_markup=markup, parse_mode="Markdown")

    elif call.data == "balance":
        bot.send_message(call.message.chat.id, f"💰 رصيدك: {user[4]} روبل\n👤 حسابك: {user[2]}\n\nأسعار @Aa151000:\nواتساب 5-10 روبل\nتليجرام 10 روبل\nمتابعين 15 روبل\nعرض 12 رقم 20 روبل\n\nللشحن: @Aa151000")
    elif call.data == "account":
        bot.send_message(call.message.chat.id, f"👤 حسابك الخاص:\n\nالاسم: {user[2]}\nتليجرام: @{user[1]}\nايدي: {user[0]}\nرصيد: {user[4]}\nبوتك: @{BOT_USERNAME}\nالدعم: @Aa151000")
    elif call.data == "countries":
        bot.send_message(call.message.chat.id, "🌍 كل الدول كاملة بالأصفار: SA EG US RU TR IN ID...")

@bot.message_handler(commands=['charge','stock'])
def admin_cmds(msg):
    if msg.from_user.id != ADMIN_ID: return
    if msg.text.startswith('/charge'):
        try:
            _, target, amount = msg.text.split()
            amount = float(amount)
            if target.isdigit():
                c.execute("UPDATE users SET balance=balance+? WHERE user_id=?", (amount, int(target)))
                uid_target = int(target)
            else:
                c.execute("UPDATE users SET balance=balance+? WHERE custom_id=?", (amount, target))
                c.execute("SELECT user_id FROM users WHERE custom_id=?", (target,))
                row = c.fetchone()
                uid_target = row[0] if row else None
            conn.commit()
            bot.reply_to(msg, f"✅ تم شحن {amount} لـ {target}")
            if uid_target:
                try:
                    bot.send_message(uid_target, f"💰 تم شحن رصيدك {amount} روبل من @Aa151000 ✅")
                except: pass
        except Exception as e:
            bot.reply_to(msg, f"الصح: /charge اسم_الحساب 100\nمثال: /charge albraa123 50\n{e}")
    elif msg.text.startswith('/stock'):
        c.execute("SELECT country, service, COUNT(*) FROM numbers WHERE is_used=0 GROUP BY country, service")
        rows = c.fetchall()
        txt = "📦 مخزون @Ahvfg0555bot:\n" + "\n".join([f"{r[0]} {r[1]}: {r[2]}" for r in rows]) if rows else "فاضي"
        bot.reply_to(msg, txt)

print("Bot @Ahvfg0555bot for @Aa151000 running 24/7...")
bot.infinity_polling()
