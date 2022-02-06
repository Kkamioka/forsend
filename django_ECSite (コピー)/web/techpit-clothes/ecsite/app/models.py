from django.db import models

# Create your models here.
class Product(models.Model):
    # カテゴリ名のフィールド
    name = models.CharField(verbose_name='名前', max_length=50)
    description = models.TextField(verbose_name='説明', blank=True, null=True, max_length=200)
    image = models.ImageField(verbose_name='写真', blank=True, null=True)
    price = models.IntegerField(verbose_name='価格', default=1000)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    # カテゴリ名のフィールド
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)



class line_items(models.Model):
    # カテゴリ名のフィールド
    cart_id = models.ForeignKey('Cart', verbose_name='カートID', on_delete=models.CASCADE)
    product_id = models.ForeignKey('Product', verbose_name='商品ID', on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='数量')
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)

    
