import discord
import requests
import sqlite3
from discord import app_commands
from discord.ext import commands, tasks
from datetime import datetime, timezone
import pytz
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 从环境变量获取 Token
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# 设置 Intents
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True  # 允许 Bot 读取消息
intents.dm_messages = True  # 允许 Bot 监听私信
intents.message_content = True  # 允许 Bot 访问消息内容

# **使用 commands.Bot**
bot = commands.Bot(command_prefix="!", intents=intents)

# **初始化 SQLite 数据库**
def init_db():
    conn = sqlite3.connect("subscribers.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY
        )
    """)
    conn.commit()
    conn.close()

init_db()  # 初始化数据库

# **订阅用户**
def add_subscriber(user_id):
    conn = sqlite3.connect("subscribers.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO subscribers (id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

# **取消订阅**
def remove_subscriber(user_id):
    conn = sqlite3.connect("subscribers.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM subscribers WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

# **获取所有订阅用户**
def get_all_subscribers():
    conn = sqlite3.connect("subscribers.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM subscribers")
    users = [row[0] for row in cursor.fetchall()]
    conn.close()
    return users

# **Codeforces API**
API_URL = "https://codeforces.com/api/contest.list"

def get_next_contest():
    """获取下一场 Codeforces 比赛信息，并提供倒计时"""
    try:
        response = requests.get(API_URL)
        data = response.json()

        if data["status"] != "OK":
            return "❌ Codeforces API 返回错误"

        contests = data["result"]
        upcoming_contests = [c for c in contests if c["phase"] == "BEFORE"]

        if not upcoming_contests:
            return "📢 目前没有即将到来的比赛！"

        # 按开始时间排序，获取最近的比赛
        next_contest = sorted(upcoming_contests, key=lambda x: x["startTimeSeconds"])[0]

        # 定义中欧时区
        CET = pytz.timezone("Europe/Berlin")

        # 获取 UTC 时间并转换为中欧时区
        contest_utc_time = datetime.utcfromtimestamp(next_contest["startTimeSeconds"]).replace(tzinfo=timezone.utc)
        contest_cet_time = contest_utc_time.astimezone(CET).strftime('%Y-%m-%d %H:%M:%S %Z')

        # 计算倒计时
        now = datetime.now(timezone.utc)
        time_left = contest_utc_time - now

        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        # 生成倒计时文本
        countdown = f"{days} 天 {hours} 小时 {minutes} 分钟" if days > 0 else f"{hours} 小时 {minutes} 分钟"

        # 返回格式化的比赛信息
        return (
            f"🎯 **下一场 Codeforces 比赛**\n"
            f"```yaml\n"
            f"🏆 比赛名称: {next_contest['name']}\n"
            f"🕒 开始时间: {contest_cet_time}\n"
            f"⏳ 倒计时: {countdown}\n"
            f"🔗 比赛链接: https://codeforces.com/contest/{next_contest['id']}\n"
            f"```"
        )
    except Exception as e:
        return f"❌ 获取比赛信息失败: {str(e)}"

# 斜杠命令 `/next`
@bot.tree.command(name="next", description="查询下一场 Codeforces 比赛")
async def contest(interaction: discord.Interaction):
    """查询下一场 Codeforces 比赛"""
    await interaction.response.send_message(get_next_contest())


# **斜杠命令 `/subscribe` 订阅比赛提醒**
@bot.tree.command(name="subscribe", description="订阅 Codeforces 竞赛提醒")
async def subscribe(interaction: discord.Interaction):
    """用户订阅私信提醒"""
    if interaction.guild is not None:
        await interaction.response.send_message("❌ 该命令只能在私信中使用！", ephemeral=True)
        return

    user_id = interaction.user.id
    add_subscriber(user_id)
    await interaction.response.send_message("✅ 你已成功订阅 Codeforces 竞赛提醒！", ephemeral=True)

# **斜杠命令 `/unsubscribe` 取消订阅**
@bot.tree.command(name="unsubscribe", description="取消 Codeforces 竞赛提醒")
async def unsubscribe(interaction: discord.Interaction):
    """用户取消订阅私信提醒"""
    if interaction.guild is not None:
        await interaction.response.send_message("❌ 该命令只能在私信中使用！", ephemeral=True)
        return

    user_id = interaction.user.id
    remove_subscriber(user_id)
    await interaction.response.send_message("✅ 你已成功取消 Codeforces 竞赛提醒！", ephemeral=True)

# **定时任务：每 8 小时通知订阅者**
@tasks.loop(hours=8)
async def check_contest():
    """定时检查 Codeforces 比赛并给所有订阅者和服务器频道发送消息"""
    contest_info = get_next_contest()

    # **给所有订阅的用户发送私信**
    subscribers = get_all_subscribers()
    for user_id in subscribers:
        user = bot.get_user(user_id)
        if user:
            try:
                await user.send(contest_info)
                print(f"✅ 成功私信 {user.name}")
            except discord.Forbidden:
                print(f"❌ {user.name} 拒绝私信")
        else:
            print(f"❌ 无法找到 ID {user_id} 的用户")

    # **在服务器频道发送提醒**
    for guild in bot.guilds:
        channel = discord.utils.get(guild.text_channels, name="cf提醒")  # 确保频道名称正确
        if channel:
            try:
                await channel.send(contest_info)
                print(f"✅ 发送到服务器频道 {guild.name} -> {channel.name}")
            except discord.Forbidden:
                print(f"❌ Bot 没有权限在 {guild.name} 发送消息")
        else:
            print(f"❌ 在服务器 {guild.name} 找不到频道 'cf提醒'，跳过发送比赛通知。")


@bot.event
async def on_ready():
    """Bot 启动后执行"""
    print(f"✅ Bot 已登录为 {bot.user}")

    # **同步斜杠命令**
    try:
        for guild in bot.guilds:
            await bot.tree.sync(guild=guild)
        print("✅ 斜杠命令已同步")
    except Exception as e:
        print(f"❌ 斜杠命令同步失败: {e}")

    # **启动定时任务**
    check_contest.start()

# 启动 Bot
bot.run(TOKEN)
