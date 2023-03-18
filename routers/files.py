from fastapi import UploadFile, APIRouter
from service.ipfs import add_files
from typing import List


router = APIRouter(
    prefix="/files",
    tags=["files"]
)


# @router.post("/uploadfile/")
# async def create_upload_file(file: UploadFile):
#     file_dict = {
#         file.filename: file.file
#     }

#     return {"filename": file.filename}


@router.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile]):
    files_dict: dict = {}
    for f in files:
        files_dict[f.filename] = f.file
    # file_list = [{'path': f.filename, 'content': f.file} for f in files]
    df = add_files(files_dict)
    cid = df.loc[df['Name'] == '', 'Hash'].values[0]
    return {"cid": cid}
