

# Import local modules directly (no "app." prefix)
import services
import schema

from schema import UserIn, BaseResponse, UserListOut

app = FastAPI()

# Prometheus metrics endpoint
Instrumentator().instrument(app).expose(app, endpoint="/metrics")


@app.get("/")
async def index():
    """
    Index route for the application
    """
    return {"message": "Hello from FastAPI - @kiranrakh155@gmail.com ;)"}


@app.post("/users", response_model=BaseResponse)
async def user_create(user: UserIn):
    """
    Add user data to JSON file
    """
    try:
        services.add_userdata(user.dict())
    except Exception as e:
        return {"success": False, "error": str(e)}
    return {"success": True}


@app.get("/users", response_model=UserListOut)
async def get_users():
    """
    Read user data from JSON file
    """
    return services.read_usersdata()

