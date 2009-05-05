from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Policy(models.Model):
    """
    A Flash cross-domain access policy.

    """
    SITE_CONTROL_ALL = u'A'
    SITE_CONTROL_BY_CONTENT_TYPE = u'C'
    SITE_CONTROL_BY_FTP_FILENAME = u'F'
    SITE_CONTROL_MASTER_ONLY = u'M'
    SITE_CONTROL_NONE = u'N'

    SITE_CONTROL_CHOICES = (
        (SITE_CONTROL_MASTER_ONLY, _(u"Master policy file only")),
        (SITE_CONTROL_ALL, _(u"All policy files on this domain")),
        (SITE_CONTROL_BY_CONTENT_TYPE, _(u"Only policy files with canonical content-type")),
        (SITE_CONTROL_BY_FTP_FILENAME, _(u"Only policy files with canonical filename")),
        (SITE_CONTROL_NONE, _(u"No policy files")),
        )
    site = models.ForeignKey(Site)
    site_control = models.CharField(_(u"Allow policies to be applied from"),
                                    max_length=1,
                                    choices=SITE_CONTROL_CHOICES,
                                    default=SITE_CONTROL_MASTER_ONLY)
    allow_subdomains = models.BooleanField(_(u"Allow access for any subdomain of this domain"),
                                           default=False,
                                           help_text=_(u"Due to serious security issues, this is <strong>NOT</strong> recommended."))
    allow_all = models.BooleanField(_(u"Allow access for any domain"),
                                    default=False,
                                    help_text=_(u"Due to serious security issues, this is <strong>NOT</strong> recommended."))
    
    class Meta:
        ordering = ('site__name',)
        verbose_name = _(u"Policy")
        verbose_name_plural = _(u"Policies")

    def __unicode__(self):
        return u"Cross-domain Flash policy for %s" % self.site


class PermittedDomain(models.Model):
    """
    Rules for a particular domain within a Flash cross-domain access
    policy.
    
    """
    policy = models.ForeignKey(Policy)
    domain = models.CharField(max_length=255)
    allow_subdomains = models.BooleanField(_(u"Allow access for any subdomain of this domain"),
                                           default=False,
                                           help_text=_(u"Due to serious security issues, this is <strong>NOT</strong> recommended."))

    class Meta:
        ordering = ('domain',)
        verbose_name = _(u"Permitted domain")
        verbose_name_plural = _(u"Permitted domains")

    def __unicode__(self):
        return u"%s permitted for %s" % (self.domain, self.policy.site)
