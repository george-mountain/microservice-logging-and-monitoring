from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Item
from .serializers import ItemSerializer
from prometheus_client import generate_latest
from app.utils.logger_config import app_logger
from app.metrics import request_counter
from uuid import uuid4


class ItemList(APIView):
    def get(self, request):
        log_id = str(uuid4())
        with app_logger.contextualize(log_id=log_id):
            try:
                app_logger.info("Accessed Item List endpoint")
                items = Item.objects.all()
                serializer = ItemSerializer(items, many=True)
                request_counter.labels(
                    endpoint="item_list", method="GET", status="success"
                ).inc()
                return Response(serializer.data)
            except Exception as ex:
                app_logger.error(f"Failed to retrieve item list: {ex}")
                request_counter.labels(
                    endpoint="item_list", method="GET", status="error"
                ).inc()
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        log_id = str(uuid4())
        with app_logger.contextualize(log_id=log_id):
            try:
                app_logger.info("Creating a new Item")
                serializer = ItemSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    request_counter.labels(
                        endpoint="item_create", method="POST", status="success"
                    ).inc()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                app_logger.error(f"Failed to create item: {serializer.errors}")
                request_counter.labels(
                    endpoint="item_create", method="POST", status="error"
                ).inc()
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as ex:
                app_logger.error(f"Failed to create item: {ex}")
                request_counter.labels(
                    endpoint="item_create", method="POST", status="error"
                ).inc()
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ItemDetail(APIView):
    def get(self, request, pk):
        log_id = str(uuid4())
        with app_logger.contextualize(log_id=log_id):
            try:
                app_logger.info(f"Accessed Item Detail for item {pk}")
                item = Item.objects.get(pk=pk)
                serializer = ItemSerializer(item)
                request_counter.labels(
                    endpoint="item_detail", method="GET", status="success"
                ).inc()
                return Response(serializer.data)
            except Item.DoesNotExist:
                app_logger.error(f"Item {pk} not found")
                request_counter.labels(
                    endpoint="item_detail", method="GET", status="not_found"
                ).inc()
                return Response(status=status.HTTP_404_NOT_FOUND)
            except Exception as ex:
                app_logger.error(f"Failed to retrieve item detail: {ex}")
                request_counter.labels(
                    endpoint="item_detail", method="GET", status="error"
                ).inc()
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        log_id = str(uuid4())
        with app_logger.contextualize(log_id=log_id):
            try:
                app_logger.info(f"Updating Item {pk}")
                item = Item.objects.get(pk=pk)
                serializer = ItemSerializer(item, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    request_counter.labels(
                        endpoint="item_update", method="PUT", status="success"
                    ).inc()
                    return Response(serializer.data)
                app_logger.error(f"Failed to update item {pk}: {serializer.errors}")
                request_counter.labels(
                    endpoint="item_update", method="PUT", status="error"
                ).inc()
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Item.DoesNotExist:
                app_logger.error(f"Item {pk} not found")
                request_counter.labels(
                    endpoint="item_update", method="PUT", status="not_found"
                ).inc()
                return Response(status=status.HTTP_404_NOT_FOUND)
            except Exception as ex:
                app_logger.error(f"Failed to update item {pk}: {ex}")
                request_counter.labels(
                    endpoint="item_update", method="PUT", status="error"
                ).inc()
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        log_id = str(uuid4())
        with app_logger.contextualize(log_id=log_id):
            try:
                app_logger.info(f"Deleting Item {pk}")
                item = Item.objects.get(pk=pk)
                item.delete()
                request_counter.labels(
                    endpoint="item_delete", method="DELETE", status="success"
                ).inc()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Item.DoesNotExist:
                app_logger.error(f"Item {pk} not found")
                request_counter.labels(
                    endpoint="item_delete", method="DELETE", status="not_found"
                ).inc()
                return Response(status=status.HTTP_404_NOT_FOUND)
            except Exception as ex:
                app_logger.error(f"Failed to delete item {pk}: {ex}")
                request_counter.labels(
                    endpoint="item_delete", method="DELETE", status="error"
                ).inc()
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MetricsView(APIView):
    def get(self, request):
        return Response(generate_latest(), content_type="text/plain")


class RootView(APIView):
    def get(self, request):
        app_logger.info("Root endpoint accessed")
        return Response({"Hello": "World"})
