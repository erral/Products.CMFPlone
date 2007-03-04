from zope.interface import Interface
from zope.component import adapts
from zope.formlib.form import FormFields
from zope.interface import implements
from zope.schema import Bool

from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.interfaces import IPloneSiteRoot

from form import ControlPanelForm

class ISecuritySchema(Interface):

    enable_self_reg = Bool(title=_(u'Enable Self Registration'),
                        description=_(u'''Allows users to join the site. 
                                       If not selected only site managers will
                                       be able to add new users.'''),
                        default=False,
                        required=True)

    enable_user_pwd_choice = Bool(title=_(u'Let Users select their passwords'),
                        description=_(u'''If not selected passwords will be 
                                       autogenerated and mailed to users.'''),
                        default=False,
                        required=True)

    enable_user_folders = Bool(title=_(u'Enable User Folders'),
                        description=_(u'''If selected home folders will be 
                                       created for new users.'''),
                        default=False,
                        required=True)

    allow_anon_views_about = Bool(title=_(u'Allow anyone to view about information'),
                        description=_(u'''If not selected only logged in users 
                                       will be able to view this information.'''),
                        default=False,
                        required=True)


class SecurityControlPanelAdapter(SchemaAdapterBase):
    
    adapts(IPloneSiteRoot)
    implements(ISecuritySchema)

    def __init__(self, context):
        super(SecurityControlPanelAdapter, self).__init__(context)
        pprop = getToolByName(context, 'portal_properties')
        self.pmembership = getToolByName(context, 'portal_membership')
        portal_url = getToolByName(context, "portal_url")
        self.portal = portal_url.getPortalObject()
        self.context = pprop.site_properties

    def get_enable_self_reg(self):
        app_perms = self.portal.rolesOfPermission(permission='Add portal member')
        for appperm in app_perms:
            if appperm['name'] == 'Anonymous' and appperm['selected'] == 'SELECTED':
                return True
            else:
                return False

    def set_enable_self_reg(self, value):
        app_perms = self.portal.rolesOfPermission(permission='Add portal member')
        reg_roles = []
        for appperm in app_perms:
            if appperm['selected'] == 'SELECTED':
                reg_roles.append(appperm['name'])
        if value == True and 'Anonymous' not in reg_roles:
            reg_roles.append('Anonymous')
        if value == False and 'Anonymous' in reg_roles:
            reg_roles.remove('Anonymous')
            
        self.portal.manage_permission('Add portal member', roles=reg_roles, acquire=0)

    enable_self_reg = property(get_enable_self_reg, set_enable_self_reg)


    def get_enable_user_pwd_choice(self):
        if self.portal.validate_email:
            return False
        else:
            return True

    def set_enable_user_pwd_choice(self, value):
        if value == True:
            self.portal.validate_email = False
        else:
            self.portal.validate_email = True

    enable_user_pwd_choice = property(get_enable_user_pwd_choice, set_enable_user_pwd_choice)


    def get_enable_user_folders(self):
        return self.pmembership.getMemberareaCreationFlag()

    def set_enable_user_folders(self, value):
        self.pmembership.memberareaCreationFlag = value

    enable_user_folders = property(get_enable_user_folders, set_enable_user_folders)


    def get_allow_anon_views_about(self):
        return self.context.site_properties.allowAnonymousViewAbout

    def set_allow_anon_views_about(self, value):
        self.context.site_properties.allowAnonymousViewAbout = value

    allow_anon_views_about = property(get_allow_anon_views_about, set_allow_anon_views_about)


class SecurityControlPanel(ControlPanelForm):

    form_fields = FormFields(ISecuritySchema)

    label = _("Security settings")
    description = _("Security settings for this site.")
    form_name = _("Site security settings")
