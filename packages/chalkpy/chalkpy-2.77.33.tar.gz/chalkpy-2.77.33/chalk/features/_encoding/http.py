from typing import TYPE_CHECKING, Generic, Mapping, Optional, TypeVar

if TYPE_CHECKING:
    from pydantic import BaseModel
else:
    try:
        from pydantic.v1.generics import GenericModel as BaseModel
    except ImportError:
        from pydantic import BaseModel


T = TypeVar("T", str, bytes)


class HttpResponse(BaseModel, Generic[T]):
    """
     Feature annotation for HTTP responses, with a string body. HTTP responses are treated internally as
     structs, and you can treat them as such in code/expressions that involve this feature.

     The underlying pyarrow type of HttpStringResponse is
     pa.struct_([
         pa.field("status_code", pa.int64()),
         pa.field("headers", pa.map_(pa.large_string(), pa.large_string())),
         pa.field("body", pa.large_string()),
         pa.field("final_url", pa.large_string()),
     ])

    Examples
     --------
     >>> from chalk import _
     >>> import chalk.functions as F
     >>> from chalk.functions.http import HttpResponse
     >>> @features
     ... class User:
     ...    id: str
     ...    resp: HttpResponse[str] = F.http_request("https://example.com", "GET")
     ...    status_code: int = _.resp.status_code
     ...    resp_body: str = _.resp.body
    """

    status_code: Optional[int]
    headers: Optional[Mapping[str, str]]
    body: Optional[T]
    final_url: Optional[str]


__all__ = ["HttpResponse"]
