terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}

provider "local" {}

resource "local_file" "ndsa" {
  filename = "hello.txt"
  content  = "NDSA Zero Trust SOC Project"
}
