import graphene
import graphql_jwt
from graphene_django import DjangoObjectType
from Members.models import Member, MemberImage, MemberAddress
from Products.models import Product, Category, ProductImage, Review, Vote, Manufacturer
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery
import datetime
from graphene import relay
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


class ProductNode(DjangoObjectType):
    class Meta:
        model = Product
        fields = (
        'id', 'name', 'category', 'price', 'rating', 'stock', 'product_image', 'product_review', 'manufacturer',
        'gender', 'variants', 'short_description')


class ManufacturerType(DjangoObjectType):
    class Meta:
        model = Manufacturer
        fields = '__all__'


class AllProductsQuery(graphene.ObjectType):
    products = graphene.List(ProductNode)
    product_detail = graphene.Field(ProductNode, productid=graphene.Int())
    product_reviews = graphene.List(ReviewType, productid=graphene.Int())

    def resolve_product_detail(root, info, productid):
        return Product.objects.get(pk=productid)

    def resolve_product_reviews(root, info, productid):
        return Review.objects.filter(product=productid)

    def resolve_products(self, info):
        return Product.objects.all()



