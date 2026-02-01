import os
import tempfile
import pandas as pd
import matplotlib.pyplot as plt

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from .models import Dataset
from .serializers import DatasetDetailSerializer

def generate_type_distribution_chart(type_distribution):
    labels = list(type_distribution.keys())
    values = list(type_distribution.values())

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(labels, values)
    ax.set_title("Equipment Type Distribution")
    ax.set_xlabel("Equipment Type")
    ax.set_ylabel("Count")
    plt.xticks(rotation=30)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    plt.tight_layout()
    plt.savefig(temp_file.name)
    plt.close(fig)

    return temp_file.name

class UploadCSVView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get("file")

        if not file:
            return Response({"error": "No file uploaded"}, status=400)

        if not file.name.endswith(".csv"):
            return Response({"error": "Only CSV files allowed"}, status=400)

        try:
            df = pd.read_csv(file)

            required_columns = [
                "Equipment Name", "Type", "Flowrate", "Pressure", "Temperature"
            ]
            for col in required_columns:
                if col not in df.columns:
                    return Response(
                        {"error": f"Missing column: {col}"}, status=400
                    )

            summary = {
                "total_count": len(df),
                "avg_flowrate": round(df["Flowrate"].mean(), 2),
                "avg_pressure": round(df["Pressure"].mean(), 2),
                "avg_temperature": round(df["Temperature"].mean(), 2),
                "type_distribution": df["Type"].value_counts().to_dict(),
            }

            dataset = Dataset.objects.create(
                file=file,
                summary=summary
            )

            # Keep only last 5 datasets
            datasets = Dataset.objects.order_by("-uploaded_at")
            if datasets.count() > 5:
                for old in datasets[5:]:
                    old.file.delete()
                    old.delete()

            preview = df.head(20).to_dict(orient="records")

            return Response(
                {
                    "id": dataset.id,
                    "summary": summary,
                    "preview": preview,
                },
                status=200,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=500)

class HistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        datasets = Dataset.objects.order_by("-uploaded_at")[:5]

        data = []
        for d in datasets:
            data.append(
                {
                    "id": d.id,
                    "filename": os.path.basename(d.file.name),
                    "uploaded_at": d.uploaded_at,
                    "summary": d.summary,
                }
            )

        return Response(data, status=200)

class HistoryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        dataset = get_object_or_404(Dataset, id=id)
        serializer = DatasetDetailSerializer(dataset)
        return Response(serializer.data)

class ReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, dataset_id):
        dataset = get_object_or_404(Dataset, id=dataset_id)
        summary = dataset.summary

        response = HttpResponse(content_type="application/pdf")
        response[
            "Content-Disposition"
        ] = f'attachment; filename="report_{dataset_id}.pdf"'

        c = canvas.Canvas(response, pagesize=A4)
        width, height = A4
        y = height - 50

        # Title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y, "Chemical Equipment Report")
        y -= 40

        # Metadata
        c.setFont("Helvetica", 11)
        c.drawString(50, y, f"File: {os.path.basename(dataset.file.name)}")
        y -= 20
        c.drawString(50, y, f"Uploaded at: {dataset.uploaded_at}")
        y -= 30

        # Summary
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Summary Statistics")
        y -= 20

        c.setFont("Helvetica", 11)
        c.drawString(50, y, f"Total Equipment: {summary['total_count']}")
        y -= 18
        c.drawString(50, y, f"Average Flowrate: {summary['avg_flowrate']}")
        y -= 18
        c.drawString(50, y, f"Average Pressure: {summary['avg_pressure']}")
        y -= 18
        c.drawString(50, y, f"Average Temperature: {summary['avg_temperature']}")
        y -= 30

        # Chart
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Equipment Type Distribution")
        y -= 30

        chart_path = generate_type_distribution_chart(
            summary["type_distribution"]
        )

        c.drawImage(chart_path, 50, y - 250, width=400, height=250)
        y -= 280

        os.remove(chart_path)

        c.showPage()
        c.save()

        return response