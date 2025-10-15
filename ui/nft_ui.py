from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class NFTUI:
    def create_nft_gallery(self, user_nfts):
        text = "🎨 **גלריית ה-NFT שלך**\n"
        if not user_nfts:
            text += "\nעדיין אין לך NFTs."
        else:
            for i, n in enumerate(user_nfts, 1):
                stars = "⭐" * int(n.get('rarity', 1))
                text += f"\n{i}. {n['name']} {stars} — `{n['token_id']}`"
        kb = [
            [InlineKeyboardButton("🖼️ הצג את ה-NFT שלי", callback_data="nft_show")],
            [InlineKeyboardButton("🔼 העלאה", callback_data="nft_upload")],
            [InlineKeyboardButton("↩️ חזרה", callback_data="back_to_dashboard")]
        ]
        return text, InlineKeyboardMarkup(kb)
