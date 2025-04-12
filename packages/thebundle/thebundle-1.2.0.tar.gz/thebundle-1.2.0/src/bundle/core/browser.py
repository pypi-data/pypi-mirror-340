# Copyright 2024 HorusElohim

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from __future__ import annotations

from contextlib import asynccontextmanager
from enum import Enum

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

from typing import AsyncIterator, List, Type

from playwright.async_api import Browser as PlaywrightBrowser
from playwright.async_api import BrowserContext, ElementHandle, Page, Playwright, async_playwright

from . import data, entity, tracer
from .logger import get_logger

logger = get_logger(__name__)


class BrowserType(Enum):
    CHROMIUM = "chromium"
    FIREFOX = "firefox"
    WEBKIT = "webkit"


class Browser(entity.Entity):
    """
    Simplified asynchronous Playwright browser wrapper with dynamic configuration,
    chainable methods, and robust error handling.

    Example Usage:
        async with Browser.chromium(headless=False) as browser:
            page = await browser.new_page()
    """

    # Shared Playwright instance per process
    _playwright: Playwright | None = data.PrivateAttr(default=None)
    is_closed: bool = data.Field(default=False, exclude=True)
    browser_type: BrowserType = data.Field(default=BrowserType.CHROMIUM)
    headless: bool = data.Field(default=True)
    browser: PlaywrightBrowser | None = data.Field(default=None, exclude=True)
    contexts: List[BrowserContext] = data.Field(default_factory=list, exclude=True)

    @data.field_validator("browser_type", mode="before")
    def validate_browser_type(cls, v: str | BrowserType) -> BrowserType:
        if isinstance(v, str):
            try:
                return BrowserType(v.lower())
            except ValueError:
                supported = [bt.value for bt in BrowserType]
                raise ValueError(f"Unsupported browser type: {v}. Supported types are: {supported}")
        if isinstance(v, BrowserType):
            return v
        raise ValueError(f"Invalid browser type: {v}")

    @classmethod
    @asynccontextmanager
    async def chromium(cls: Type[Self], headless: bool = True, **kwargs) -> AsyncIterator[Self]:
        """
        Context manager to instantiate a Chromium browser.
        """
        instance = cls(browser_type=BrowserType.CHROMIUM, headless=headless, **kwargs)
        try:
            await instance.__aenter__()
            yield instance
        finally:
            await instance.__aexit__(None, None, None)

    @classmethod
    @asynccontextmanager
    async def firefox(cls: Type[Self], headless: bool = True, **kwargs) -> AsyncIterator[Self]:
        """
        Context manager to instantiate a Firefox browser.
        """
        instance = cls(browser_type=BrowserType.FIREFOX, headless=headless, **kwargs)
        try:
            await instance.__aenter__()
            yield instance
        finally:
            await instance.__aexit__(None, None, None)

    @classmethod
    @asynccontextmanager
    async def webkit(cls: Type[Self], headless: bool = True, **kwargs) -> AsyncIterator[Self]:
        """
        Context manager to instantiate a WebKit browser.
        """
        instance = cls(browser_type=BrowserType.WEBKIT, headless=headless, **kwargs)
        try:
            await instance.__aenter__()
            yield instance
        finally:
            await instance.__aexit__(None, None, None)

    async def __aenter__(self) -> Self:
        """
        Enter the asynchronous context manager, starting Playwright and launching the browser.
        """
        await self.launch()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Exit the asynchronous context manager, closing the browser and stopping Playwright.
        """
        await self.close()
        if self._playwright:
            await self._playwright.stop()
            logger.debug("Playwright stopped.")

    @tracer.Async.decorator.call_raise
    async def launch(self) -> Self:
        """
        Launch the specified browser type.

        Returns:
            Browser: The current instance for method chaining.
        """
        self._playwright = await async_playwright().start()
        logger.debug("Playwright started.")

        if not self._playwright:
            raise RuntimeError("Playwright is not started.")

        if self.browser_type == BrowserType.CHROMIUM:
            self.browser = await tracer.Async.call_raise(self._playwright.chromium.launch, headless=self.headless)
        elif self.browser_type == BrowserType.FIREFOX:
            self.browser = await tracer.Async.call_raise(self._playwright.firefox.launch, headless=self.headless)
        elif self.browser_type == BrowserType.WEBKIT:
            self.browser = await tracer.Async.call_raise(self._playwright.webkit.launch, headless=self.headless)
        else:
            raise ValueError(f"Unsupported browser type: {self.browser_type.value}")

        logger.info(
            "%s Browser[%s] launched.  Headless=%s",
            logger.Emoji.success,
            self.browser_type.value.capitalize(),
            self.headless,
        )
        return self

    @tracer.Async.decorator.call_raise
    async def new_context(self, *args, **kwargs) -> Self:
        """
        Create a new browser context.

        Returns:
            Browser: The current instance for method chaining.
        """
        if not self.browser:
            raise RuntimeError("Browser is not launched. Call launch() first.")

        context = await self.browser.new_context(*args, **kwargs)
        self.contexts.append(context)
        logger.debug("%s New browser context created.", logger.Emoji.success)
        return self

    @tracer.Async.decorator.call_raise
    async def new_page(self) -> Page:
        """
        Create a new page within a new browser context.

        Returns:
            Page: A new Playwright Page object.
        """
        await self.new_context()
        context = self.contexts[-1]
        page = await context.new_page()
        logger.debug("%s New page created.", logger.Emoji.success)
        return page

    @tracer.Async.decorator.call_raise
    async def close(self) -> Self:
        """
        Close all browser contexts and the browser itself.

        Returns:
            Browser: The current instance for method chaining.
        """
        if self.contexts:
            for context in self.contexts:
                try:
                    await context.close()
                    logger.debug("%s Browser context closed.", logger.Emoji.success)
                except Exception as e:
                    logger.warning("%s Failed to close a browser context: %s", logger.Emoji.warning, e)
            self.contexts.clear()

        if self.browser:
            try:
                await self.browser.close()
                logger.info("Browser closed.")
            except Exception as e:
                logger.error("%s Failed to close the browser: %s", logger.Emoji.failed, e)
            self.browser = None

        self.is_closed = True
        return self
