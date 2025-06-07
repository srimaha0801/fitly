# Fitly - Fitness Class Booking API

**Fitly** is a simple fitness class booking system built using Django and Django REST Framework. 
Users can view available fitness classes, book a slot, and view their bookings. Admins can manage classes and clients via the admin panel.

---

## Features

- View available fitness classes
- Book a class by providing name and email
- Prevents overbooking and duplicate bookings
- Admin panel for managing classes and clients
- Validations for class availability and client data
- Unit tests for booking functionality

---

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/srimaha0801/fitly.git
cd fitly
```

### 2. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create a Superuser (for admin panel)

```bash
python manage.py createsuperuser
```

Follow the prompts to set username, email, and password.

### 4. Run the Server

```bash
python manage.py runserver
```

Server runs at: [http://127.0.0.1:8000]

---

## API Endpoints

### View All Classes

```bash
curl -X GET http://127.0.0.1:8000/classes/
```

Returns a list of available fitness classes.

---

### Book a Class

```bash
curl -X POST http://127.0.0.1:8000/book/ \
  -H "Content-Type: application/json" \
  -d '{
    "class_id": 1,
    "client_name": "Megna",
    "client_email": "megna@megna.com"
  }'
```

Validates and books the user into the class if slots are available.

---

### View Client Bookings

```bash
curl -X GET http://127.0.0.1:8000/bookings/?email=john@example.com
```

Returns a list of classes the user is enrolled in.

---

## Admin Panel

To add or edit fitness classes manually:

1. Go to: [http://127.0.0.1:8000/admin]
2. Log in with the superuser credentials you created
3. Use the admin interface to add/edit:
   - Fitness classes (`ClassList`)

---

## Project Structure (Brief)

```
fitly/
├── bookings/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── booking_test.py
├── fitly/
│   ├── settings.py
│   ├── urls.py
```

---

## 📌 Notes

- Duplicate enrollments are blocked
- Overbooking is prevented
- Email is treated as a unique identifier for clients