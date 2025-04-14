#!/usr/bin/env python3.11
"""
Provides classes that execute tests requiring happy- and unhappy-path
tests for all class members and functions within a source module.
"""

from __future__ import annotations

# Built-In Imports
import inspect
import sys

from importlib import import_module
from types import ModuleType

# Third-Party Imports

# Path Manipulations (avoid these!) and "Local" Imports
# TODO: uncomment these (or remove them) when needed
from goblinfish.testing.pact.abcs import HasSourceAndTestEntities
from goblinfish.testing.pact.pact_logging import logger

# Module "Constants" and Other Attributes


# Module Functions
def is_inherited(member_name: str, cls: type) -> bool:
    """
    Determines whether a member of a class, identified by its name, is
    inherited from one or more parent classes of a class.

    Parameters:
    -----------
    member_name : str
        The name of the member to check inheritance status of
    cls : type
        The class that the member-name is checked for.

    Returns:
    --------
    True if the named member is inherited from a parent.
    False otherwise
    """
    parents = cls.__mro__[1:]
    result = any(
        [
            getattr(parent, member_name, None) is getattr(cls, member_name)
            for parent in parents
        ]
    )
    logger.debug(f'is_inherited({member_name}, {cls}): {result}')
    return result


# Module Abstract Base Classes
class ExaminesSourceClass(HasSourceAndTestEntities):
    """
    Mix-in class that tests that all the expected test-methods
    corresponding to the source function are present in the class.
    Test-method expectations include tests for methods and properties
    (or other data-descriptors) alike.

    Class Variables/Attributes:
    ---------------------------
    TARGET_MODULE : str
        The namespace of the module where the source class can be found.
    TARGET_CLASS : str
        [defaults to None]
        The name of the class that the TestCase is concerned with testing.
    TEST_PREFIX : str
        [defaults to 'test_']
        The string that is used to prefix all expected test-case names
        in the test module that the test-case class lives in.
    IGNORE_MEMBERS : set[str]
        [defaults to {'__subclasshook__', '__init_subclass__', '__weakref__'}]
        A collection of member-names that will NOT have test requirements.
        These are typically auto-generated when deriving from an ABC
        (Abstract Base Class)
    HAPPY_SUFFIX : str
        [defaults to '_happy_paths']
        The suffix to apply to names for happy-path test-methods
    INVALID_SUFFIX : str
        [defaults to '_bad_{argument}']
        The suffix to apply to names for unhappy-happy-path test-methods.
        Note that it contains a placeholder for an argument name!
    INVALID_DEL_SUFFIX : str
        [defaults to '_invalid_del']
        The suffix to apply to unhappy-path tests of delete methods of
        properties and data-descriptors
    IGNORE_CLASS_SCOPES: tuple[str]
        [defaults to ('self', 'cls')]
        Parameter-names to ignore in test-method requirements. These are
        typical initial parameters for method class-members, and are always
        expected to be handled correctly by the Python interpreter.
    """

    TARGET_MODULE = ''
    TARGET_CLASS = None
    TEST_PREFIX = 'test_'
    IGNORE_MEMBERS = set(
        ['__subclasshook__', '__init_subclass__', '__weakref__']
    )
    HAPPY_SUFFIX = '_happy_paths'
    INVALID_SUFFIX = '_bad_{argument}'
    INVALID_DEL_SUFFIX = '_invalid_del'
    IGNORE_CLASS_SCOPES = ('self', 'cls')

    def test_source_class_has_expected_test_methods(self):
        """
        Asserts that the expected test-method names are all present
        in the class.
        """
        for expected in self.expected_test_entities:
            with self.subTest(
                f'Verifying that {self.__class__.__name__}.'
                f'{expected} exists as a test-method'
            ):
                self.assertTrue(
                    expected in self.test_entities,
                    f'Missing expected test-method - {expected}'
                )

    @property
    def test_entities(self) -> set[str]:
        """
        Gets the actual test-method names defined in the class
        """
        results = set(
            [
                name for name, member
                in inspect.getmembers(self.__class__, callable)
                if name.startswith(self.TEST_PREFIX)
                and (
                    inspect.isfunction(member)
                    or inspect.ismethod(member)
                )
            ]
        )
        return results

    @property
    def expected_test_entities(self) -> set[str]:
        """
        Gets the test-method names expected in the instance
        """
        results = set()
        for name in self.source_entities:
            target_element = getattr(self.target_class, name)

            # By default, everything should have a happy-path test
            suffixes = [self.HAPPY_SUFFIX]

            # Handle creating test-method expectations for properties and
            # other data-descriptor members.
            # There are more data-descriptor-like implementations than just
            # properties, so check based on the interface expectations (see
            # https://docs.python.org/3.11/howto/descriptor.html#properties)
            # instead of relying on inspect.isdatadescriptor. :-/
            if any(
                [
                    getattr(target_element, method_name, None) is not None
                    for method_name in (
                        '__get__', 'fget',
                        '__set__', 'fset',
                        '__delete__', 'fdel'
                    )
                ]
            ):
                # Check for deleter-method variations
                if any(
                    [
                        getattr(target_element, method_name, None) is not None
                        for method_name in ('__delete__', 'fdel')
                    ]
                ):
                    suffixes.append(self.INVALID_DEL_SUFFIX)
                # Check for setter-method variations
                if any(
                    [
                        getattr(target_element, method_name, None) is not None
                        for method_name in ('__set__', 'fset')
                    ]
                ):
                    if getattr(target_element, 'fset', None) is not None:
                        setter_method = target_element.fset
                    elif getattr(target_element, '__set__', None) is not None:
                        setter_method = target_element.__set__
                    suffixes += [
                        '_set' + self.INVALID_SUFFIX.format(argument=arg_name)
                        for arg_name in inspect.signature(
                            setter_method
                        ).parameters.keys()
                        if arg_name not in self.IGNORE_CLASS_SCOPES
                    ]

            # Handle creating test-method expectations for methods
            elif callable(target_element) \
                    and not inspect.isclass(target_element):
                suffixes += [
                    self.INVALID_SUFFIX.format(argument=arg_name)
                    for arg_name
                    in inspect.signature(target_element).parameters.keys()
                    if arg_name not in self.IGNORE_CLASS_SCOPES
                ]

            # Gather up all the items for this member and add them to
            # the results
            test_names = set(
                [
                    f'{self.TEST_PREFIX}{name}{suffix}'
                    for suffix in suffixes
                ]
            )
            results = results.union(test_names)

        logger.debug(
            f'{self.__class__.__name__}.expected_test_entities: {results}'
        )
        return results

    @property
    def source_entities(self) -> set[str]:
        """
        Gets the actual entities present in the source target
        """
        results = set()
        methods = set(
            [
                name for name, member in inspect.getmembers(
                    self.target_class,
                    lambda m: callable(m) and not inspect.isclass(m)
                )
                if not is_inherited(name, self.target_class)
            ]
        )
        logger.debug(f'• methods ............ {methods}')
        results = results.union(methods)

        properties = set(
            [
                name for name, member in inspect.getmembers(
                    self.target_class,
                    lambda m: inspect.isdatadescriptor(m)
                )
                if not is_inherited(name, self.target_class)
            ]
        )
        logger.debug(f'• data-descriptors ... {properties}')
        results = results.union(properties)

        results = results.difference(self.IGNORE_MEMBERS)
        logger.debug(
            f'{self.__class__.__name__}[{self.target_module.__name__}'
            f'{self.target_class}].source_entities: {results}'
        )
        return results

    @property
    def target_class(self) -> type:
        """
        Gets the class that the instance is concerned with testing
        from the specified module namespace for the class
        """
        assert self.TARGET_CLASS is not None, (
            f'{self.__class__.__name__} needs to define a TARGET_CLASS '
            'class attribute with the name of the class being tested.'
        )
        result = getattr(self.target_module, self.TARGET_CLASS)
        logger.debug(f'{self.__class__.__name__}.target_class: {result}')
        return result

    @property
    def target_module(self) -> ModuleType:
        """
        Gets, caches, and returns the actual module specified by the
        namespace in the class' TARGET_MODULE attribute, importing it
        locally if needed in the process.
        """
        assert self.TARGET_MODULE, (
            f'{self.__class__.__name__}.TARGET_MODULE does not have a '
            'module namespace specified in it: '
            f'"{self.TARGET_MODULE}" ({type(self.TARGET_MODULE).__name__})'
        )
        # If it's already cached, return it
        if getattr(self, '_target_module', None) is not None:
            return self._target_module

        # If it's already imported, but not cached, cache it and return it
        if self.TARGET_MODULE in sys.modules:
            self._target_module = sys.modules[self.TARGET_MODULE]
            logger.debug(f'Caching {self.TARGET_MODULE}: already imported.')
            return self._target_module

        # Import it, cache it, and return it
        namespace_segments = self.TARGET_MODULE.split('.')
        if len(namespace_segments) > 1:
            name = namespace_segments[-1]
            package = '.'.join(namespace_segments[:-1])
            logger.debug(f'Trying to import {name} from package {package}')
            self._target_module = import_module(name, package)
        else:
            logger.debug(
                f'Trying to import {self.TARGET_MODULE} from package {package}'
            )
            self._target_module = import_module(self.TARGET_MODULE)
        logger.debug(
            f'{self.__class__.__name__}.target_module: Imported '
            f'{self.TARGET_MODULE} as {self._target_module}'
        )
        return self._target_module


