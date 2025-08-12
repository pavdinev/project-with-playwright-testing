import pytest

@pytest.mark.smoke
def test_get_products(playwright):
    api_request_context = playwright.request.new_context()
    response = api_request_context.get("https://fakestoreapi.com/products")
    assert response.ok
    data = response.json()
    assert isinstance(data, list)
    api_request_context.dispose()
