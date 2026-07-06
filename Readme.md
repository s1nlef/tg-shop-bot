# Sneaker Shop Bot

Telegram bot for sneaker shop with cart system, order management, and admin panel. Built with aiogram 3, SQLAlchemy, and PostgreSQL.

## Features

**User Side**
- Browse catalog by brand with pagination
- Filter by size and price
- Shopping cart with quantity tracking
- Order history and receipts
- FSM-based checkout flow

**Admin Panel**
- Add/delete products
- Update stock per size
- Manage inventory
- Track all orders

**Technical**
- Async architecture (aiogram 3 + SQLAlchemy 2)
- PostgreSQL with Alembic migrations
- Docker Compose deployment
- Input validation and error handling

## Tech Stack

Python 3.12 • aiogram 3 • SQLAlchemy 2 • PostgreSQL 16 • Alembic • asyncpg • Docker

## Setup

**Requirements:** Docker, or Python 3.12+ with PostgreSQL

### With Docker

```bash
git clone https://github.com/shwdabyss/SneakerShopBot.git
cd SneakerShopBot

# Create .env file
cat > .env << EOF
TOKEN=your_bot_token
DATABASE_URL=postgresql+asyncpg://postgres:your_password@db:5432/tg_shop_db
POSTGRES_PASSWORD=your_password
ADMINS_TG_IDS=your_telegram_id
EOF

docker compose up --build
```

### Without Docker

```bash
git clone https://github.com/shwdabyss/SneakerShopBot.git
cd SneakerShopBot

# Install dependencies
pip install -r requirements.txt

# Create .env (update DATABASE_URL host to localhost)
cat > .env << EOF
TOKEN=your_bot_token
DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/tg_shop_db
POSTGRES_PASSWORD=your_password
ADMINS_TG_IDS=your_telegram_id
EOF

# Run migrations
alembic upgrade head

# Start bot
python main.py
```

### Get Credentials

- **Bot Token:** Message [@BotFather](https://t.me/BotFather) → `/newbot`
- **Your Telegram ID:** Message [@userinfobot](https://t.me/userinfobot)

### Seed Database (Optional)

```bash
python seed.py
```

Adds 18 demo sneakers across Nike, Asics, New Balance, Converse with sizes 36-46.

## Project Structure

```
app/
├── database/
│   ├── models.py         # SQLAlchemy models & database setup
│   └── request.py        # Database queries (DAL)
├── handlers/
│   ├── purchase.py       # Purchase flow & main menu
│   ├── catalog.py        # Product browsing & filtering
│   └── admin.py          # Admin panel
└── keyboards/
    ├── keyboards.py      # User keyboards
    └── admkeyboard.py    # Admin keyboards

migrations/               # Alembic migrations
image/                    # Brand images
main.py                   # Bot entry point
seed.py                   # Database seeding
.env                      # Environment variables (create this)
docker-compose.yml
```

## Usage

**Commands**
- `/start` — Open main menu
- `/admin` — Admin panel (admin only)

**User Flow**

```
/start
  ├─ Catalog → Brand → Product → Add to cart
  ├─ Cart → Checkout → Payment → Receipt
  └─ Cabinet → Order history
```

**Admin Flow**

```
/admin
  ├─ Add sneaker → Brand/Model/Price/Image → Sizes/Stock
  ├─ Admin catalog → Update stock / Delete product
  └─ Change balance
```

## Database Schema

```
users                 sneakers              sneakers_size
─────────             ──────────            ─────────────
id                    id                    id
tg_id (unique)        brand                 sneaker_id → sneakers
                      model                 size
                      colorway              stock
                      price
                      image_url

cart_items            orders                orders_items
──────────            ──────────            ────────────
id                    id                    id
tg_id → users         tg_id → users         order_id → orders
sneaker_id → sneakers price                 sneaker_id → sneakers
quantity              status                quantity
size                  created_at            price
```

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `TOKEN` | Telegram bot token from @BotFather | `123456:ABC-DEF...` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://user:pass@host:5432/db` |
| `POSTGRES_PASSWORD` | Database password | `your_secure_password` |
| `ADMINS_TG_IDS` | Comma-separated admin IDs | `123456789,987654321` |

## Development

```bash
# Create migration after model changes
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1

# Connect to database
docker compose exec db psql -U postgres -d tg_shop_db

# View logs
docker compose logs -f bot
```

## Security

- Global error handler (no stack trace exposure)
- Brand name validation (path traversal protection)
- Input validation on admin panel
- Environment variables in `.gitignore`

## License

MIT License - see [LICENSE](LICENSE) file for details
