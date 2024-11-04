import azure.functions as func
from blobfiletrigger.function import bp as bp_videoupload
from health.function import bp as bp_health

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# Register blueprints
app.register_functions(bp_health)
app.register_functions(bp_videoupload)
