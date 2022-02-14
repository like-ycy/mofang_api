import oss2


class OSS(object):
    """
    阿里云对象存储工具类
    """

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """初始化"""
        self.app = app
        return self.setup()

    def setup(self):
        """安装"""
        self.endpoint = self.app.config.get("OSS_ENDPOINT")
        self.bucket_name = self.app.config.get("OSS_BUCKET_NAME")
        self.bucket_url = self.app.config.get("OSS_BUCKET_URL")
        self.access_key_id = self.app.config.get("ALI_ACCESS_KEY_ID")
        self.access_key_secret = self.app.config.get("ALI_ACCESS_KEY_SECRET")
        self.auth = oss2.Auth(self.access_key_id, self.access_key_secret)
        self.bucket = oss2.Bucket(self.auth, self.endpoint, self.bucket_name)
        return self.bucket

    def upload(self, name, data):
        """文件上传"""
        return self.bucket.put_object(name, data)

    def download(self, remote_name, local_name):
        """
        文件下载
        :param remote_name 要下载的文件路径
        :param local_name 本次保存下载文件的路径
        """
        object_stream = self.bucket.get_object(remote_name)
        content = object_stream.read()
        with open(f"{local_name}", "wb+") as f:
            f.write(content)
