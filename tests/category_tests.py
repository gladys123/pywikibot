# -*- coding: utf-8  -*-
"""Tests for the Category class."""
#
# (C) Pywikibot team, 2008-2014
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id$'

import sys
import pywikibot
from pywikibot import config
from pywikibot import InvalidTitle
import pywikibot.page

from tests.aspects import unittest, TestCase, DefaultSiteTestCase
from tests.utils import allowed_failure

if sys.version_info[0] > 2:
    basestring = (str, )
    unicode = str

class TestCategoryObject(TestCase):

    """Test Category object."""

    family = 'wikipedia'
    code = 'en'

    cached = True

    def test_isEmptyCategory(self):
        """Test if category is empty or not."""
        site = self.get_site()
        cat_empty = pywikibot.Category(site, u'Category:foooooo')
        cat_not_empty = pywikibot.Category(site, u'Category:Wikipedia categories')
        self.assertTrue(cat_empty.isEmptyCategory())
        self.assertFalse(cat_not_empty.isEmptyCategory())

    def test_isHiddenCategory(self):
        """Test isHiddenCategory"""
        site = self.get_site()
        cat_hidden = pywikibot.Category(site, u'Category:Hidden categories')
        cat_not_hidden = pywikibot.Category(site, u'Category:Wikipedia categories')
        self.assertTrue(cat_hidden.isHiddenCategory())
        self.assertFalse(cat_not_hidden.isHiddenCategory())

    def test_sortKey(self):
        """Test the sortKey attribute"""
        site = self.get_site()
        cat = pywikibot.Category(site, u'Category:Wikipedia categories', 'Example')
        self.assertEqual(cat.aslink(), u'[[Category:Wikipedia categories|Example]]')
        self.assertEqual(cat.aslink(sortKey='Foo'), u'[[Category:Wikipedia categories|Foo]]')

    def test_categoryinfo(self):
        """Test the categoryinfo property"""
        site = self.get_site()
        cat = pywikibot.Category(site, u'Category:Wikipedia categories')
        categoryinfo = cat.categoryinfo
        self.assertTrue(u'files' in categoryinfo)
        self.assertTrue(u'pages' in categoryinfo)
        self.assertTrue(u'size' in categoryinfo)
        self.assertTrue(u'subcats' in categoryinfo)

    def test_members(self):
        """Test the members method"""
        site = self.get_site()
        cat = pywikibot.Category(site, u'Category:Wikipedia legal policies')
        p1 = pywikibot.Page(site, u'Category:Wikipedia disclaimers')
        p2 = pywikibot.Page(site, u'Wikipedia:Terms of use')
        p3 = pywikibot.Page(site, u'Wikipedia:Risk disclaimer')

        members = list(cat.members())
        self.assertIn(p1, members)
        self.assertIn(p2, members)
        self.assertNotIn(p3, members)

        members_recurse = list(cat.members(recurse=True))
        self.assertIn(p1, members_recurse)
        self.assertIn(p2, members_recurse)
        self.assertIn(p3, members_recurse)

        members_namespace = list(cat.members(namespaces=14))
        self.assertIn(p1, members_namespace)
        self.assertNotIn(p2, members_namespace)
        self.assertNotIn(p3, members_namespace)

        members_total = list(cat.members(total=2))
        self.assertEqual(len(members_total), 2)

    def test_subcategories(self):
        """Test the subcategories method"""
        site = self.get_site()
        cat = pywikibot.Category(site, u'Category:Wikipedians by gender')
        c1 = pywikibot.Category(site, u'Category:Female Wikipedians')
        c2 = pywikibot.Category(site, u'Category:Lesbian Wikipedians')

        subcategories = list(cat.subcategories())
        self.assertIn(c1, subcategories)
        self.assertNotIn(c2, subcategories)

        subcategories_total = list(cat.subcategories(total=2))
        self.assertEqual(len(subcategories_total), 2)

    def test_subcategories_recurse(self):
        site = self.get_site()
        cat = pywikibot.Category(site, u'Category:Wikipedians by gender')
        c1 = pywikibot.Category(site, u'Category:Female Wikipedians')
        c2 = pywikibot.Category(site, u'Category:Lesbian Wikipedians')

        subcategories_recurse = list(cat.subcategories(recurse=True))
        self.assertIn(c1, subcategories_recurse)
        self.assertIn(c2, subcategories_recurse)

        cat2 = pywikibot.Category(site, u'Category:Biographical dictionaries by country')
        cat2_1 = pywikibot.Category(site, u'Category:Australian Dictionary of Biography')
        cat2_2 = pywikibot.Category(site, u'Category:Dictionary of National Biography')

        subcategories2_recurse = list(cat2.subcategories(recurse=True))
        self.assertIn(cat2_1, subcategories2_recurse)
        self.assertIn(cat2_2, subcategories2_recurse)

    def test_articles(self):
        """Test the articles method"""
        site = self.get_site()
        cat = pywikibot.Category(site, u'Category:Wikipedia legal policies')
        p1 = pywikibot.Page(site, u'Wikipedia:Terms of use')
        p2 = pywikibot.Page(site, u'Wikipedia:Risk disclaimer')

        articles = list(cat.articles())
        self.assertIn(p1, articles)
        self.assertNotIn(p2, articles)

        articles_recurse = list(cat.articles(recurse=True))
        self.assertIn(p1, articles_recurse)
        self.assertIn(p2, articles_recurse)

        articles_namespace = list(cat.articles(namespaces=1))
        self.assertNotIn(p1, articles_namespace)
        self.assertNotIn(p2, articles_namespace)

        articles_total = list(cat.articles(total=2))
        self.assertEqual(len(articles_total), 2)
