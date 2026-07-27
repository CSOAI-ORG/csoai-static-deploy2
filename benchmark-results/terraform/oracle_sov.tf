# Oracle Cloud Free Tier — SOV Oracle Terraform Config
# terraform init && terraform plan && terraform apply

terraform {
  required_providers {
    oci = {
      source  = "oracle/oci"
      version = "~> 5.0"
    }
  }
}

variable "compartment_ocid" {
  description = "Oracle Cloud compartment OCID"
  type        = string
}

variable "ssh_public_key" {
  description = "SSH public key for instance access"
  type        = string
  default     = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKGlYrEF0ShI63CdOgcJDN9yxcapdBm7h2a97QcJtQVP sovereign-council-deployment"
}

# Always Free Ampere A1 Instance
resource "oci_core_instance" "sov_oracle" {
  compartment_id      = var.compartment_ocid
  availability_domain = data.oci_identity_availability_domains.ads.availability_domains[0].name
  display_name        = "sov-oracle"
  shape               = "VM.Standard.A1.Flex"

  shape_config {
    ocpus       = 4
    memory_in_gbs = 24
  }

  source_details {
    source_type = "image"
    source_id   = data.oci_core_images.ubuntu.images[0].id
  }

  create_vnic_details {
    subnet_id        = oci_core_subnet.sov_subnet.id
    assign_public_ip = true
  }

  metadata = {
    ssh_authorized_keys = var.ssh_public_key
    user_data = base64encode(file("${path.module}/oracle_setup.sh"))
  }
}

# 200GB Block Volume (Always Free)
resource "oci_core_volume" "sov_storage" {
  compartment_id      = var.compartment_ocid
  availability_domain = data.oci_identity_availability_domains.ads.availability_domains[0].name
  display_name        = "sov-oracle-storage"
  size_in_gbs         = 200
}

resource "oci_core_volume_attachment" "sov_attachment" {
  instance_id = oci_core_instance.sov_oracle.id
  volume_id   = oci_core_volume.sov_storage.id
  attachment_type = "paravirtualized"
}

# VCN + Subnet
resource "oci_core_vcn" "sov_vcn" {
  compartment_id = var.compartment_ocid
  display_name   = "sov-oracle-vcn"
  cidr_block     = "10.0.0.0/16"
}

resource "oci_core_subnet" "sov_subnet" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.sov_vcn.id
  display_name   = "sov-oracle-subnet"
  cidr_block     = "10.0.1.0/24"
}

# Security List — SSH + SOV API
resource "oci_core_security_list" "sov_security" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.sov_vcn.id
  display_name   = "sov-oracle-security"

  ingress_security_rules {
    protocol = "6"
    source   = "0.0.0.0/0"
    tcp_options {
      min = 22
      max = 22
    }
  }

  ingress_security_rules {
    protocol = "6"
    source   = "0.0.0.0/0"
    tcp_options {
      min = 8766
      max = 8766
    }
  }

  egress_security_rules {
    protocol    = "all"
    destination = "0.0.0.0/0"
  }
}

data "oci_identity_availability_domains" "ads" {
  compartment_id = var.compartment_ocid
}

data "oci_core_images" "ubuntu" {
  compartment_id = var.compartment_ocid
  filter {
    name   = "operating-system"
    values = ["Canonical Ubuntu"]
  }
  filter {
    name   = "operating-system-version"
    values = ["22.04"]
  }
  filter {
    name   = "architecture"
    values = ["aarch64"]
  }
}

output "instance_ip" {
  value = oci_core_instance.sov_oracle.public_ip
}

output "instance_ocid" {
  value = oci_core_instance.sov_oracle.id
}
