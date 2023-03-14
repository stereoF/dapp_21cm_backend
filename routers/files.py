from fastapi import UploadFile, APIRouter


router = APIRouter(
    prefix="/files",
    tags=["files"]
)

@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    print(file.filename)
    return {"filename": file.filename}


@router.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}
