from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()
class User(BaseModel):
    name: str
    email: str
    password: str
    role: str   
class Comment(BaseModel):
    author: str
    text: str
class Document(BaseModel):
    id: int
    title: str
    description: str
    filename: str
    uploaded_by: str
    status: str = "Pending"
    comments: List[Comment] = []
users = {}
documents = {}
doc_id_counter = 1
@app.post("/register")
def register(user: User):
    if user.email in users:
        raise HTTPException(400, "User already exists")

    users[user.email] = user
    return {"message": "User registered"}
@app.post("/login")
def login(email: str, password: str):
    user = users.get(email)

    if not user or user.password != password:
        raise HTTPException(401, "Invalid credentials")

    return {"message": f"Welcome {user.name}", "role": user.role}
@app.post("/documents")
def upload_doc(doc: Document):
    global doc_id_counter

    doc.id = doc_id_counter
    doc_id_counter += 1

    documents[doc.id] = doc
    return {"message": "Document uploaded", "id": doc.id}
@app.get("/documents")
def list_docs():
    return list(documents.values())
@app.get("/documents/{doc_id}")
def get_doc(doc_id: int):
    doc = documents.get(doc_id)

    if not doc:
        raise HTTPException(404, "Document not found")

    return doc
@app.put("/documents/{doc_id}/status")
def update_status(doc_id: int, status: str):
    doc = documents.get(doc_id)

    if not doc:
        raise HTTPException(404, "Document not found")

    if status not in ["Pending", "Approved", "Changes Requested"]:
        raise HTTPException(400, "Invalid status")

    doc.status = status
    return {"message": "Status updated"}
@app.post("/documents/{doc_id}/comment")
def add_comment(doc_id: int, comment: Comment):
    doc = documents.get(doc_id)

    if not doc:
        raise HTTPException(404, "Document not found")

    doc.comments.append(comment)
    return {"message": "Comment added"}
@app.get("/report")
def report():
    pending = sum(1 for d in documents.values() if d.status == "Pending")
    approved = sum(1 for d in documents.values() if d.status == "Approved")
    changes = sum(1 for d in documents.values() if d.status == "Changes Requested")

    return {
        "total_docs": len(documents),
        "pending": pending,
        "approved": approved,
        "changes_requested": changes,
        "total_users": len(users)
    }
