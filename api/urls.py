from django.urls import path , include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from api.views import FolderView , fileView , FolderDownloadView , fileDownloadView



urlpatterns = [
    path('folder', FolderView.as_view(), name='folder'),
    path('file', fileView.as_view(), name='file'),
    path("folder/download/<str:folder_id>", FolderDownloadView.as_view(), name="folder_download"),
    path("file/download/<str:file_id>", fileDownloadView.as_view(), name="file_download"),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]