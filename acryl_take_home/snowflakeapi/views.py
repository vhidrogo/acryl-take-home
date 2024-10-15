import snowflake.connector
from django.conf import settings
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page


class SchemaListView(View):
    def get(self, request):
        conn = snowflake.connector.connect(
            user=settings.SNOWFLAKE_USER,
            password=settings.SNOWFLAKE_PASSWORD,
            account=settings.SNOWFLAKE_ACCOUNT_ID,
            warehouse=settings.SNOWFLAKE_WAREHOUSE,
            database=settings.SNOWFLAKE_DATABASE
        )
        cursor = conn.cursor()
        cursor.execute("SHOW SCHEMAS")
        schemas = cursor.fetchall()
        cursor.close()
        conn.close()
        return JsonResponse({'schemas': schemas})


class TableListView(View):
    def get(self, request, schema_name):
        conn = snowflake.connector.connect(
            user=settings.SNOWFLAKE_USER,
            password=settings.SNOWFLAKE_PASSWORD,
            account=settings.SNOWFLAKE_ACCOUNT_ID,
            warehouse=settings.SNOWFLAKE_WAREHOUSE,
            database=settings.SNOWFLAKE_DATABASE
        )
        cursor = conn.cursor()
        
        try:
            cursor.execute(f"SHOW TABLES IN SCHEMA {schema_name}")
            tables = cursor.fetchall()
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        finally:
            cursor.close()
            conn.close()
        
        return JsonResponse({'tables': tables})


class ColumnListView(View):
    @method_decorator(cache_page(60 * 5))  # Cache for 5 minutes
    def get(self, request, schema_name, table_name):
        conn = snowflake.connector.connect(
            user=settings.SNOWFLAKE_USER,
            password=settings.SNOWFLAKE_PASSWORD,
            account=settings.SNOWFLAKE_ACCOUNT_ID,
            warehouse=settings.SNOWFLAKE_WAREHOUSE,
            database=settings.SNOWFLAKE_DATABASE
        )
        cursor = conn.cursor()
        
        # Execute a query to fetch the columns for the specified table
        query = f"DESC TABLE {schema_name}.{table_name}"
        cursor.execute(query)
        columns = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # Format the columns into a more readable format
        columns_data = []
        for column in columns:
            column_info = {
                "name": column[0],
                "type": column[1],
                "description": column[2]
            }
            columns_data.append(column_info)

        return JsonResponse({'columns': columns_data})


class TableSummaryView(View):
    def get(self, request, schema_name, table_name):
        conn = snowflake.connector.connect(
            user=settings.SNOWFLAKE_USER,
            password=settings.SNOWFLAKE_PASSWORD,
            account=settings.SNOWFLAKE_ACCOUNT_ID,
            warehouse=settings.SNOWFLAKE_WAREHOUSE,
            database=settings.SNOWFLAKE_DATABASE
        )
        cursor = conn.cursor()
        
        # Get column names and types
        cursor.execute(f"DESC TABLE {schema_name}.{table_name}")
        columns = cursor.fetchall()
        
        summary = {}

        # Generate SQL to get summary statistics
        for column in columns:
            column_name = column[0]
            column_type = column[1]

            if "NUMBER" in column_type.upper():
                query = f"""
                    SELECT 
                        COUNT({column_name}) AS non_null_count,
                        AVG({column_name}) AS mean,
                        MIN({column_name}) AS min,
                        MAX({column_name}) AS max
                    FROM {schema_name}.{table_name}
                """
                cursor.execute(query)
                stats = cursor.fetchone()
                summary[column_name] = {
                    "non_null_count": stats[0],
                    "mean": stats[1],
                    "min": stats[2],
                    "max": stats[3]
                }
            else:
                query = f"""
                    SELECT 
                        COUNT({column_name}) AS non_null_count,
                        COUNT(DISTINCT {column_name}) AS unique_count
                    FROM {schema_name}.{table_name}
                """
                cursor.execute(query)
                stats = cursor.fetchone()
                summary[column_name] = {
                    "non_null_count": stats[0],
                    "unique_count": stats[1]
                }

        cursor.close()
        conn.close()

        return JsonResponse({'summary': summary})