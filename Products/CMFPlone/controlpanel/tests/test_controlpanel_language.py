# -*- coding: utf-8 -*-
from zope.component import getMultiAdapter
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import ILanguageSchema
from Products.CMFPlone.testing import \
    PRODUCTS_CMFPLONE_INTEGRATION_TESTING

import unittest2 as unittest


class LanguageRegistryIntegrationTest(unittest.TestCase):
    """Test that the Language settings are stored as plone.app.registry
    settings.
    """

    layer = PRODUCTS_CMFPLONE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(
            ILanguageSchema, prefix="plone")

    def test_language_controlpanel_view(self):
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name="language-controlpanel")
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_language_in_controlpanel(self):
        self.controlpanel = getToolByName(self.portal, "portal_controlpanel")
        self.assertTrue('PloneLanguageTool' in [
            a.getAction(self)['id']
            for a in self.controlpanel.listActions()
        ])

    def test_use_combined_language_codes_exists(self):
        self.assertTrue(hasattr(self.settings, 'use_combined_language_codes'))

    def test_default_language_exists(self):
        self.assertTrue(hasattr(self.settings, 'default_language'))
