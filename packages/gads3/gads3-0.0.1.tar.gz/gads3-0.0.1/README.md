<p align="center">
  <a href="https://github.com/AlexDemure/gads3">
    <a href="https://ibb.co/8ghgbtdJ"><img src="https://i.ibb.co/xq4qYdfy/logo.png" alt="logo" border="0"></a>
  </a>
</p>

<p align="center">
  An async and lightweight S3 client for uploading, downloading, and deleting files
</p>

---

### Installation

```
pip install gads3
```

### Usage

```sh
from gads3 import S3, Mimetype

s3 = S3(
    bucket="media",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="S3_ACCESS_KEY",
    aws_secret_access_key="S3_SECRET_KEY",
)

await s3.upload(file=bytes, filename="filename", mimetype=Mimetype.jpeg storage="files")
await s3.delete(filename="filename", mimetype=Mimetype.jpeg storage="files")
```
