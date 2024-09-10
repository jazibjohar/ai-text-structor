resource "google_storage_bucket" "bucket" {
  name     = "ai-engine-code"
  location = "US"
}


resource "google_storage_bucket_object" "archive" {
  name   = "ai-engine-v4.zip"
  bucket = google_storage_bucket.bucket.name
  source = "../../package/build.zip"
}
