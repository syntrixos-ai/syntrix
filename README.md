# Syntrix AI - Business Intelligence Assistant

## Overview

Syntrix AI is a conversational AI business assistant that helps small businesses in Africa record sales and expenses through WhatsApp-style conversations, calculate profits automatically, provide business recommendations, and send reminder alerts.

## Features

✅ **User Authentication**
- User registration and login
- JWT-based authentication
- Secure password hashing with bcrypt

✅ **Business Management**
- Create and manage multiple businesses
- Support for different currencies
- Business type categorization

✅ **Sales & Expense Tracking**
- Record sales with item name, quantity, and amount
- Record expenses with item name, quantity, and amount
- Complete CRUD operations for both

✅ **AI-Powered Chat Interface**
- Natural language transaction extraction using Groq API (Llama 3.3 70B)
- Friendly, conversational responses
- Automatic transaction recording

✅ **Financial Analytics**
- Daily, weekly, and monthly profit calculations
- Revenue and expense summaries
- Profit margin analysis

✅ **Smart Recommendations**
- AI-generated business insights
- Actionable recommendations based on performance
- Trend analysis

✅ **Activity Tracking**
- Log all business transactions
- Track summary requests
- User activity history

✅ **Scheduled Reminders**
- Daily reminder alerts for inactive users
- Customizable notification timing

✅ **WhatsApp Integration**
- Generic provider interface for easy integration
- Support for Meta WhatsApp Cloud API
- Extensible for Twilio, WASender, and other providers

## Technology Stack

### Backend
- **Python 3.12** - Modern Python runtime
- **FastAPI** - High-performance async web framework
- **SQLAlchemy 2.0** - ORM with async support
- **Alembic** - Database migrations
- **PostgreSQL** - Production database
- **Pydantic v2** - Data validation
- **JWT** - Authentication tokens
- **APScheduler** - Background jobs

### AI/ML
- **Groq API** - Fast LLM inference
- **Llama 3.3 70B Versatile** - Large language model
- **JSON-based structured extraction** - Reliable data parsing

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Local development
- **Railway** - Cloud deployment ready

## Project Structure

```
syntrix/
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── auth.py
│   │   │   ├── business.py
│   │   │   ├── sales.py
│   │   │   ├── expenses.py
│   │   │   ├── chat.py
│   │   │   ├── summary.py
│   │   │   └── recommendations.py
│   │   └── routes.py
│   ├── ai/
│   │   ├── transaction_extractor.py
│   │   ├── reply_generator.py
│   │   └── recommendation_engine.py
│   ├── services/
│   │   ├── auth.py
│   │   ├── business.py
│   │   ├── sales.py
│   │   ├── expenses.py
│   │   └── summary.py
│   ├── repositories/
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── business.py
│   │   ├── sale.py
│   │   ├── expense.py
│   │   └── activity_log.py
│   ├── models/
│   │   ├── user.py
│   │   ├── business.py
│   │   ├── sale.py
│   │   ├── expense.py
│   │   └── activity_log.py
│   ├── schemas/
│   │   ├── user.py
│   │   ├── business.py
│   │   ├── sale.py
│   │   ├── expense.py
│   │   ├── summary.py
│   │   ├── chat.py
│   │   └── transaction.py
│   ├── integrations/
│   │   ├── whatsapp_base.py
│   │   ├── whatsapp_cloud.py
│   │   └── whatsapp_webhook.py
│   ├── jobs/
│   │   └── scheduler.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── database/
│   │   └── base.py
│   └── main.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_business.py
│   └── test_ai.py
├── alembic/
│   ├── versions/
│   │   └── 001_initial_migration.py
│   └── env.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── alembic.ini
├── .env.example
└── README.md
```

## Setup & Installation

### Prerequisites
- Python 3.12+
- PostgreSQL 14+
- Docker & Docker Compose (optional)
- Groq API Key

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/syntrixos-ai/syntrix.git
cd syntrix
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run database migrations**
```bash
alembic upgrade head
```