class ExaminesSourceFunction:
    """
    Mix-in class that tests that all the expected test-methods
    corresponding to the source function are present in the class.

    Class Variables/Attributes:
    ---------------------------
    TARGET_MODULE : str
        The namespace of the module where the source class can be found.
    TARGET_FUNCTION : str
        [defaults to None]
        The name of the function that the TestCase is concerned with testing.
    TEST_PREFIX : str
        [defaults to 'test_']
        The string that is used to prefix all expected test-case names
        in the test module that the test-case class lives in.
    HAPPY_SUFFIX : str
        [defaults to '_happy_paths']
        The suffix to apply to names for happy-path test-methods
    INVALID_SUFFIX : str
        [defaults to '_bad_{argument}']
        The suffix to apply to names for unhappy-happy-path test-methods.
        Note that it contains a placeholder for an argument name!
    """

    TARGET_MODULE = ''
    TARGET_FUNCTION = None
    TEST_PREFIX = 'test_'
    HAPPY_SUFFIX = '_happy_paths'
    INVALID_SUFFIX = '_bad_{argument}'

    def test_source_function_has_expected_test_methods(self):
        """
        Asserts that the expected test-method names are all present
        in the class.
        """
        for expected in self.expected_test_entities:
            with self.subTest(
                f'Verifying that {self.__class__.__name__}.'
                f'{expected} exists as a test-method'
            ):
                self.assertTrue(
                    expected in self.test_entities,
                    f'Missing expected test-method - {expected}'
                )

    @property
    def target_function(self) -> type:
        """
        Gets the function that the instance is concerned with testing
        from the specified module namespace for the class
        """
        assert self.TARGET_FUNCTION is not None, (
            f'{self.__class__.__name__} needs to define a TARGET_FUNCTION '
            'class attribute with the name of the function being tested.'
        )
        return getattr(self.target_module, self.TARGET_FUNCTION)

    @property
    def test_entities(self) -> set[str]:
        """
        Gets the actual test-method names defined in the class
        """
        results = set(
            [
                name for name, member
                in inspect.getmembers(self.__class__, callable)
                if name.startswith(self.TEST_PREFIX)
                and (
                    inspect.isfunction(member)
                    or inspect.ismethod(member)
                )
            ]
        )
        return results

    @property
    def expected_test_entities(self) -> set[str]:
        """
        Gets the test-method names expected in the instance
        """
        suffixes = [self.HAPPY_SUFFIX] + [
            self.INVALID_SUFFIX.format(argument=arg_name)
            for arg_name
            in inspect.signature(self.target_function).parameters.keys()
        ]
        results = set(
            [
                f'{self.TEST_PREFIX}{self.target_function.__name__}'
                f'{suffix}'
                for suffix in suffixes
            ]
        )
        return results

    @property
    def target_module(self) -> ModuleType:
        """
        Gets, caches, and returns the actual module specified by the
        namespace in the class' TARGET_MODULE attribute, importing it
        locally if needed in the process.
        """
        assert self.TARGET_MODULE, (
            f'{self.__class__.__name__}.TARGET_MODULE does not have a '
            'module namespace specified in it: '
            f'"{self.TARGET_MODULE}" ({type(self.TARGET_MODULE).__name__})'
        )
        # If it's already cached, return it
        if getattr(self, '_target_module', None) is not None:
            return self._target_module

        # If it's already imported, but not cached, cache it and return it
        if self.TARGET_MODULE in sys.modules:
            self._target_module = sys.modules[self.TARGET_MODULE]
            logger.debug(f'Caching {self.TARGET_MODULE}: already imported.')
            return self._target_module

        # Import it, cache it, and return it
        namespace_segments = self.TARGET_MODULE.split('.')
        if len(namespace_segments) > 1:
            name = namespace_segments[-1]
            package = '.'.join(namespace_segments[:-1])
            logger.debug(f'Trying to import {name} from package {package}')
            self._target_module = import_module(name, package)
        else:
            logger.debug(
                f'Trying to import {self.TARGET_MODULE} from package {package}'
            )
            self._target_module = import_module(self.TARGET_MODULE)
        logger.debug(f'Imported {self.TARGET_MODULE} as {self._target_module}')
        return self._target_module


# Module Concrete Classes

# Code to run if the module is executed directly
if __name__ == '__main__':
    pass
