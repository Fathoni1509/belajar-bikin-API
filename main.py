# Fathoni Nur Habibi - L0123054

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os

app = FastAPI()

# halaman utama
@app.get("/")
def page_utama():
    return {"Halo Ini Adalah Halaman Utama"}

# upload file HTML atau txt maks 10MB
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    max_size = 10 * 1024 * 1024
    format_file = (".html", ".txt")

    if not file.filename.lower().endswith(format_file):
        raise HTTPException(status_code=400, detail="Hanya file .html atau .txt yang diperbolehkan")

    dest = os.path.join("uploads", file.filename)
    size = 0

    with open(dest, "wb") as f:
        while True:
            chunk = await file.read(1024 * 1024)
            if not chunk:
                break
            size += len(chunk)
            if size > max_size:
                f.close()
                os.remove(dest)
                raise HTTPException(status_code=413, detail="File terlalu besar. Maks 10MB")
            f.write(chunk)

    return {"filename": file.filename, "size": size}

# tampilkan semua file yang ada di folder uploads dengan format html atau txt
@app.get("/uploads-list")
def list_uploads():
    format_file = (".html", ".txt")
    files = [f for f in os.listdir("uploads") if f.endswith(format_file)]
    return {"uploads": files}

# tampilkan isi file pada folder uploads
@app.get("/upload/{filename}")
def get_page(filename: str):
    path = os.path.join("uploads", filename)

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Halaman tidak ditemukan")
    
    if filename.lower().endswith(".html"):
        media_type = "text/html"
    elif filename.lower().endswith(".txt"):
        media_type = "text/plain"
    else :
        raise HTTPException(status_code=400, detail="Cuma .html atau .txt yang bisa diakses")
    return FileResponse(path, media_type=media_type)