from django.urls import path
from .views import UploadCSVView, HistoryView,ReportView,HistoryDetailView

urlpatterns = [
    path("upload/", UploadCSVView.as_view(), name="upload-csv"),
    path("history/", HistoryView.as_view(), name="history"),
    path("report/<int:dataset_id>/",ReportView.as_view(),name="report"),
    path("history/<int:id>/", HistoryDetailView.as_view()),
]
