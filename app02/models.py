from django.db import models


class Host(models.Model):
    """
    主机表
    """

    host = models.CharField(verbose_name='主机名', max_length=32)
    ip = models.GenericIPAddressField(verbose_name='IP', protocol='both')  # 即支持ipv4也支持ipv6
    
