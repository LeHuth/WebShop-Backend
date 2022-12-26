import graphene
import graphql_jwt
from graphene_django import DjangoObjectType
from Members.models import Member, MemberImage, MemberAddress
from Products.models import Product, Category, ProductImage, Review, Vote, Manufacturer
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery
import datetime
from Members.schema import Query as MemberQuery


class VoteType(DjangoObjectType):
    class Meta:
        name = 'vote'
        model = Vote
        fields = ('id', 'value', 'timestamp', 'member', 'review')


class ReviewType(DjangoObjectType):
    class Meta:
        name = 'review'
        model = Review
        fields = ('id', 'title', 'rating', 'text', 'created', 'member', 'review_vote')


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
        fields = ('id', 'name', 'category', 'price', 'rating', 'stock', 'product_image', 'product_review', 'manufacturer', 'gender' ,'variants')


class ManufacturerType(DjangoObjectType):
    class Meta:
        model = Manufacturer
        fields = '__all__'


class AllProductsQuery(graphene.ObjectType):
    all_products = graphene.List(ProductType)

    def resolve_all_products(self):
        return Product.objects.all()
