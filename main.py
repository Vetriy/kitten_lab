from fastapi import FastAPI, HTTPException, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Kitten(Base):
    __tablename__ = "kittens"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    color = Column(String, nullable=False)
    breed = Column(String, nullable=False)


Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/kittens/")
def create_kitten(
    name: str,
    age: int,
    color: str,
    breed: str,
    db: Session = Depends(get_db)
):
    kitten = Kitten(name=name, age=age, color=color, breed=breed)
    db.add(kitten)
    db.commit()
    db.refresh(kitten)
    return {
        "id": kitten.id,
        "name": kitten.name,
        "age": kitten.age,
        "color": kitten.color,
        "breed": kitten.breed,
    }


@app.get("/kittens/")
def read_kittens(db: Session = Depends(get_db)):
    kittens = db.query(Kitten).all()
    return [
        {
            "id": k.id,
            "name": k.name,
            "age": k.age,
            "color": k.color,
            "breed": k.breed,
        }
        for k in kittens
    ]


@app.get("/kittens/{kitten_id}")
def read_kitten(kitten_id: int, db: Session = Depends(get_db)):
    k = db.get(Kitten, kitten_id)
    if not k:
        raise HTTPException(status_code=404, detail="Kitten not found")
    return {
        "id": k.id,
        "name": k.name,
        "age": k.age,
        "color": k.color,
        "breed": k.breed,
    }


@app.put("/kittens/{kitten_id}")
def update_kitten(
    kitten_id: int,
    name: str,
    age: int,
    color: str,
    breed: str,
    db: Session = Depends(get_db)
):
    k = db.get(Kitten, kitten_id)
    if not k:
        raise HTTPException(status_code=404, detail="Kitten not found")

    k.name = name
    k.age = age
    k.color = color
    k.breed = breed
    db.commit()
    db.refresh(k)

    return {
        "id": k.id,
        "name": k.name,
        "age": k.age,
        "color": k.color,
        "breed": k.breed,
    }


@app.delete("/kittens/{kitten_id}")
def delete_kitten(kitten_id: int, db: Session = Depends(get_db)):
    k = db.get(Kitten, kitten_id)
    if not k:
        raise HTTPException(status_code=404, detail="Kitten not found")

    db.delete(k)
    db.commit()
    return {"ok": True}


@app.get("/health")
def health():
    return {"status": "healthy", "service": "kitten-api"}



