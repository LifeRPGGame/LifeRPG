<h3><p align="center">LifeRPG</p></h3>

<p align="center">LifeRPG is an open-source task management application based on 
gamification techniques, specifically those used in role-playing games (RPGs) works in Telegram</p>

<p align="center">
  
  ![sublogo](https://github.com/user-attachments/assets/995a88fb-9721-43db-b466-162863265057)

</p>

![wakatime](https://wakatime.com/badge/user/018ce029-5220-4722-881d-fc5406c5e923/project/3180761b-ecef-4283-86e3-cf8bbff5d218.svg)
<hr>


## 🕹 Game Attributes
Your character will possess the following game attributes:
- Levels
- Hearts
- Power
- Experience points
- Coins


## ⚡ Features
- Create your own `Locations`
- Create your own `Quests` with rewards
- Fight mobs in battles
- Enhance your real-life experiences
- Monitor the actual progress of your journey


## ⚙ Getting Started
If you want to run, edit or improve this code - just follow these steps.

Clone repository:
```bash
git clone https://github.com/LifeRPGGame/LifeRPG.git
```

Change catalog:
```bash
cd LifeRPG
```

Create `.env` file in `src` catalog and fill by your data:
```bash
BOT_KEY='HERE YOUR TOKEN by BotFather'
LOG_TOKEN='OPTIONAL'
MODERATOR_ID='TELEGRAM ID FOR MODERATOR'
POSTGRESQL_HOST='HERE HOST'
POSTGRESQL_PORT=HERE PORT
POSTGRESQL_USER=HERE USER
POSTGRESQL_PASSWORD=HERE PASSWORD
POSTGRESQL_DBNAME=HERE DATABASE NAME
```

Activate <a href='https://python-poetry.org/'>poetry</a> environment:
```bash
poetry shell
```

Install dependencie:
```bash
poetry install
```

Run your bot:
```bash
python3 bot.py
```

Open your Telegram bot and enjoy :3


## ⭐ For contributers
If you're interesting about the project - follow these steps.

Make a fork by a `Fork` button.

Clone your fork to your local.

Create a new branch for changes:
```bash
git branch -m NEW_BRANCH_NAME
```

Switch branch:
```bash
git switch NEW_BRANCH_NAME
```

After your changes push these.

Create a Pull Request.

