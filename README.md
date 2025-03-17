# 📢 CFReminder-Bot  

A **Discord bot** that **automatically fetches upcoming Codeforces contests** and **sends reminders** to a designated Discord channel and subscribed users via **DMs**.

---

## ⚡ Features  
- 🔔 **Automated Reminders**: Fetches upcoming **Codeforces contests** every 8 hours.  
- 📩 **Private Message Notifications**: Users can subscribe via `/subscribe` to receive **direct messages** with contest details.  
- 🔄 **Unsubscribe Anytime**: Users can opt-out with `/unsubscribe`.  
- ⏳ **Countdown Timer**: Shows remaining time until the next contest.  
- 🌎 **Time Zone Conversion**: Displays contest times in **Central European Time (CET/CEST)**.  
- 📡 **Docker Support**: Easily deploy with **Docker** and `docker-compose`.  
- 🛠 **SQLite Persistence**: Keeps track of user subscriptions across restarts.  

---

## 🛠 Installation & Setup  

### **1️⃣ Prerequisites**  
Ensure you have:  
- **Python 3.8+** installed  
- **Discord bot token** (from the [Discord Developer Portal](https://discord.com/developers/applications))  
- **Codeforces API** access (no key required)  
- **Docker (optional, for deployment)**  

---

### **2️⃣ Clone the Repository**  
```sh
git clone https://github.com/yourusername/cfreminder-bot.git
cd cfreminder-bot
```

### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4️⃣ Set Up Environment Variables**
Create a .env file and add your Discord Bot Token:
```
DISCORD_BOT_TOKEN=your-bot-token-here
```

### **5️⃣ Run the Bot Locally**
```sh
python main.py
```

### 📖 Commands
Command	Description
/next	Fetches and displays the next Codeforces contest.
/subscribe	Subscribes the user to receive private DM reminders.
/unsubscribe	Unsubscribes the user from private DM reminders.
#### 🐳 Docker Deployment

1️⃣ Build & Run the Docker Container
```sh
docker build -t cfreminder-bot .
docker run -d --name cfreminder --env-file .env cfreminder-bot
```
2️⃣ Using Docker Compose
If using docker-compose.yml, start the bot with:
```sh
docker-compose up -d
```
🎯 How It Works
1️⃣ The bot fetches upcoming Codeforces contests every 8 hours.

2️⃣ It sends contest reminders to:
The #cf提醒 text channel in the Discord server.
Subscribed users' DMs if they used /subscribe.

3️⃣ Users can unsubscribe at any time using /unsubscribe.

📸 Screenshots
![e17bf3dcec28ce208a8ddf60126016fd](https://github.com/user-attachments/assets/9ba28c41-6f6f-43b9-9573-256060c0bdb7)


💡 Future Improvements
✅ Support for custom time zones.
✅ Ability to set reminders closer to contest time.
✅ Support for more competitive programming platforms (AtCoder, LeetCode, etc.).
🤝 Contributing
PRs and suggestions are welcome! Feel free to open an issue or submit a pull request.

📜 License
This project is licensed under the MIT License.

🚀 Happy Coding & Good Luck on Codeforces! 🏆

---

## **✅ What This README Covers**
- **Overview** of the bot  
- **Features** list  
- **Installation & Setup**  
- **Commands (`/next`, `/subscribe`, `/unsubscribe`)**  
- **Docker Deployment**  
- **How the Bot Works**  
- **Future Enhancements**  
- **Contribution & License Info**  

---

### **📌 Next Steps**
- **Replace** `"yourusername"` with your **GitHub username** in the repository link.  
- **Customize** the README if needed (e.g., add screenshots, extra features).  
- **Push the `README.md` to GitHub**:  
  ```sh
  git add README.md
  git commit -m "Added README"
  git push origin main
  ```
