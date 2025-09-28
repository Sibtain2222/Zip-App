from django.shortcuts import render
from django.http import HttpResponse
from .serializer import FolderSerializer 
from rest_framework.views import APIView

from django.http import FileResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import zipfile ,tempfile,uuid
import os 
import tkinter as tk 
from tkinter import filedialog
from pathlib import Path
# Create your views here.

# Store compressed files in memory for later download
TEMP_ZIPS = {}
class FolderView( APIView):
     def post(self, request):
        uploaded_files = request.FILES.getlist("files")
        if not uploaded_files:
            return Response({"error": "No files uploaded"}, status=400)

        # Save uploaded files to a temp folder
        with tempfile.TemporaryDirectory() as tmpdirname:
            for f in uploaded_files:
                file_path = os.path.join(tmpdirname, f.name)
                with open(file_path, "wb+") as dest:
                    for chunk in f.chunks():
                        dest.write(chunk)

            # Compress folder
            # archive_path = tmpdirname + ".zip"
            # with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            #     for root, _, files in os.walk(tmpdirname):
            #         for file in files:
            #             file_path = os.path.join(root, file)
            #             arcname = os.path.relpath(file_path, start=tmpdirname)
            #             zipf.write(file_path, arcname)
              # Create zip
            archive_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.zip")
            with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(tmpdirname):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, start=tmpdirname)
                        zipf.write(file_path, arcname)

            # Store zip path in dictionary with unique ID
            folder_id = str(uuid.uuid4())
            TEMP_ZIPS[folder_id] = archive_path

            
            def convert_bytes(num):

                for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
                    if num < 1024.0:
                        return "%3.1f %s" % (num, x)
                    num /= 1024.0


            def folder_size(folder):
                total=0
                for file in Path(folder).rglob('*'):
                    try:
                        if file.is_file():
                            total+=file.stat().st_size
                    except FileNotFoundError:
                      continue
                return convert_bytes(total)
            
        
            original_size = f"{folder_size(tmpdirname)}"  # e.g. "4.2 MB"
            compressed_size = f"{convert_bytes(os.path.getsize(archive_path))}"
        



        return Response({ "compressed_size" : compressed_size  , "original_size" : original_size ,"folder_id": folder_id,
                          })
     
class FolderDownloadView(APIView):
    def get(self, request, folder_id):
        zip_path = TEMP_ZIPS.get(folder_id)
        if not zip_path or not os.path.exists(zip_path):
            return Response({"error": "File not found"}, status=404)

        return FileResponse(
            open(zip_path, "rb"),
            as_attachment=True,
            filename="compressed_folder.zip"
        )

     

class fileView(APIView):
    def post(self, request):
        upload_file= request.FILES.get("file")
        if not upload_file:
            return Response({"error": "No file uploaded"}, status=400)
        with tempfile.TemporaryDirectory() as tmpdirname:
            file_path = os.path.join(tmpdirname, upload_file.name)
            with open(file_path, "wb+") as dest:
                for chunk in upload_file.chunks():
                    dest.write(chunk)

            # # Compress file
            # archive_path = file_path + ".zip"

            # with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            #     zipf.write(file_path, os.path.basename(file_path))
            archive_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.zip")
            with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(file_path, arcname=upload_file.name)

            # Store zip path in dictionary with unique ID
            file_id = str(uuid.uuid4())
            TEMP_ZIPS[file_id] = archive_path
            def convert_bytes(num):

                for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
                    if num < 1024.0:
                        return "%3.1f %s" % (num, x)
                    num /= 1024.0


            def file_size(file_path):
                if os.path.isfile(file_path):
                    file_info = os.stat(file_path)
                    return convert_bytes(file_info.st_size)
            if file_path: 
                orignal_size=(f"{file_size(file_path)}")
            compressed_size = f"{file_size(archive_path)}"
            # compressed_size = os.path.getsize(archive_path) / (1024 * 1024) # in MB 
        return Response({ "file_id": file_id,"compressed_size": compressed_size , "original_size": orignal_size})





class fileDownloadView(APIView):
    def get(self,request,file_id):
        zip_path=TEMP_ZIPS.get(file_id)
        if not zip_path or not os.path.exists(zip_path):
            return Response({"error": "File not found"}, status=404)
        return (FileResponse(
            open(zip_path, "rb"),
            as_attachment=True,
            filename="compressed_file.zip"
        ))