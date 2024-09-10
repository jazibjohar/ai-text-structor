variable "openai_api_key" {
  type        = string
  sensitive   = true
  description = "OpenAI API key"
}

variable "google_ai_api_key" {
  type        = string
  sensitive   = true
  description = "Google AI API key"
}


variable "mistral_ai_api_key" {
  type        = string
  sensitive   = true
  description = "Mistral AI API key"
}