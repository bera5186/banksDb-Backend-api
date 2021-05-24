from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.core import paginator
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .serializers import BankSerializer, BranchSerializer
from .models import Banks, Branches

import math


class BranchSearch(APIView):

    # caching decorators
    @method_decorator(cache_page(60 * 2))
    @method_decorator(vary_on_cookie)
    def get(self, request):
        # parsing query params from request
        search_query = request.GET.get("q")
        limit = request.GET.get("limit")
        offset = request.GET.get("offset")
        city = request.GET.get("city")

        
        if search_query is None:
            return Response({"error":True,"query": "Null"}, status=status.HTTP_400_BAD_REQUEST)
        if city is None:
            return Response({"error":True,"city": "Null"}, status=status.HTTP_400_BAD_REQUEST)
        if limit is None:
            limit = 5
        if offset is None:
            offset = 1

        vector = SearchVector('city') + SearchVector('state') + SearchVector('address') + SearchVector('branch') \
                                      + SearchVector('state') + SearchVector('ifsc')
        query = SearchQuery(str(search_query).upper())
        branches = Branches.objects.filter(city=str(city).upper()).annotate(rank=SearchRank(vector, query)) \
                                                                  .order_by('-rank')

        total_results = branches.count()
        n_pages = math.ceil(total_results/int(limit))

        branches_limited = paginator.Paginator(branches, limit)
        branches_offsetted = branches_limited.get_page(offset)
        serializer = BranchSerializer(branches_offsetted, many=True)

        return Response({"error":False,"result":serializer.data, "n_pages": n_pages, "per_page": limit}, status=status.HTTP_200_OK)


class BranchesAutocomplete(APIView):
    # caching decorators
    @method_decorator(cache_page(60 * 2))
    @method_decorator(vary_on_cookie)
    def get(self, request):
        # parsing query params from request
        search_query = request.GET.get("q")
        limit = request.GET.get("limit")
        offset = request.GET.get("offset")

        if search_query is None:
            return Response({"error":True, "query": "Null"}, status=status.HTTP_400_BAD_REQUEST)
        if limit is None:
            limit = 5
        if offset is None:
            offset = 1

        context = {"error": False}

        try:
            branches = Branches.objects.filter(branch_vector=str(search_query).lower()).order_by('ifsc')
            branches_limited = paginator.Paginator(branches, limit)
            branches_offsetted = branches_limited.get_page(offset)
            serializer = BranchSerializer(branches_offsetted, many=True)

            context["result"] = serializer.data
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            context["error"] = True
            context["result"] = []
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BankInfo(APIView):
    @method_decorator(cache_page(60 * 2))
    @method_decorator(vary_on_cookie)
    def get(self, request, id):
        context = {"error": False}

        if id is None:
            context["error"] = True
            context["message"] = ['Pass bank id banks/:id']
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        bank = Banks.objects.filter(id=id).first()
        serialized_bank = BankSerializer(bank, many=False)

        count = Branches.objects.filter(bank=id).count()
        

        context["result"] = serialized_bank.data
        context["n_branch"] = count

        return Response(context, status=status.HTTP_200_OK)