@app.get("/", response_class=HTMLResponse)
def home(db: Session = Depends(get_db)):
    kittens = db.query(Kitten).all()

    html = """
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Kitten Manager</title>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: #fff;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 30px;
}

.container {
    width: 100%;
    max-width: 900px;
}

.card {
    background: rgba(255,255,255,0.06);
    border-radius: 20px;
    padding: 30px;
    backdrop-filter: blur(12px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
}

h1 {
    font-size: 32px;
    margin-bottom: 20px;
}

.form {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    margin-bottom: 25px;
}

input {
    padding: 12px;
    border-radius: 10px;
    border: none;
    background: rgba(255,255,255,0.1);
    color: #fff;
}

input::placeholder {
    color: rgba(255,255,255,0.6);
}

.main-btn {
    grid-column: span 4;
    padding: 14px;
    border: none;
    border-radius: 12px;
    background: #4ade80;
    color: #111;
    font-weight: bold;
    cursor: pointer;
}

.list {
    display: grid;
    gap: 12px;
}

.item {
    background: rgba(255,255,255,0.08);
    padding: 15px;
    border-radius: 12px;
}

.view-block {
    font-size: 16px;
    line-height: 1.5;
}

.edit-block {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
}

.actions {
    margin-top: 12px;
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}

.delete {
    background: #ef4444;
    color: white;
    padding: 8px 12px;
    border-radius: 8px;
    text-decoration: none;
}

.edit {
    background: #3b82f6;
    color: white;
    padding: 8px 12px;
    border-radius: 8px;
    text-decoration: none;
}

.save {
    background: #22c55e;
    color: #111;
    padding: 8px 12px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
}

.cancel {
    background: #64748b;
    color: white;
    padding: 8px 12px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
}

.hidden {
    display: none;
}

.empty {
    opacity: 0.7;
    text-align: center;
    padding: 20px;
}
</style>
</head>

<body>
<div class="container">
<div class="card">

<h1>Kitten Manager</h1>

<form class="form" action="/add" method="post">
    <input name="name" placeholder="Имя" required>
    <input name="age" type="number" placeholder="Возраст" min="0" required>
    <input name="color" placeholder="Цвет" required>
    <input name="breed" placeholder="Порода" required>
    <button class="main-btn" type="submit">Добавить котёнка</button>
</form>

<div class="list">
"""

    if not kittens:
        html += '<div class="empty">Пока нет котят</div>'

    for k in kittens:
        html += f"""
<div class="item">
    <form action="/update/{k.id}" method="post">
        <div class="view-block view-{k.id}">
            <b>{k.name}</b> — {k.age} — {k.color} — {k.breed}
        </div>

        <div class="edit-block edit-{k.id} hidden">
            <input name="name" value="{k.name}" required>
            <input name="age" type="number" value="{k.age}" min="0" required>
            <input name="color" value="{k.color}" required>
            <input name="breed" value="{k.breed}" required>
        </div>

        <div class="actions">
            <a class="delete" href="/delete/{k.id}">Удалить</a>
            <a class="edit edit-btn-{k.id}" href="#" onclick="editKitten({k.id}); return false;">Изменить</a>
            <button class="save hidden save-btn-{k.id}" type="submit">Сохранить</button>
            <button class="cancel hidden cancel-btn-{k.id}" type="button" onclick="cancelEdit({k.id})">Отмена</button>
        </div>
    </form>
</div>
"""

    html += """
</div>
</div>
</div>

<script>
function editKitten(id) {
    document.querySelector(".view-" + id).classList.add("hidden");
    document.querySelector(".edit-" + id).classList.remove("hidden");
    document.querySelector(".edit-btn-" + id).classList.add("hidden");
    document.querySelector(".save-btn-" + id).classList.remove("hidden");
    document.querySelector(".cancel-btn-" + id).classList.remove("hidden");
}

function cancelEdit(id) {
    document.querySelector(".view-" + id).classList.remove("hidden");
    document.querySelector(".edit-" + id).classList.add("hidden");
    document.querySelector(".edit-btn-" + id).classList.remove("hidden");
    document.querySelector(".save-btn-" + id).classList.add("hidden");
    document.querySelector(".cancel-btn-" + id).classList.add("hidden");
}
</script>

</body>
</html>
"""
    return html


@app.post("/add")
def add(
    name: str = Form(...),
    age: int = Form(...),
    color: str = Form(...),
    breed: str = Form(...),
    db: Session = Depends(get_db)
):
    kitten = Kitten(name=name, age=age, color=color, breed=breed)
    db.add(kitten)
    db.commit()
    return RedirectResponse("/", status_code=303)


@app.get("/delete/{kitten_id}")
def delete_gui(kitten_id: int, db: Session = Depends(get_db)):
    k = db.get(Kitten, kitten_id)
    if k:
        db.delete(k)
        db.commit()
    return RedirectResponse("/", status_code=303)


@app.post("/update/{kitten_id}")
def update_gui(
    kitten_id: int,
    name: str = Form(...),
    age: int = Form(...),
    color: str = Form(...),
    breed: str = Form(...),
    db: Session = Depends(get_db)
):
    k = db.get(Kitten, kitten_id)
    if not k:
        raise HTTPException(status_code=404, detail="Kitten not found")

    k.name = name
    k.age = age
    k.color = color
    k.breed = breed
    db.commit()
    return RedirectResponse("/", status_code=303)