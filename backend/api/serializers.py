from rest_framework import serializers
from .models import Dataset

class DatasetDetailSerializer(serializers.ModelSerializer):
    preview = serializers.SerializerMethodField()

    class Meta:
        model = Dataset
        fields = ["id", "summary", "preview"]

    def get_preview(self, obj):
        """
        Return preview rows for this dataset.
        Must match the same preview returned during upload.
        """
        import pandas as pd

        df = pd.read_csv(obj.file.path)
        return df.head(20).to_dict(orient="records")