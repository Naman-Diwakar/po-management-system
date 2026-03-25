# 🧾 Purchase Order (PO) Management System

## 🚀 Overview

This project is a full-stack Purchase Order Management System built using FastAPI, PostgreSQL, and JavaScript.

It allows users to manage vendors, products, and create purchase orders with multiple items and automatic tax calculation.

---

## 🛠 Tech Stack

* Backend: FastAPI (Python)
* Database: PostgreSQL
* Frontend: HTML, CSS, Bootstrap, JavaScript

---

## ✨ Features

* Create & view Vendors
* Create & view Products
* Create Purchase Orders with multiple items
* Automatic total calculation with 5% tax
* Dynamic frontend (add/remove product rows)
* Live total calculation in UI

---

## ⚙️ How to Run

### Backend

```bash
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
python -m http.server 5500
```

Open:
http://127.0.0.1:5500

---

## 🧠 Database Design

* Vendors → Stores supplier info
* Products → Stores product details
* PurchaseOrders → Stores order summary
* PurchaseOrderItems → Stores products inside each order

---

## 🎯 Key Learnings

* REST API development
* Database relationships (Foreign Keys)
* Frontend-backend integration
* Real-time UI updates

---

## 📌 Future Improvements

* Authentication (JWT / OAuth)
* AI-based product description generator
* Notifications for order status

---
