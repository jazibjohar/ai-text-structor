resource "google_cloudfunctions2_function" "function" {
  name        = "basic-summary-engine"
  description = "accepts content and builds a summary"
  location    = "us-central1"

  build_config {
    runtime     = "python310"
    entry_point = "summaries"
    source {
      storage_source {
        bucket = google_storage_bucket.bucket.name
        object = google_storage_bucket_object.archive.name
      }
    }
    environment_variables = {
      OPENAI_API_KEY     = var.openai_api_key
      GOOGLE_AI_API_KEY  = var.google_ai_api_key
      MISTRAL_AI_API_KEY = var.mistral_ai_api_key
      SUMMARY_BUCKET     = google_storage_bucket.summary-bucket.name
    }
  }

  service_config {
    max_instance_count = 100
    available_memory   = "1G"
    available_cpu      = "1"
    environment_variables = {
      OPENAI_API_KEY     = var.openai_api_key
      GOOGLE_AI_API_KEY  = var.google_ai_api_key
      MISTRAL_AI_API_KEY = var.mistral_ai_api_key
      SUMMARY_BUCKET     = google_storage_bucket.summary-bucket.name
    }
  }
}