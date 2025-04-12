"""Copy action for content rules."""
from Acquisition import aq_base
from OFS.event import ObjectClonedEvent
from OFS.SimpleItem import SimpleItem
import OFS.subscribers
from plone.app.contentrules import PloneMessageFactory as _
from plone.app.contentrules.actions import ActionAddForm
from plone.app.contentrules.actions import ActionEditForm
from plone.app.contentrules.browser.formhelper import ContentRuleFormWrapper
from plone.app.vocabularies.catalog import CatalogSource
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleElementData
try:
    from plone.base.utils import pretty_title_or_id
except ImportError:
    # BBB Plone 5
    from Products.CMFPlone.utils import pretty_title_or_id
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from ZODB.POSException import ConflictError
from zope import schema
from zope.component import adapter
from zope.event import notify
from zope.interface import implementer
from zope.interface import Interface
from zope.lifecycleevent import ObjectCopiedEvent


class ICopyAction(Interface):
    """Interface for the configurable aspects of a move action.

    This is also used to create add and edit forms, below.
    """

    target_folder = schema.Choice(
        title=_("Target folder"),
        description=_("As a path relative to the portal root."),
        required=True,
        source=CatalogSource(is_folderish=True),
    )

    change_note = schema.TextLine(
        title=_("Change note"),
        description=_(
            "Optional change note to be used when creating new version."),
        required=False,
    )


@implementer(ICopyAction, IRuleElementData)
class CopyAction(SimpleItem):
    """The actual persistent implementation of the action element."""

    target_folder = ""
    change_note = ""
    element = "eea.dexterity.indicators.Copy"

    @property
    def summary(self):
        """A summary of the element's configuration."""
        return _(
            "Copy to folder ${folder}.",
            mapping=dict(folder=self.target_folder)
        )


@adapter(Interface, ICopyAction, Interface)
@implementer(IExecutable)
class CopyActionExecutor:
    """The executor for this action."""

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        portal_url = getToolByName(self.context, "portal_url", None)
        if portal_url is None:
            return False

        obj = self.event.object

        path = self.element.target_folder
        change_note = self.element.change_note
        if len(path) > 1 and path[0] == "/":
            path = path[1:]
        target = portal_url.getPortalObject().unrestrictedTraverse(
            str(path),
            None,
        )

        if target is None:
            self.error(
                obj,
                _("Target folder ${target} does not exist.",
                  mapping={"target": path}),
            )
            return False

        old_id = obj.getId()
        new_id = self.generate_id(target, old_id)
        if not new_id.endswith('.1'):
            # Version already exists, redirect to it - refs #279130
            return True

        try:
            obj._notifyOfCopyTo(target, op=0)
        except ConflictError:
            raise
        except Exception as e:
            self.error(obj, str(e))
            return False

        orig_obj = obj
        obj = obj._getCopy(target)
        obj._setId(new_id)

        notify(ObjectCopiedEvent(obj, orig_obj))

        target._setObject(new_id, obj)
        obj = target._getOb(new_id)
        obj.wl_clearLocks()

        obj._postCopy(target, op=0)

        OFS.subscribers.compatibilityCall("manage_afterClone", obj, obj)

        notify(ObjectClonedEvent(obj))

        pr = getToolByName(obj, 'portal_repository')
        pr.save(obj=obj, comment=change_note)

        return True

    def error(self, obj, error):
        """Report an error during the copy."""
        request = getattr(self.context, "REQUEST", None)
        if request is not None:
            title = pretty_title_or_id(obj, obj)
            message = _(
                "Unable to copy ${name} as part of content rule "
                "'copy' action: ${error}",
                mapping={"name": title, "error": error},
            )
            IStatusMessage(request).addStatusMessage(message, type="error")

    def generate_id(self, target, old_id):
        """Generate a new id for the copied object."""
        taken = getattr(aq_base(target), "has_key",
                        lambda x: x in target.objectIds())

        if not taken(old_id):
            return old_id
        idx = 1
        while taken("{old_id}.{idx}".format(old_id=old_id, idx=idx)):
            idx += 1
        return "{old_id}.{idx}".format(old_id=old_id, idx=idx)


class CopyAddForm(ActionAddForm):
    """An add form for move-to-folder actions."""

    schema = ICopyAction
    label = _("Add Copy Action")
    description = _("A copy action can copy an object to a different folder.")
    Type = CopyAction


class CopyAddFormView(ContentRuleFormWrapper):
    """A wrapper for the add form."""
    form = CopyAddForm


class CopyEditForm(ActionEditForm):
    """An edit form for copy rule actions.

    z3c.form does all the magic here.
    """

    schema = ICopyAction
    label = _("Edit Copy Action")
    description = _("A copy action can copy an object to a different folder.")
    form_name = _("Configure element")


class CopyEditFormView(ContentRuleFormWrapper):
    """A wrapper for the edit form."""
    form = CopyEditForm
