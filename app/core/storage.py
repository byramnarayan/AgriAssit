import os
import uuid
from pathlib import Path
from typing import Optional
from app.core.config import settings

LOCAL_STORAGE_DIR = Path("local_s3")

class StorageService:
    def __init__(self):
        self.client = None
        self.local_dir = LOCAL_STORAGE_DIR
        self.local_dir.mkdir(parents=True, exist_ok=True)
        
        # Try initializing Supabase client if configured
        if settings.SUPABASE_URL and settings.SUPABASE_SERVICE_KEY:
            try:
                from supabase import create_client
                self.client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
                print("✅ Supabase Storage initialized")
            except Exception as e:
                print(f"⚠️ Supabase Storage init warning ({e}). Using local_s3 storage fallback.")
        else:
            print("📁 Local S3 Storage active (local_s3/)")

    async def upload_file(self, bucket_name: str, file_data: bytes, file_name: str, content_type: str) -> Optional[str]:
        """
        Uploads a file to Supabase bucket or falls back to local storage (local_s3/).
        Returns the public URL or local URL path.
        """
        safe_filename = f"{uuid.uuid4().hex}_{file_name.replace(' ', '_')}"

        # 1. Attempt Supabase upload if available
        if self.client:
            try:
                response = self.client.storage.from_(bucket_name).upload(
                    path=safe_filename,
                    file=file_data,
                    file_options={"content-type": content_type}
                )
                public_url = self.client.storage.from_(bucket_name).get_public_url(safe_filename)
                return public_url
            except Exception as e:
                print(f"⚠️ Supabase Upload Error ({e}), falling back to local_s3 storage.")

        # 2. Local S3 Fallback
        try:
            bucket_dir = self.local_dir / bucket_name
            bucket_dir.mkdir(parents=True, exist_ok=True)
            file_path = bucket_dir / safe_filename
            
            with open(file_path, "wb") as f:
                f.write(file_data)
            
            local_url = f"/local_s3/{bucket_name}/{safe_filename}"
            print(f"💾 File stored in local_s3: {local_url}")
            return local_url
        except Exception as err:
            print(f"❌ Failed to store file locally: {err}")
            return None

storage_service = StorageService()
