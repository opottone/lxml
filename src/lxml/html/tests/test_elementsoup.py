import unittest, sys
from lxml.tests.common_imports import make_doctest, HelperTestCase

try:
    import BeautifulSoup
    BS_INSTALLED = True
except ImportError:
    BS_INSTALLED = False

from lxml.html import tostring

if BS_INSTALLED:
    class SoupParserTestCase(HelperTestCase):
        from lxml.html import soupparser

        def test_broken_attribute(self):
            html = """\
              <html><head></head><body>
                <form><input type='text' disabled size='10'></form>
              </body></html>
            """
            root = self.soupparser.fromstring(html)
            self.assertTrue(root.find('.//input').get('disabled') is not None)

        def test_body(self):
            html = '''<body><p>test</p></body>'''
            res = '''<html><body><p>test</p></body></html>'''
            tree = self.soupparser.fromstring(html)
            self.assertEquals(tostring(tree), res)

        def test_body_comment(self):
            html = '''<!-- comment --><body><p>test body</p></body>'''
            res = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" "http://www.w3.org/TR/REC-html40/loose.dtd">
<!-- comment --><html><body><p>test body</p></body></html>'''
            tree = self.soupparser.fromstring(html).getroottree()
            self.assertEquals(tostring(tree), res)

        def test_head_body(self):
            html = '<head><title>test</title></head><body><p>test</p></body>'
            res = '<html><head><title>test</title></head><body><p>test</p></body></html>'
            tree = self.soupparser.fromstring(html)
            self.assertEquals(tostring(tree), res)

        def test_comment1(self):
            html = '''<!-- comment -->
<?test asdf> 
<head><title>test</title></head><body><p>test</p></body>
<!-- another comment -->'''
            res = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" "http://www.w3.org/TR/REC-html40/loose.dtd">
<!-- comment --><?test asdf?><html><head><title>test</title></head><body><p>test</p></body></html><!-- another comment -->'''
            tree = self.soupparser.fromstring(html).getroottree()
            self.assertEquals(tostring(tree), res)

        def test_comment2(self):
            html = '''<!-- comment -->
<?test asdf>
<html><head><title>test</title></head><body><p>test</p></body></html>
<!-- another comment -->'''
            res = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" "http://www.w3.org/TR/REC-html40/loose.dtd">
<!-- comment --><?test asdf?><html><head><title>test</title></head><body><p>test</p></body></html><!-- another comment -->'''
            tree = self.soupparser.fromstring(html).getroottree()
            self.assertEquals(tostring(tree), res)

        def test_doctype1(self):
            html = \
'''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
 <html><head><title>My first HTML document</title></head><body><p>Hello world!</body></html>'''
            res = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html><head><title>My first HTML document</title></head><body><p>Hello world!</p></body></html>'''

            tree = self.soupparser.fromstring(html).getroottree()
            self.assertEquals(tree.docinfo.public_id, "-//W3C//DTD HTML 4.01//EN")
            self.assertEquals(tostring(tree), res)


        def test_doctype2(self):
            html = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<!-- comment --> 
<?test asdf>
<html><head><title>test</title></head><body><p>test</p></body></html>
<!-- another comment -->'''
            res = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<!-- comment --><?test asdf?><html><head><title>test</title></head><body><p>test</p></body></html><!-- another comment -->'''
            tree = self.soupparser.fromstring(html).getroottree()
            self.assertEquals(tree.docinfo.public_id, "-//W3C//DTD XHTML 1.0 Strict//EN")
            self.assertEquals(tostring(tree), res)

        def test_doctype3(self):
            # html 5 doctype declaration
            html = '''<!DOCTYPE HTML>
<html><head><title>test</title></head><body><p>test</p></body></html>
<!-- another comment -->'''
            res = '''<!DOCTYPE html>
<html><head><title>test</title></head><body><p>test</p></body></html><!-- another comment -->'''
            tree = self.soupparser.fromstring(html).getroottree()
            self.assertEquals(tree.docinfo.public_id, "")
            self.assertEquals(tostring(tree), res)




def test_suite():
    suite = unittest.TestSuite()
    if BS_INSTALLED:
        suite.addTests([unittest.makeSuite(SoupParserTestCase)])
        if sys.version_info[0] < 3:
            suite.addTests([make_doctest('../../../../doc/elementsoup.txt')])
    return suite

if __name__ == '__main__':
    unittest.main()
