# Copyright 2008-2011 Nokia Networks
# Copyright 2011-2016 Ryan Tomac, Ed Manlove and contributors
# Copyright 2016-     Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from SeleniumLibrary.utils import escape_xpath_value


class ContextAware(object):

    def __init__(self, ctx):
        """Base class exposing attributes from the common context.

        :param SeleniumLibrary.SeleniumLibrary ctx:
            The library itself as a context object.
        """
        self.ctx = ctx

    @property
    def driver(self):
        return self.ctx.driver

    @property
    def drivers(self):
        return self.ctx._drivers

    @property
    def element_finder(self):
        return self.ctx._element_finder

    def find_element(self, locator, tag=None, required=True, parent=None):
        """Find element matching `locator`.

        :param locator: Locator to use when searching the element.
            See library documentation for the supported locator syntax.
        :param tag: Limit searching only to these elements.
        :param required: Raise `ElementNotFound` if element not found when
            true, return `None` otherwise.
        :param parent: Optional parent `WebElememt` to search child elements
            from. By default search starts from the root using `WebDriver`.
        :return: Found `WebElement` or `None` if element not found and
            `required` is false.
        :rtype: selenium.webdriver.remote.webelement.WebElement
        :raises SeleniumLibrary.errors.ElementNotFound: If element not found
            and `required` is true.
        """
        return self.element_finder.find(locator, tag, True, required, parent)

    def find_elements(self, locator, tag=None, parent=None):
        """Find all elements matching `locator`.

        Always returns a list of `WebElement` objects. If no matching element
        is found, the list is empty. Otherwise semantics are exactly same
        as with :meth:`find_element`.
        """
        return self.element_finder.find(locator, tag, False, False, parent)

    def is_text_present(self, text):
        locator = "xpath://*[contains(., %s)]" % escape_xpath_value(text)
        return self.find_element(locator, required=False) is not None

    def is_element_enabled(self, locator, tag=None):
        element = self.find_element(locator, tag)
        return (element.is_enabled() and
                element.get_attribute('readonly') is None)
