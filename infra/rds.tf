resource "aws_db_subnet_group" "default" {
  name       = "rds-subnet-group"
  subnet_ids = module.vpc.private_subnets

  tags = {
    Name = "rds-subnet-group"
  }
}

resource "aws_db_instance" "postgres" {
  identifier         = "temperature-db"
  engine             = "postgres"
  instance_class     = "db.t3.micro"
  allocated_storage  = 20
#   name               = "temperatures"
  username           = "postgres"
  password           = "password123"
  publicly_accessible = false
  skip_final_snapshot = true

  db_subnet_group_name = aws_db_subnet_group.default.name
  vpc_security_group_ids = [module.vpc.default_security_group_id]

  tags = {
    Name = "temperature-postgres"
  }
}
