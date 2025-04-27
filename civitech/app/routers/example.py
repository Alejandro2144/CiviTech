from fastapi import APIRouter

router = APIRouter(
    prefix="/example",
    tags=["example"]
)

@router.get("/")
def get_example():
    return {"message": "This is an example endpoint."}
