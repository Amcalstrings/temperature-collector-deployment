provider "aws" {
  region = var.aws_region
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "eks-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["${var.aws_region}a", "${var.aws_region}b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = true

  tags = {
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
    "kubernetes.io/role/internal-elb"           = "1"
  }
}

module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  version         = "~> 20.0"
  cluster_name    = var.cluster_name
  cluster_version = "1.29"
  cluster_endpoint_public_access = true
  subnet_ids      = module.vpc.private_subnets
  vpc_id          = module.vpc.vpc_id

  enable_irsa = true

  eks_managed_node_groups = {
    default = {
      instance_types = ["t3.medium"]
      min_size       = 2
      max_size       = 4
      desired_size   = 2
    }
  }

  access_entries = {
    admin-user = {
      principal_arn     = "arn:aws:iam::717279705656:user/Amcalstrings"
      kubernetes_groups = ["cluster-admin"]
      type              = "STANDARD"
    }
  }

  tags = {
    Environment = "dev"
    Project     = "temperature-data"
  }
}

resource "aws_ecr_repository" "scraper" {
  name = "temp-scraper"
  force_delete = true
}

resource "aws_ecr_repository" "consumer" {
  name = "kafka-consumer"
  force_delete = true
}

output "cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

