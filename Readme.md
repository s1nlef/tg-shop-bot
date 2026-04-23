# 🎮 TG Shop Bot

A Telegram bot for selling digital goods (games), built with Python and aiogram 3. Features a full purchase flow, order history, cart management, and an admin panel — backed by PostgreSQL and deployed via Docker.

---

## ✨ Features

- 🛒 **Catalog** — paginated game listings loaded from the database
- 🧺 **Cart** — add/remove items, quantity tracking
- 💳 **Purchase flow** — FSM-based checkout: cart → confirm → pay → receipt
- 📜 **Order history** — full purchase history per user
- 🗄️ **User cabinet** — balance and personal info
- 🔐 **Admin panel** — add games and manage user balances directly from Telegram
- 🐘 **PostgreSQL** + **Alembic** migrations
- 🐳 **Docker Compose** — one command to run the whole stack

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Bot framework | [aiogram 3](https://docs.aiogram.dev) |
| Language | Python 3.12+ |
| Database | PostgreSQL |
| ORM | SQLAlchemy 2 (async) |
| Migrations | Alembic |
| Driver | asyncpg |
| Deploy | Docker + Docker Compose |

---

## 🚀 Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/s1nlef/tg-shop-bot.git
cd tg-shop-bot
```

### 2. Set up environment variables

```bash
cp .env.example .env
```

Fill in `.env`:

```env
TOKEN=your_telegram_bot_token
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/shopbot
ADMINS_TG_ID=your_telegram_id
```

### 3. Run with Docker Compose

```bash
docker compose up --build
```

The bot starts automatically. Migrations run on first launch.

### 4. Run without Docker (local dev)

```bash
pip install -r requirements.txt
alembic upgrade head
python main.py
```

---

## 📁 Project Structure

```
tg-shop-bot/
├── app/
│   ├── database/
│   │   ├── models.py       # SQLAlchemy models
│   │   └── request.py      # DB queries (DAL)
│   ├── handlers/
│   │   ├── user.py         # User-facing handlers & FSM
│   │   └── admin.py        # Admin commands
│   └── keyboards/
│       ├── keyboards.py    # User keyboards
│       └── admkeyboard.py  # Admin keyboards
├── migrations/             # Alembic migrations
├── main.py
├── .env.example
├── Dockerfile
└── docker-compose.yml
```

---

## 🤖 Bot Commands

| Command | Description |
|---|---|
| `/start` | Open main menu |
| `/admin` | Open admin panel *(admin only)* |

### User Flow

```
/start → Menu
          ├── Catalog → [game page] → Add to cart
          ├── Cart    → Confirm → Pay → Receipt
          └── Cabinet → Order History
```

---

## 🗄️ Database Schema

```
users           games
─────────       ──────────
id              id
tg_id (unique)  name
balance         genre
                daterelease
                description
                price

cart_items      orders          orders_items
──────────      ──────────      ────────────
id              id              id
tg_id → users   tg_id → users   order_id → orders
game_id → games price           game_id  → games
quantity        status          quantity
                created_at      price
```

---

## ⚙️ Environment Variables

| Variable | Description |
|---|---|
| `TOKEN` | Telegram Bot API token (from [@BotFather](https://t.me/BotFather)) |
| `DATABASE_URL` | PostgreSQL connection string |
| `ADMINS_TG_ID` | Telegram ID of the admin user |

---

## 📌 Roadmap

- [x] Stage 0 — Bug fixes
- [x] Stage 1 — DB foundation (SQLAlchemy, relations, pagination)
- [x] Stage 2 — Full purchase flow (FSM, orders, balance)
- [x] Stage 3 — PostgreSQL + Alembic migrations
- [ ] Stage 4 — Docker deploy + VPS
- [ ] Game image support
- [ ] Search and genre filter
- [ ] Telegram Stars payment integration
- [ ] Auto game key delivery (`GameKey` table)
- [ ] Broadcast notifications

---

## 👤 Author

**s1nlef** — [@s1nlef](https://github.com/s1nlef)

> Built as a learning project evolving into a real product. Feedback and stars are welcome ⭐