resource "aws_instance" "main" {
  ami = "ami-4fffc834"
  instance_type = "t2.micro"
  subnet_id = "${var.subnet_id}"
  vpc_security_group_ids = ["${var.sg_admin_id}"]
  key_name = "${var.key_name}"

  tags {
    Name = "pdf-worker"
  }
}