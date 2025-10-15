from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class WalletUI:
    def create_wallet_interface(self, wallet_data=None):
        if wallet_data:
            keyboard = [
                [
                    InlineKeyboardButton("💰 יתרות", callback_data="wallet_balance"),
                    InlineKeyboardButton("📤 שלח", callback_data="wallet_send")
                ],
                [
                    InlineKeyboardButton("📥 קבל", callback_data="wallet_receive"),
                    InlineKeyboardButton("📊 היסטוריה", callback_data="wallet_history")
                ],
                [
                    InlineKeyboardButton("🛡️ אבטחה", callback_data="wallet_security"),
                    InlineKeyboardButton("🔗 חבר ארנק", callback_data="wallet_connect")
                ],
                [InlineKeyboardButton("🏠 דשבורד ראשי", callback_data="back_to_dashboard")]
            ]

            wallet_text = f"""
╔══════════════════════════════╗
║       💰 הארנק שלי          ║
╚══════════════════════════════╝

✅ **ארנק פעיל ומאובטח**

📬 **כתובת:** `{wallet_data['public_address']}`
📅 **נוצר:** {wallet_data['created_date']}

💫 **פעולות זמינות:**
•💰 **יתרות** - צפה ביתרות שלך
•📤 **שלח** - העבר מטבעות
•📥 **קבל** - קבל מטבעות
•📊 **היסטוריה** - עסקאות אחרונות
•🛡️ **אבטחה** - הגדרות אבטחה
•🔗 **חבר ארנק** - חבר ארנק נוסף
"""
        else:
            keyboard = [
                [InlineKeyboardButton("✨ צור ארנק חדש", callback_data="wallet_create")],
                [InlineKeyboardButton("🔗 חבר ארנק קיים", callback_data="wallet_connect")],
                [InlineKeyboardButton("📖 מדריך מפורט", callback_data="wallet_guide")],
                [InlineKeyboardButton("🏠 דשבורד ראשי", callback_data="back_to_dashboard")]
            ]

            wallet_text = """
╔══════════════════════════════╗
║     🚀 ארנק דיגיטלי         ║
╚══════════════════════════════╝

🎁 **קבל 1 SELA מתנה** על יצירת ארנק!

💫 **אפשרויות:**
• ✨ **צור ארנק חדש** - מאובטח ופשוט
• 🔗 **חבר ארנק קיים** - MetaMask, Trust Wallet
• 📖 **מדריך מפורט** - הדרכה שלב אחר שלב

🔐 **בטיחות מובטחת:**
• הצפנה מתקדמת
• גיבוי אוטומטי
• אבטחה bank-level
"""

        reply_markup = InlineKeyboardMarkup(keyboard)
        return wallet_text, reply_markup
