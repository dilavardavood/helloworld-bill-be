# SecureBill Backend

Flask + MySQL backend for SecureBill.

## Requirements
- Python 3.x
- MySQL Server

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configuration**
   - Copy `.env.example` to `.env`.
   - Update `DATABASE_URL` with your MySQL credentials.
   ```
   DATABASE_URL=mysql+pymysql://root:password@localhost/securebill_db
   ```

3. **Database Setup**
   - Create the database `securebill_db` in MySQL if it doesn't exist.
   - Run migrations to create tables:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

4. **Run Server**
   ```bash
   python run.py
   ```
   Server will run on `http://localhost:5000`.

## Verification
Run the verification script to test the APIs:
```bash
python verify_api.py
```

## API Modules
- Categories: `/api/categories`
- Products: `/api/products`
- Invoices: `/api/invoices`
- Company: `/api/company`
- Users: `/api/users`
