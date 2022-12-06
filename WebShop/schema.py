import graphene
from graphene_django import DjangoObjectType

from Products.models import Product, Category, ProductImage


class CategoryType(DjangoObjectType):
    class Meta:
        name = 'category'
        model = Category
        fields = ('id', 'name', 'parent')


class ProductImageType(DjangoObjectType):
    class Meta:
        name = 'image'
        model = ProductImage
        field = ("id", "image")

    def resolve_image(self, info):
        if self.image:
            self.image = info.context.build_absolute_uri(self.image.url)
        return self.image

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'price', 'rating', 'stock', 'product_image')




class Query(graphene.ObjectType):
    products = graphene.List(ProductType)
    images = graphene.List(ProductImageType)

    def resolve_products(self, info):
        return Product.objects.all()

    def resolve_images(self):
        return ProductImage.objects.all()


schema = graphene.Schema(query=Query)
