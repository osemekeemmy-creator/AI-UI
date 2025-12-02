from fastapi import APIRouter, File, UploadFile, Depends, BackgroundTasks
from pdf2image import convert_from_bytes
from PIL import Image
import pytesseract
from io import BytesIO
from app.utils.splitter import split_questions
from app.core.vector import upsert_questions
from app.core.security import get_api_key

router = APIRouter()

def enhance_image(img: Image.Image) -> Image.Image:
    img = img.convert("L")
    from PIL import ImageEnhance, ImageFilter
    img = ImageEnhance.Contrast(img).enhance(2.5)
    img = ImageEnhance.Sharpness(img).enhance(2.0)
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    return img

async def process_file(content: bytes, filename: str, subject: str, year: int):
    images = []
    if filename.lower().endswith(".pdf"):
        images = convert_from_bytes(content, dpi=300)
    else:
        images = [Image.open(BytesIO(content))]

    all_text = ""
    for img in images:
        text = pytesseract.image_to_string(enhance_image(img), lang="eng")
        all_text += text + "\n\n"

    questions = split_questions(all_text)
    await upsert_questions(questions, subject, year, filename)

@router.post("/ingest")
async def ingest(
    file: UploadFile = File(...),
    subject: str = "General",
    year: int = 2024,
    background: BackgroundTasks = BackgroundTasks(),
    _: str = Depends(get_api_key)
):
    content = await file.read()
    background.add_task(process_file, content, file.filename, subject, year)
    return {"status": "queued", "file": file.filename, "questions": "processing..."}
