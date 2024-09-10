resource "google_storage_bucket" "output" {
  name     = "output-repo"
  location = "US"
}
