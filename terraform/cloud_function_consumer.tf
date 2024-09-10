

resource "google_cloudfunctions2_function" "function-pubsub" {
  name        = "basic-summary-engine-consumer"
  description = "accepts content and builds a summary from pub sub"
  location    = "us-central1"

  build_config {
    runtime     = "python310"
    entry_point = "summaries_consumer"
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
    available_memory   = "512M"
    environment_variables = {
      OPENAI_API_KEY     = var.openai_api_key
      GOOGLE_AI_API_KEY  = var.google_ai_api_key
      MISTRAL_AI_API_KEY = var.mistral_ai_api_key
      SUMMARY_BUCKET     = google_storage_bucket.summary-bucket.name
    }
  }
  event_trigger {
    event_type   = "google.cloud.pubsub.topic.v1.messagePublished"
    pubsub_topic = google_pubsub_topic.topic.id
  }
}