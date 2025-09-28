from rest_framework import serializers

class FolderSerializer(serializers.Serializer):
    Folder = serializers.FileField()
    file= serializers.FileField()

# --- IGNORE ---