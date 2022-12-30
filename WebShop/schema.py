import graphene
import graphql_jwt
from graphene_django import DjangoObjectType
from Members.models import Member, MemberImage, MemberAddress
from Products.models import Product, Category, ProductImage, Review, Vote
from Products.schema import AllProductsQuery, ProductNode, ReviewType, ProductImageType, VoteMutation,ReportMutation
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery
import datetime
from Members.schema import Query as MemberQuery


class Query(UserQuery, MemberQuery, MeQuery, AllProductsQuery, graphene.ObjectType):
    images = graphene.List(ProductImageType)

    def resolve_images(self):
        return ProductImage.objects.all()


class ProductMutation(graphene.Mutation):
    class Arguments:
        p_id = graphene.ID()
        name = graphene.String(required=True)

    product = graphene.Field(ProductNode)

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


class CreateReviewMutation(graphene.Mutation):
    class Arguments:
        p_id = graphene.Int(required=True)
        title = graphene.String()
        text = graphene.String()
        rating = graphene.Decimal(required=True)

    review = graphene.Field(ReviewType)

    @classmethod
    def mutate(cls, root, info, title, text, rating, p_id):
        if info.context.user.is_authenticated:
            product = Product.objects.get(pk=p_id)
            review = Review(title=title, text=text, rating=rating, member=info.context.user, product=product)
            review.save()
            return CreateReviewMutation(review=review)
        else:
            raise Exception("Authentication credentials were not provided")


class DeleteReviewMutation(graphene.Mutation):
    class Arguments:
        r_id = graphene.Int(required=True)

    review = graphene.Field(ReviewType)
    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, r_id):
        review = Review.objects.get(pk=r_id)
        member = info.context.user
        if review.member is not member and not member.is_staff:
            raise Exception("This User is not Authorized to perform this action")

        review.delete()
        return DeleteReviewMutation(review=review, ok=True)


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    login = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    update_account = mutations.UpdateAccount.Field()
    refresh_token = mutations.RefreshToken.Field()


class Mutation(AuthMutation, graphene.ObjectType):
    update_product = ProductMutation.Field()
    update_review = ReviewMutation.Field()
    create_review = CreateReviewMutation.Field()
    delete_review = DeleteReviewMutation.Field()
    vote = VoteMutation.Field()
    report = ReportMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
