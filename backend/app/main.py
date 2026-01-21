from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import select

from .db import Base, engine, get_db
from .models import Movie
from .schemas import MovieCreate, MovieOut

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Movie API", version="1.0.0")

# Streamlit(프론트)에서 호출할 수 있도록 CORS 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/movies", response_model=MovieOut, status_code=201)
def create_movie(payload: MovieCreate, db: Session = Depends(get_db)):
    movie = Movie(
        title=payload.title.strip(),
        release_date=payload.release_date,
        director=payload.director.strip(),
        genre=payload.genre.strip(),
        poster_url=str(payload.poster_url),
    )
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return MovieOut.model_validate(movie)

@app.get("/movies", response_model=list[MovieOut])
def list_movies(db: Session = Depends(get_db)):
    movies = db.scalars(select(Movie).order_by(Movie.created_at.desc())).all()
    # avg_rating은 현재 None
    return [MovieOut.model_validate(m) for m in movies]

@app.get("/movies/{movie_id}", response_model=MovieOut)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return MovieOut.model_validate(movie)

@app.delete("/movies/{movie_id}", status_code=204)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    db.delete(movie)
    db.commit()
    return None
