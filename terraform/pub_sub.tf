resource "google_pubsub_topic" "topic" {
  name = "ai-engine-topic"

  message_retention_duration = "86600s"
}