6. **Start the application**
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Docker Setup

1. **Build and run with Docker Compose**
```bash
docker-compose up -d
```

2. **Run migrations**
```bash
docker-compose exec app alembic upgrade head
```

3. **Access the application**
- API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/refresh` - Refresh access token

### Businesses
- `POST /api/v1/businesses` - Create business
- `GET /api/v1/businesses` - List user's businesses
- `GET /api/v1/businesses/{id}` - Get business details

### Sales
- `POST /api/v1/sales?business_id=1` - Record sale
- `GET /api/v1/sales?business_id=1` - List sales

### Expenses
- `POST /api/v1/expenses?business_id=1` - Record expense
- `GET /api/v1/expenses?business_id=1` - List expenses

### Chat & AI
- `POST /api/v1/chat` - Process chat message and extract transaction
- `GET /api/v1/summary?business_id=1&period=today` - Get business summary
- `GET /api/v1/recommendations?business_id=1&period=today` - Get recommendations

## Example Usage

### 1. Register User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123",
    "full_name": "John Doe"
  }'
```

### 2. Create Business
```bash
curl -X POST http://localhost:8000/api/v1/businesses \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John\'s Shoe Store",
    "business_type": "retail",
    "currency": "UGX"
  }'
```

### 3. Chat & Record Transaction
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "business_id": 1,
    "message": "Sold 3 shoes at 120000"
  }'
```

Response:
```json
{
  "business_id": 1,
  "user_message": "Sold 3 shoes at 120000",
  "assistant_message": "Done 👍\n\nI've recorded the sale of 3 shoes worth UGX 120,000.\n\nShoes seem to be selling well today.",
  "transaction_recorded": true,
  "transaction_type": "sale"
}
```

### 4. Get Summary
```bash
curl -X GET "http://localhost:8000/api/v1/summary?business_id=1&period=today" \
  -H "Authorization: Bearer <access_token>"
```

Response:
```json
{
  "period": "today",
  "total_revenue": 650000,
  "total_expenses": 180000,
  "profit": 470000,
  "profit_margin": 72.31,
  "transaction_count": 5,
  "message": "Your business is profitable today 📈"
}
```

## Testing

Run tests with pytest:
```bash
pytest tests/ -v
```

Run tests with coverage:
```bash
pytest tests/ --cov=app --cov-report=html
```

## Configuration

Key environment variables (see `.env.example`):

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/syntrix_db

# JWT
SECRET_KEY=your-super-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Groq API
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=llama-3.3-70b-versatile

# WhatsApp (for future integration)
WHATSAPP_WEBHOOK_TOKEN=your-webhook-token
WHATSAPP_PHONE_NUMBER_ID=your-phone-number-id
```

## Deployment

### Railway Deployment

1. **Connect your GitHub repository to Railway**
2. **Set environment variables in Railway dashboard**
3. **Deploy using Railway's Docker support**
4. **Railway will automatically run migrations on deploy**

### Production Checklist
- ✅ Change `SECRET_KEY` to a strong random value
- ✅ Set `DEBUG=False`
- ✅ Use PostgreSQL (not SQLite)
- ✅ Configure proper CORS origins
- ✅ Set up Groq API key
- ✅ Configure SMTP for email notifications
- ✅ Enable HTTPS/SSL
- ✅ Set up monitoring and logging

## API Documentation

Interactive API documentation available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: https://github.com/syntrixos-ai/syntrix/issues
- Email: support@syntrixai.com

## Roadmap

- [ ] Mobile app (React Native)
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Tax calculation features
- [ ] Invoice generation
- [ ] Payment integration (Stripe, M-Pesa)
- [ ] Inventory management
- [ ] Staff management
- [ ] Customer loyalty program

---

**Built with ❤️ for African SMEs**
