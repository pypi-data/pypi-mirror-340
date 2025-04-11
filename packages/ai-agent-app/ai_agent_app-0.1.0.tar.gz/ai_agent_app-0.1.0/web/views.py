import logging
import os
import sys
import uuid
from common.log_formatter import setup_logger
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from models.queryModel import baseQuery
from web import settings
from importlib.metadata import version
from injector import inject
from ai_agent.sql_agent import AiAgentApiService
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework import status

logger = setup_logger("cit-datacenter-service-ai-agent")

class LivenessCheckView(APIView):
    """
    Liveness check to indicate if the application is running.
    """
    authentication_classes = []
    permission_classes = []
    @swagger_auto_schema(
        operation_description="Liveness Check - Indicates if the application is alive.",
        tags=["Health Check"],
        responses={200: "Application is alive"}
    )
    def get(self, request):
        return JsonResponse({"status": "alive"}, status=200)


class IndexView(View):
    """
    Handles the rendering of the index page with application details.
    """
    def get(self, request):
        # Gather application information
        app_info = {
            "app_name": "CIT Datacenter Service AI Agent",
            "version": "1.0.0",
            "environment": "development",
            "django_version": version('django'),
            "installed_apps": list(settings.INSTALLED_APPS),
        }
        #fetch/create correlation id
        if request.META.get('HTTP_DELL_TRACE_ID'):
            correlation_id = str(request.META.get('HTTP_DELL_TRACE_ID'))
        else:
            correlation_id = str(uuid.uuid4())
        logger.info("Rendering the index page with app info.",extra={'correlation_id': correlation_id})
        logger.debug(f"App Info: {app_info}", extra={'correlation_id': correlation_id})

        response =  render(request, 'index.html', {'app_info': app_info})
        response['dell-trace-id'] = correlation_id
        return response
    
class QueryAiAgentView(APIView):
    """
    Query AI Agent and return filtered results from Datacenter view.
    """

    def __init__(self):
        self.ai_agent = AiAgentApiService()

    # @swagger_auto_schema(
    #     operation_description=" Post Operation",
    #     responses={200: "Operation successfully.", 500: "Internal Server Error"},
    #     tags=["Virtual Data Center"]
    # )
    # def post(self,request):
    #     logger.info("Entering into Post Operation")


    @swagger_auto_schema(
        operation_description=" Get Operation",
        responses={200: "Operation successfully.", 500: "Internal Server Error"},
        tags=["Virtual Data Center"],
        manual_parameters=[
            openapi.Parameter(
                name='question',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Query to ask the agent',
                required=True,
                default=None
            ),
        ]
    )
    def post(self,request):
        logger.info("Entering into Get Operation")

        # Get user query
        question = str(request.query_params.get('question', None))
        try:
            # Get the paginated result, which now includes both vcenters and pageInfo
            result = self.ai_agent.get_ai_agent_query(question)
            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error in fetching vcenters: {e}")
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        finally:
            # Close the session at the end of the request lifecycle
            logger.info("Exiting from Get Operation")  