# 📄 Client Document Approval System (FastAPI)

## 🚀 Overview

The **Client Document Approval System** is a backend API built using **FastAPI** that allows users to upload, review, approve, and manage documents efficiently.

This system simulates a real-world workflow where:

* Admins upload documents
* Clients review them
* Feedback is given via comments
* Documents go through an approval lifecycle

---

## 🧠 How It Works

The system is built around three main entities:

### 👤 Users

* Can register and login
* Have roles: `admin` or `client`

### 📄 Documents

* Uploaded by users
* Contain metadata like:

  * title
  * description
  * filename
  * status

### 💬 Comments

* Users can add feedback to documents
* Stored inside each document

---

## ⚙️ Features

### 🔐 Authentication

* User registration (`/register`)
* User login (`/login`)

### 📂 Document Management

* Upload document (`/documents`)
* View all documents (`/documents`)
* View single document (`/documents/{doc_id}`)

### 🔄 Workflow System

* Update document status:

  * Pending
  * Approved
  * Changes Requested

### 💬 Comment System

* Add comments to documents

### 📊 Reporting

* Get system stats:

  * Total documents
  * Status distribution
  * Total users

---

## 🧩 API Endpoints

| Method | Endpoint                  | Description          |
| ------ | ------------------------- | -------------------- |
| POST   | `/register`               | Register a user      |
| POST   | `/login`                  | Login user           |
| POST   | `/documents`              | Upload document      |
| GET    | `/documents`              | List all documents   |
| GET    | `/documents/{id}`         | Get document details |
| PUT    | `/documents/{id}/status`  | Update status        |
| POST   | `/documents/{id}/comment` | Add comment          |
| GET    | `/report`                 | Get summary report   |

---

## 🏗️ Tech Stack

* **FastAPI** ⚡
* **Pydantic** (data validation)
* **Python** 🐍
* In-memory storage (for simplicity)

---

## 📌 Project Structure

* `User` → handles user data
* `Document` → main entity
* `Comment` → feedback system
* `users` → in-memory user database
* `documents` → in-memory document store

---

## 🔥 Key Concepts Demonstrated

* REST API design
* Backend architecture
* Data modeling with Pydantic
* CRUD operations
* Role-based workflow
* State management (Pending → Approved → Changes Requested)

---

## ⚠️ Limitations (Current Version)

* No database (data resets on restart)
* No authentication tokens (JWT not implemented)
* Passwords stored in plain text (not secure)
* No file upload handling (only metadata stored)

---

## 🚀 Future Improvements

This project can be extended into a production-level system by adding:

### 🔐 Security

* JWT authentication
* Password hashing

### 🗄️ Database

* PostgreSQL / MongoDB integration
* Persistent storage

### 📁 File Handling

* Actual file upload support
* Cloud storage (AWS S3)

### 🤖 AI Integration (NEXT LEVEL 🔥)

* Document auto-summary using LLM
* Smart review suggestions
* AI-based approval recommendations

## 💡 Learning Outcome

This project helped in understanding:

* How real backend systems are designed
* How workflows are implemented
* How APIs communicate with clients
* How scalable systems can be structured

---

## ⭐ Final Thought

> This is not just a CRUD app — it’s a **workflow system**, which is exactly what real-world companies build.

---
