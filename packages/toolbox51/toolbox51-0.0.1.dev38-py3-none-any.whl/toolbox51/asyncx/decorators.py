

import traceback
import functools
from typing import Callable, Awaitable, TypeVar, ParamSpec
from toolbox51 import logger

from .manager import manager
from . import exceptions

P = ParamSpec('P')
R = TypeVar('R')


def using_resource(
    resource: str,
    *, 
    url: str|None = None,
    priority: int|None = None,
    validate: bool = False, parallel: int|None = None, 
):
    if url is not None:
        resource = f"{resource}@{url}"
    if validate and not manager.touch_resource(resource, parallel=parallel):
        raise exceptions.InvalidResource(f"Invalid resource: {resource}")
    
    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        if not callable(func) or not func.__code__.co_flags & 0x0080:
            raise TypeError(f"Decorator {using_resource.__name__} can only be used on async functions")
        
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            await manager.check_terminate(logger_stacklevel=3)
            event = await manager.allocate(resource, priority=priority)
            if event is None:
                raise exceptions.AllocateResourceFailed(f"Failed to allocate resource {resource}.")
            try:
                try:
                    await event.wait()
                    return await func(*args, **kwargs)
                finally:
                    await manager.release(resource)
            except exceptions.ReleaseResourceFailed as e:
                raise e
            except Exception as e:
                logger.error(f"等待资源或执行任务失败: {e}")
                traceback.print_exc()
                raise e
        return wrapper
    return decorator