from django.urls import path
from .views import SchemaListView, TableListView, ColumnListView, TableSummaryView

urlpatterns = [
    path('schemas/', SchemaListView.as_view(), name='schema-list'),
    path('schemas/<str:schema_name>/tables/', TableListView.as_view(), name='table-list'),
    path('schemas/<str:schema_name>/tables/<str:table_name>/columns/', ColumnListView.as_view(), name='column-list'),
    path('schemas/<str:schema_name>/tables/<str:table_name>/summary/', TableSummaryView.as_view(), name='table-summary'),
]
