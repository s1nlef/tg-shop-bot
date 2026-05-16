# 👟 TG Sneaker Shop Bot

A Telegram bot for selling sneakers, built with Python and aiogram 3. Features a complete purchase flow with FSM-based state management, cart system, order history, and admin panel for managing inventory and user balances.

---

## ✨ Features

- 🛒 **Catalog** — Brand-based catalog with pagination and filtering
- 🧺 **Cart** — Add/remove items, quantity tracking
- 💳 **Purchase flow** — FSM-based checkout: cart → confirm → pay → receipt
- 📜 **Order history** — Full purchase history per user
- 🗄️ **User cabinet** — Balance and personal info
- 🔐 **Admin panel** — Add sneakers with sizes/stock, manage user balances
- 📏 **Size management** — Multiple sizes per sneaker with individual stock tracking
- 🐘 **PostgreSQL** + **Alembic** migrations
- 🐳 **Docker Compose** — One command to run the whole stack
- 🔒 **Security** — Input validation, error handling, Path Traversal protection

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Bot framework | [aiogram 3](https://docs.aiogram.dev) |
| Language | Python 3.12+ |
| Database | PostgreSQL 16 |
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

Create `.env` file:

```env
TOKEN=your_telegram_bot_token
DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/tg_shop_db
POSTGRES_PASSWORD=your_password
ADMINS_TG_IDS=your_telegram_id
```

**Get your Telegram Bot Token:**
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` and follow instructions
3. Copy the token to `.env`

**Get your Telegram ID:**
1. Message [@userinfobot](https://t.me/userinfobot) on Telegram
2. Copy your ID to `.env`

### 3. Run with Docker Compose

```bash
docker compose up --build
```

The bot starts automatically. Migrations run on first launch.

### 4. Seed the database (optional)

```bash
python seed.py
```

This adds 18 demo sneakers (Nike, Asics, New Balance, Converse) with Ukrainian sizes (36-46).

### 5. Run without Docker (local dev)

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Seed database (optional)
python seed.py

# Start bot
python main.py
```

---

## 📁 Project Structure

```
tg-shop-bot/
├── app/
│   ├── database/
│   │   ├── models.py       # SQLAlchemy models
│   │   └── request.py      # Database queries (DAL)
│   ├── handlers/
│   │   ├── purchase.py     # Purchase flow & main menu
│   │   ├── catalog.py      # Product browsing & filtering
│   │   └── admin.py        # Admin commands
│   └── keyboards/
│       ├── keyboards.py    # User keyboards
│       └── admkeyboard.py  # Admin keyboards
├── migrations/             # Alembic migrations
├── image/                  # Brand images
├── main.py                 # Bot entry point
├── seed.py                 # Database seeding script
├── .env                    # Environment variables (create this)
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
          ├── Catalog → [Brand] → [Product] → Add to cart
          ├── Cart    → Confirm → Pay → Receipt
          └── Cabinet → Order History
```

### Admin Flow

```
/admin → Admin Menu
          ├── Change balance → Enter new balance
          └── Add sneaker → Brand → Model → Colorway → Price → Image URL
                          → Select sizes → Enter stock per size → Confirm
```

---

## 🗄️ Database Schema

```
users                sneakers              sneakers_size
─────────            ──────────            ─────────────
id                   id                    id
tg_id (unique)       brand                 sneaker_id → sneakers
balance              model                 size
                     colorway              stock
                     price
                     image_url

cart_items           orders                orders_items
──────────           ──────────            ────────────
id                   id                    id
tg_id → users        tg_id → users         order_id → orders
sneaker_id → sneakers price                sneaker_id → sneakers
quantity             status                quantity
                     created_at            price
```

---

## ⚙️ Environment Variables

| Variable | Description | Example |
|---|---|---|
| `TOKEN` | Telegram Bot API token from @BotFather | `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11` |
| `DATABASE_URL` | PostgreSQL async connection string | `postgresql+asyncpg://postgres:pass@localhost:5432/tg_shop_db` |
| `POSTGRES_PASSWORD` | PostgreSQL password for Docker | `your_secure_password` |
| `ADMINS_TG_IDS` | Comma-separated Telegram user IDs | `123456789,987654321` |

---

## 🐳 Docker Architecture

The `docker-compose.yml` defines three services:

1. **db** — PostgreSQL 16 with health check
2. **migrate** — Runs `alembic upgrade head` once, then exits
3. **bot** — Starts polling after migrations complete

All services use `network_mode: host` and share the same `.env` file.

---

## 🔒 Security Features

- ✅ Global error handler prevents stack trace exposure
- ✅ Brand name validation against database (Path Traversal protection)
- ✅ Input validation in admin panel (price, stock)
- ✅ Product existence checks before display
- ✅ `.env` in `.gitignore` (credentials never committed)

---

## 📌 Roadmap

- [x] Stage 0 — Bug fixes
- [x] Stage 1 — Database foundation (SQLAlchemy, relations, pagination)
- [x] Stage 2 — Full purchase flow (FSM, orders, balance)
- [x] Stage 3 — PostgreSQL + Alembic migrations
- [x] Stage 4 — Docker deployment
- [x] Stage 5 — Sneaker shop features (brands, sizes, stock)
- [ ] Size selection before adding to cart
- [ ] Stock deduction on purchase
- [ ] Telegram Stars payment integration
- [ ] Search and filters (size, price)
- [ ] Notifications ("your size is back in stock")
- [ ] CI/CD (GitHub Actions)

---

## 🧪 Testing

```bash
# Test full flow locally:
# 1. Start bot: python main.py
# 2. Open Telegram and message your bot
# 3. Test user flow: /start → Catalog → Brand → Product → Add to cart → Cart → Buy
# 4. Test admin flow: /admin → Add sneaker (fill all fields)
# 5. Check database: docker compose exec db psql -U postgres -d tg_shop_db
```

---

## 🛠️ Development

```bash
# Create new migration after model changes
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Connect to database
docker compose exec db psql -U postgres -d tg_shop_db

# View logs
docker compose logs -f bot
```

---

## 👤 Author

**s1nlef** — [@s1nlef](https://github.com/s1nlef)

> Built as a learning project evolving into a real product. Feedback and stars are welcome ⭐

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
