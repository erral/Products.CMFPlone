from Acquisition import aq_inner
from Products.PythonScripts.standard import url_quote
from Products.Five.browser import BrowserView
from Products.CMFPlone.resources.browser.resource import ResourceView
from urlparse import urlparse



class ScriptsView(ResourceView):
    """ Information for script rendering. """

    def get_data(self, bundle, result):
        if self.development is False:
            result.append({
                'conditionalcomment' : bundle.conditionalcomment,
                'src': '%s/%s?version=%s' % (self.portal_url, bundle.jscompilation, bundle.last_compilation)
                })
        else:
            resources = self.get_resources()
            for resource in bundle.resources:
                if resource in resources:        
                    script = resources[bundle.resource]
                    if script.js:
                        url = urlparse(script.js)
                        if url.netloc == '':
                            # Local
                            src = "%s/%s" % (self.portal_url, script.js)
                        else:
                            src = "%s" % (script.js)

                        data = {'conditionalcomment' : bundle.conditionalcomment,
                                'src': src}
                        result.append(data)


    # def get_manual_data(self, script):
    #     """
    #     Gets the information of a specific style
    #     Style is a CSS manual entry
    #     """
    #     data = None
    #     if script.enabled:
    #         if script.expression:
    #                 if script.cooked_expression:
    #                     expr = Expression(script.expression)
    #                     script.cooked_expression = expr
    #                 if self.evaluateExpression(script.cooked_expression, context):
    #                     return data
    #         url = urlparse(script.url)
    #         if url.netloc == '':
    #             # Local
    #             src = "%s/%s" % (self.portal_url, script.url)
    #         else:
    #             src = "%s" % (script.url)

    #         data = {'conditionalcomment' : script.conditionalcomment,
    #                 'src': src}
    #         return data

    def scripts(self):
        """ 
        The requirejs scripts, the ones that are not resources
        are loaded on configjs.py
        """
        result = []        
        # We always add jquery resource 
        result.append({
            'src':'%s/%s' % (
                self.portal_url, 
                self.registry.records['Products.CMFPlone.resources/jquery.js'].value)
            ,
            'conditionalcomment': None
        })


        if self.development:
            # We need to add require.js and config.js
            result.append({
                'src':'%s/%s' % (
                    self.portal_url, 
                    self.registry.records['Products.CMFPlone.resources.less-variables'].value)
                ,

                'conditionalcomment': None
            })
            result.append({
                'src':'%s/%s' % (
                    self.portal_url, 
                    self.registry.records['Products.CMFPlone.resources.lessc'].value)
                ,

                'conditionalcomment': None
            })
            result.append({
                'src':'%s/%s' % (
                    self.portal_url, 
                    self.registry.records['Products.CMFPlone.resources.requirejs'].value)
                ,

                'conditionalcomment': None
            })
            result.append({
                'src':'%s/%s' % (
                    self.portal_url, 
                    self.registry.records['Products.CMFPlone.resources.configjs'].value)
                ,
                'conditionalcomment': None
            })
            
        result.extend(self.ordered_bundles_result())
        # manual_result = self.get_manual_order('js')
        result.extend(manual_result)

        return result
