import django_filters
import graphene
import graphene_django.filter
import graphql_jwt
from graphene import relay
from graphene_django import DjangoObjectType
from Members.models import Member, MemberImage
from django.db.models import Q


class MemberImageType(DjangoObjectType):
    class Meta:
        name = 'member_image'
        model = MemberImage
        field = ('id', 'image')

    def resolve_image(self, info):
        if self.image:
            self.image = info.context.build_absolute_uri(self.image.url)
        return self.image


class MemberFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')

    searchterm = django_filters.CharFilter(method='my_custom_filter', label='Search')

    class Meta:
        model = Member
        fields = ('username', 'email',)

    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(
            Q(username__icontains=value) | Q(email__icontains=value)
        )


class MemberNode(DjangoObjectType):
    class Meta:
        name = 'member'
        model = Member
        fields = ('id', 'username', 'member_image', 'review_owner')
        filterset_class = MemberFilter
        interfaces = (relay.Node,)


class SelfQuery(graphene.ObjectType):
    self = graphene.Field(MemberNode)


    def resolve_self(self, info):
        member = info.context.user
        if not member.is_authenticated:
            raise Exception("Authentication credentials were not provided")
        return member


class Query(SelfQuery, graphene.ObjectType):
    member = relay.Node.Field(MemberNode)
    all_members = graphene_django.filter.DjangoFilterConnectionField(MemberNode)
