import random
import requests

from typing import Callable, Union

from .exceptions import ProxyRequestException


type ReqFunc = Callable[[str], requests.Response]


def create_req_func(
    method: str,
    *args,
    **kwargs,
) -> ReqFunc:
    """
    Creates a function that sends a request using a proxy.

    Args:
        method (str): The name of the request method (e.g. "get", "post", "put", "delete").
        *args: Additional arguments to pass to the request method.
        **kwargs: Additional keyword arguments to pass to the request method.

    Returns:
        ReqFunc: A function that sends a request using a proxy.
    """

    def req_func(proxy: str) -> requests.Response:
        return getattr(requests, method)(
            *args,
            **kwargs,
            proxies={"http": proxy, "https": proxy},
        )

    return req_func


def create_proxy_method(method_name: str):
    """
    Creates a method that sends a request using a proxy.

    Args:
        method_name (str): The name of the request method (e.g. "get", "post", "put", "delete").

    Returns:
        method: A method that sends a request using a proxy.
    """

    def method(self: "ProxyRequests", *args, **kwargs) -> requests.Response:
        req_func = create_req_func(method_name, *args, **kwargs)
        return self.perform_request(req_func)

    return method


class ProxyRequests:
    """
    A class that sends requests using a proxy.

    This class provides a way to make HTTP requests through a rotating set of proxies.
    It automatically handles proxy selection and error management, attempting multiple
    proxies until a successful response is received or all proxies have been tried.

    The class supports common HTTP methods (GET, POST, PUT, PATCH, DELETE) with an
    interface similar to the requests library.

    Examples:
        Basic usage with a list of proxies:

        >>> proxies = [
        ...     "http://user1:pass1@192.168.1.1:8080",
        ...     "http://user2:pass2@192.168.1.2:8080"
        ... ]
        >>> proxy_req = ProxyRequests(proxy_list=proxies)
        >>> response = proxy_req.get('https://example.com')
        >>> print(response.status_code)
        200

        Making a POST request with JSON data:

        >>> proxy_req = ProxyRequests(proxy_list=proxies, timeout=5.0)
        >>> data = {"username": "test_user", "password": "test_pass"}
        >>> response = proxy_req.post('https://api.example.com/login', json=data)
        >>> result = response.json()

        Using custom parameters and headers:

        >>> headers = {"User-Agent": "Custom User Agent"}
        >>> params = {"page": 1, "limit": 10}
        >>> response = proxy_req.get(
        ...     'https://api.example.com/products',
        ...     params=params,
        ...     headers=headers
        ... )

    Attributes:
        proxy_list (list[str]): A list of proxy URLs.
        proxy_sample_size (int): Number of proxies to sample for each request.
        timeout (float): Request timeout in seconds.
    """

    def __init__(
        self,
        proxy_list: list[str],
        proxy_sample_size: int = 10,
        timeout: float = 10.0,
    ) -> None:
        """
        Initialize a ProxyRequests object.

        Args:
            proxy_list (list[str]): A list of proxy URLs with the format "http://user:pass@ip:port".
            proxy_sample_size (int): The number of proxies to sample. Defaults to 10.
            timeout (float): The timeout for requests in seconds. Defaults to 10.0 seconds.

        Returns:
            None
        """
        self.proxy_list = proxy_list
        self.timeout = timeout
        self.proxy_sample_size = proxy_sample_size

    def choose_proxy_set(self) -> list[str]:
        """
        Choose a set of proxies from the proxy list.

        Returns:
            list[str]: A list of proxy URLs.
        """
        if len(self.proxy_list) < self.proxy_sample_size:
            return self.proxy_list

        return random.sample(self.proxy_list, k=self.proxy_sample_size)

    def perform_request(self, req_func: ReqFunc) -> requests.Response:
        """
        Perform a request using a proxy.

        Args:
            req_func (ReqFunc): A function that sends a request using a proxy.

        Returns:
            requests.Response: The response object from the request.
        """
        proxy_set = self.choose_proxy_set()
        errors = []
        for proxy in proxy_set:
            try:
                response = req_func(proxy)
                return response
            except requests.RequestException as e:
                errors.append(e)

        raise ProxyRequestException(errors)

    def get(
        self,
        url: str,
        params: Union[dict, list[tuple], bytes, None] = None,
        **kwargs,
    ) -> requests.Response:
        """
        Send a GET request to the specified URL using a proxy.

        Args:
            url: The URL to send the request to.
            params: Optional dictionary, list of tuples, or bytes to send in the query string.
            **kwargs: Additional arguments to pass to the underlying requests.get method.

        Returns:
            requests.Response: The response object from the GET request.
        """
        get_method = create_proxy_method("get")
        return get_method(
            self,
            url,
            params=params,
            timeout=self.timeout,
            **kwargs,
        )

    def post(
        self,
        url: str,
        data: Union[dict, list[tuple], bytes, None] = None,
        json=None,
        **kwargs,
    ) -> requests.Response:
        """
        Send a POST request to the specified URL using a proxy.

        Args:
            url: The URL to send the request to.
            data: Optional dictionary, list of tuples, or bytes to send in the body of the POST request.
            json: Optional json serializable object to send in the body of the POST request.
            **kwargs: Additional arguments to pass to the underlying requests.post method.

        Returns:
            requests.Response: The response object from the POST request.
        """
        post_method = create_proxy_method("post")
        return post_method(
            self,
            url,
            data=data,
            json=json,
            timeout=self.timeout,
            **kwargs,
        )

    def put(
        self,
        url: str,
        data: Union[dict, list[tuple], bytes, None] = None,
        json=None,
        **kwargs,
    ) -> requests.Response:
        """
        Send a PUT request to the specified URL using a proxy.

        Args:
            url: The URL to send the request to.
            data: Optional dictionary, list of tuples, or bytes to send in the body of the PUT request.
            json: Optional json serializable object to send in the body of the PUT request.
            **kwargs: Additional arguments to pass to the underlying requests.put method.

        Returns:
            requests.Response: The response object from the PUT request.
        """
        put_method = create_proxy_method("put")
        return put_method(
            self,
            url,
            data=data,
            json=json,
            timeout=self.timeout,
            **kwargs,
        )

    def patch(
        self,
        url: str,
        data: Union[dict, list[tuple], bytes, None] = None,
        json=None,
        **kwargs,
    ) -> requests.Response:
        """
        Send a PATCH request to the specified URL using a proxy.

        Args:
            url: The URL to send the request to.
            data: Optional dictionary, list of tuples, or bytes to send in the body of the PATCH request.
            json: Optional json serializable object to send in the body of the PATCH request.
            **kwargs: Additional arguments to pass to the underlying requests.patch method.

        Returns:
            requests.Response: The response object from the PATCH request.
        """
        patch_method = create_proxy_method("patch")
        return patch_method(
            self,
            url,
            data=data,
            json=json,
            timeout=self.timeout,
            **kwargs,
        )

    def delete(
        self,
        url: str,
        **kwargs,
    ) -> requests.Response:
        """
        Send a DELETE request to the specified URL using a proxy.

        Args:
            url: The URL to send the request to.
            **kwargs: Additional arguments to pass to the underlying requests.delete method.

        Returns:
            requests.Response: The response object from the DELETE request.
        """
        delete_method = create_proxy_method("delete")
        return delete_method(
            self,
            url,
            timeout=self.timeout,
            **kwargs,
        )

    def __repr__(self) -> str:
        """
        Return a string representation of the ProxyRequests object.

        Returns:
            str: A string representation of the ProxyRequests object.
        """
        return f"{self.__class__.__name__}(proxy_list={self.proxy_list})"
