# 🧩 Identity Reconciliation Web Service

A **Flask-based microservice** to identify and link duplicate contact records (based on email and phone number) into a **single consolidated identity** using primary/secondary contact logic.

---

## 🚀 API Endpoint

### `POST /identify`

Reconciles identities by email and/or phone number, and returns linked contact records.

---

## 📥 Sample Request

```json
POST /identify
Content-Type: application/json

{
  "email": "doc@zamazon.com",
  "phoneNumber": "9876543210"
}

📤 Sample Response

{
  "primaryContactId": 1,
  "emails": ["doc@zamazon.com"],
  "phoneNumbers": ["9876543210"],
  "secondaryContactIds": []
}
