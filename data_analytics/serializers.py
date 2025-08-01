from rest_framework import serializers

class MetricSerializer(serializers.Serializer):
    value = serializers.DecimalField(max_digits=10, decimal_places=2)
    change_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)
    description = serializers.CharField(max_length=255)

class ClientMetricSerializer(serializers.Serializer):
    value = serializers.IntegerField()
    change_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)
    description = serializers.CharField(max_length=255)

class ChartDataSerializer(serializers.Serializer):
    labels = serializers.ListField(child=serializers.CharField())
    data = serializers.ListField(child=serializers.DecimalField(max_digits=10, decimal_places=2))

class AnalyticsDashboardSerializer(serializers.Serializer):
    total_profit = MetricSerializer()
    total_clients = ClientMetricSerializer()
    visits_by_day = ChartDataSerializer()
    profit_by_day = ChartDataSerializer()