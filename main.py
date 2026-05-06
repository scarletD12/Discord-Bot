import discord
from discord.ext import commands
from discord import app_commands
import os
from datetime import datetime
import pytz

# ===== CONFIG =====
TOKEN = os.getenv("TOKEN")

WIB = pytz.timezone("Asia/Jakarta")
ORANGE = 0xf39c12

LOGO_URL = "https://imagetourl.cloud/gycxjsew.png"

ADMIN_ROLE = "ADMIN"
WARGA_ROLE = "WARGA"
VERIFY_ROLE = "Verified"

CHANNEL_ANNO = "‼️𝙰𝚗𝚗𝚘𝚞𝚗𝚌𝚎𝚖𝚎𝚗𝚝‼️"
CHANNEL_UPDATE = "𝙶𝚎𝚗𝚎𝚛𝚊𝚕-𝙲𝚑𝚊𝚝💬"

# ===== BOT =====
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

user_data = {}

# ===== READY =====
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Login sebagai {bot.user}")

# ===== EMBED =====
def create_embed(user, pesan, mode):
    now = datetime.now(WIB).strftime("%d %B %Y • %H:%M WIB")

    header = "### ANNOUNCEMENT SERVER 📢" if mode == "anno" else "### SERVER UPDATE 🔄"

    embed = discord.Embed(
        description=f"{header}\n\n{pesan}\n\n━━━━━━━━━━━━━━━━━━",
        color=ORANGE
    )

    embed.set_author(
        name=f"Posted by {user.display_name}",
        icon_url=user.display_avatar.url
    )

    embed.set_thumbnail(url=LOGO_URL)
    embed.set_footer(text=f"Tanah Air Roleplay • {now}", icon_url=LOGO_URL)

    return embed

# ===== VERIFY MODAL =====
class VerifyModal(discord.ui.Modal, title="📄 FORM REGISTRATION"):

    name = discord.ui.TextInput(label="Character Name")
    age = discord.ui.TextInput(label="Character Age")
    roblox = discord.ui.TextInput(label="Username Roblox")

    async def on_submit(self, interaction: discord.Interaction):
        user_id = interaction.user.id

        user_data[user_id] = {
            "name": self.name.value,
            "age": self.age.value,
            "roblox": self.roblox.value
        }

        role = discord.utils.get(interaction.guild.roles, name=VERIFY_ROLE)
        if role:
            await interaction.user.add_roles(role)

        now = datetime.now(WIB).strftime("%d %B %Y • %H:%M WIB")

        embed = discord.Embed(
            title="✅ Verification Successful",
            description="Selamat datang di Tanah Air Roleplay, Anda dapat bergabung dalam permainan sekarang.",
            color=ORANGE
        )

        embed.add_field(name="NAMA KARAKTER", value=self.name.value)
        embed.add_field(name="USIA KARAKTER", value=self.age.value)
        embed.add_field(name="USERNAME ROBLOX", value=self.roblox.value)

        embed.set_footer(text=f"Tanah Air Roleplay • {now}", icon_url=LOGO_URL)

        await interaction.response.send_message(embed=embed)

# ===== COMMAND =====
@bot.tree.command(name="verify", description="Verifikasi akun")
async def verify(interaction: discord.Interaction):
    await interaction.response.send_modal(VerifyModal())

@bot.tree.command(name="unverify", description="Hapus verifikasi")
async def unverify(interaction: discord.Interaction):

    role = discord.utils.get(interaction.guild.roles, name=VERIFY_ROLE)
    if role:
        await interaction.user.remove_roles(role)

    now = datetime.now(WIB).strftime("%d %B %Y • %H:%M WIB")

    embed = discord.Embed(
        description="Data Verifikasi Berhasil Dihapus!",
        color=ORANGE
    )
    embed.set_footer(text=f"Tanah Air Roleplay • {now}", icon_url=LOGO_URL)

    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="profile", description="Lihat profile")
async def profile(interaction: discord.Interaction):

    if interaction.user.id not in user_data:
        await interaction.response.send_message("Kamu belum verify!", ephemeral=True)
        return

    data = user_data[interaction.user.id]

    embed = discord.Embed(title="PLAYER PROFILE", color=ORANGE)
    embed.add_field(name="Nama", value=data["name"])
    embed.add_field(name="Usia", value=data["age"])
    embed.add_field(name="Roblox", value=data["roblox"])

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="serverinfo", description="Info server")
async def serverinfo(interaction: discord.Interaction):

    guild = interaction.guild

    embed = discord.Embed(title="SERVER INFORMATION", color=ORANGE)
    embed.add_field(name="Nama Server", value=guild.name)
    embed.add_field(name="Total Member", value=guild.member_count)

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="anno", description="Kirim pengumuman")
@app_commands.describe(pesan="Isi pengumuman")
async def anno(interaction: discord.Interaction, pesan: str):

    if not discord.utils.get(interaction.user.roles, name=ADMIN_ROLE):
        await interaction.response.send_message("Hanya ADMIN!", ephemeral=True)
        return

    channel = discord.utils.get(interaction.guild.channels, name=CHANNEL_ANNO)
    warga = discord.utils.get(interaction.guild.roles, name=WARGA_ROLE)

    embed = create_embed(interaction.user, pesan, "anno")

    await channel.send(content=warga.mention if warga else None, embed=embed)
    await interaction.response.send_message("Announcement terkirim!", ephemeral=True)

@bot.tree.command(name="anno-updt", description="Kirim update")
@app_commands.describe(pesan="Isi update")
async def anno_updt(interaction: discord.Interaction, pesan: str):

    if not discord.utils.get(interaction.user.roles, name=ADMIN_ROLE):
        await interaction.response.send_message("Hanya ADMIN!", ephemeral=True)
        return

    channel = discord.utils.get(interaction.guild.channels, name=CHANNEL_UPDATE)
    warga = discord.utils.get(interaction.guild.roles, name=WARGA_ROLE)

    embed = create_embed(interaction.user, pesan, "update")

    await channel.send(content=warga.mention if warga else None, embed=embed)
    await interaction.response.send_message("Update terkirim!", ephemeral=True)

# ===== RUN =====
bot.run(TOKEN)
