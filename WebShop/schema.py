import graphene
import graphql_jwt
from graphene_django import DjangoObjectType
from Members.models import Member, MemberImage, MemberAddress
from Products.models import Product, Category, ProductImage, Review, Vote
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
        fields = ('id', 'name', 'category', 'price', 'rating', 'stock', 'product_image', 'product_review')


class Query(UserQuery, MemberQuery, MeQuery, graphene.ObjectType):
    products = graphene.List(ProductType)
    images = graphene.List(ProductImageType)
    product_detail = graphene.Field(ProductType, productid=graphene.Int())
    product_reviews = graphene.List(ReviewType, productid=graphene.Int())

    def resolve_product_reviews(root, info, productid):
        return Review.objects.filter(product=productid)

    def resolve_product_detail(root, info, productid):
        return Product.objects.get(pk=productid)

    def resolve_products(self, info):
        return Product.objects.all()

    def resolve_images(self):
        return ProductImage.objects.all()


class ProductMutation(graphene.Mutation):
    class Arguments:
        p_id = graphene.ID()
        name = graphene.String(required=True)

    product = graphene.Field(ProductType)

    @classmethod
    def mutate(cls, root, info, p_id, name):
        product = Product.objects.get(pk=p_id)
        product.name = name
        product.save()

        return ProductMutation(product=product)


class ReviewMutation(graphene.Mutation):
    class Arguments:
        r_id = graphene.ID()
        title = graphene.String(required=True)

    review = graphene.Field(ReviewType)

    @classmethod
    def mutate(cls, root, info, r_id, title):
        review = Review.objects.get(pk=r_id)
        review.title = title
        review.updated = datetime.datetime.now()
        review.save()

        return ReviewMutation(review=review)


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    login = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    update_account = mutations.UpdateAccount.Field()


class Mutation(AuthMutation, graphene.ObjectType):
    update_product = ProductMutation.Field()
    update_review = ReviewMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
