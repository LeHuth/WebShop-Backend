import django_filters
import graphene
import graphene_django.filter
import graphql_jwt
from graphene_django import DjangoObjectType
from Members.models import Member, MemberImage, MemberAddress
from Products.models import Product, Category, ProductImage, Review, Vote, Manufacturer, ProductPdf
from django.db.models import Q
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


class ProductPdfType(DjangoObjectType):
    class Meta:
        name = 'docfile'
        model = ProductPdf
        field = ('docfile', 'product',)

    def resolve_docfile(self, info):
        if self.docfile:
            self.docfile = info.context.build_absolute_uri(self.docfile.url)
        return self.docfile


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    searchterm = django_filters.CharFilter(method='product_filter', label='SearchProducts')

    class Meta:
        model = Product
        fields = ('name',)

    def product_filter(self, queryset,name, value):
        return queryset.filter(
            Q(name__icontains=value)
        )


class ProductNode(DjangoObjectType):
    class Meta:
        name='product'
        model = Product

        fields = (
            'id', 'name', 'category', 'price', 'rating', 'stock', 'product_image', 'product_review', 'manufacturer',
            'gender', 'variants', 'short_description', 'product_pdf')
        filterset_class = ProductFilter
        interfaces = (relay.Node,)


class ManufacturerType(DjangoObjectType):
    class Meta:
        model = Manufacturer
        fields = '__all__'


class VoteMutation(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        upvote = graphene.Boolean(required=True)
        rId = graphene.Int(required=True)

    vote = graphene.Field(VoteType)

    @classmethod
    def mutate(cls, root, info, rId, upvote):
        member = info.context.user
        review = Review.objects.get(pk=rId)
        result = Vote.objects.filter(Q(member=member) & Q(review=review))

        if result.count() == 0:
            vote = Vote(value=upvote, member=member, review=review)
            vote.save()
            return VoteMutation(vote=vote)

        if result[0].value == upvote:
            result[0].delete()
            return VoteMutation(ok=True)
        else:
            vote = result[0]
            vote.value = upvote
            vote.save()
            return VoteMutation(vote=vote)


class AllProductsQuery(graphene.ObjectType):
    #products = graphene.List(ProductNode)
    product_detail = graphene.Field(ProductNode, productid=graphene.Int())
    product_reviews = graphene.List(ReviewType, productid=graphene.Int())
    all_products = graphene_django.filter.DjangoFilterConnectionField(ProductNode)

    def resolve_product_detail(root, info, productid):
        return Product.objects.get(pk=productid)

    def resolve_product_reviews(root, info, productid):
        return Review.objects.filter(product=productid)

    def resolve_products(self, info):
        return Product.objects.all()
