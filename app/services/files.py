import io
from typing import List
import uuid
import boto3
from fastapi import UploadFile

session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net'
)

async def get_url(file: List[UploadFile]):
	uploded_files = []
	filenames = []
	for f in file:
		file_content = await f.read()
		f.filename = str(uuid.uuid4()) + ".jpg"
		filenames.append(f.filename)
		s3.upload_fileobj(
			Fileobj=io.BytesIO(file_content),
			Bucket='patriot-music',
			Key=f.filename
		)
		uploded_files.append({"filename": f.filename, "status": "uploaded"})
	async def get(img_url):
		return ["https://storage.yandexcloud.net/patriot-music/" + uploded_files[f]["filename"] for f in range(len(uploded_files))]
	return await get(filenames)
		
  
import uuid
import io
import os
from typing import List
from fastapi import UploadFile
import boto3

s3 = boto3.client('s3')

async def get_url_music(file: List[UploadFile]):
    uploaded_files = []
    
    for f in file:
        file_content = await f.read()
        _, ext = os.path.splitext(f.filename)
        new_filename = str(uuid.uuid4()) + ext  

        s3.upload_fileobj(
            Fileobj=io.BytesIO(file_content),
            Bucket='patriot-music',
            Key=new_filename
        )
        uploaded_files.append({"filename": new_filename, "status": "uploaded"})
    
    return [
        f"https://storage.yandexcloud.net/patriot-music/{file['filename']}"
        for file in uploaded_files
    ]

# # ## Из файла
# async def upload_file_to_s3(file: List[UploadFile]):
# 	uploded_files = []
# 	filenames = []
# 	file_urls = []
# 	for f in file:
# 		file_content = await f.read()
# 		f.filename = str(uuid.uuid4()) + ".jpg"
# 		filenames.append(f.filename)
# 		s3.upload_fileobj(
# 			Fileobj=io.BytesIO(file_content),
# 			Bucket='patriot-music',
# 			Key=f.filename
# 		)
# 		uploded_files.append({"filename": f.filename, "status": "uploaded"})
# 	async def get_url_from_s3(files: List[str]):
# 		for f in files:
# 			url = s3.generate_presigned_url(
# 				ClientMethod='get_object',
# 				Params={'Bucket': 'patriot-music', 'Key': f}
# 			)
# 			file_urls.append({"filename": f, "url": url})
# 		return file_urls		
# 	return await get_url_from_s3(filenames)