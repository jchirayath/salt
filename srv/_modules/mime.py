# -*- coding: utf-8 -*-
'''
Module for Sending Messages via SMTP - updating for mime.multipart

.. versionadded:: 2014.7.0

:depends:   - smtplib python module
:configuration: This module can be used by either passing a jid and password
    directly to send_message, or by specifying the name of a configuration
    profile in the minion config, minion pillar, or master config.

    For example:

    .. code-block:: yaml

        my-smtp-login:
            smtp.server: smtp.domain.com
            smtp.tls: True
            smtp.sender: admin@domain.com
            smtp.username: myuser
            smtp.password: verybadpass

    The resourcename refers to the resource that is using this account. It is
    user-definable, and optional. The following configurations are both valid:

    .. code-block:: yaml

        my-smtp-login:
            smtp.server: smtp.domain.com
            smtp.tls: True
            smtp.sender: admin@domain.com
            smtp.username: myuser
            smtp.password: verybadpass

        another-smtp-login:
            smtp.server: smtp.domain.com
            smtp.tls: True
            smtp.sender: admin@domain.com
            smtp.username: myuser
            smtp.password: verybadpass

'''

from __future__ import absolute_import
import logging
import tempfile
import os

log = logging.getLogger(__name__)

HAS_LIBS = False
try:
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    HAS_LIBS = True
except ImportError:
    pass


__virtualname__ = 'mime'


def __virtual__():
    '''
    Only load this module if smtplib is available on this minion.
    '''
    if HAS_LIBS:
        return __virtualname__
    return (False, 'This module is only loaded if smtplib is available')


def email_from_tpl(source, context):
    fh, tmp_file = tempfile.mkstemp()
    __salt__['cp.get_template'](source, tmp_file, **context)
    # return __salt__['template.render'](source=template, context=context)
    msg = open(tmp_file, 'r').read()

    # remove tmp file
    os.unlink(tmp_file)
    return msg


def _sanitize_recipient(recipient):
    if recipient[0] == '{':
        recipient = recipient[1:]
    if recipient[-1] == '}':
        recipient = recipient[:-1]
    return recipient


def send_msg(recipient,
             template,
             context={},
             subject='Message from Salt',
             sender=None,
             server=None,
             use_ssl='True',
             username=None,
             password=None,
             profile=None):
    '''
    Send a message to an SMTP recipient. Designed for MIME Multipart

    CLI Examples:

    .. code-block:: bash

        smtp.send_msg 'admin@example.com' 'This is a salt module test' \
            profile='my-smtp-account'
        smtp.send_msg 'admin@example.com' 'This is a salt module test' \
            username='myuser' password='verybadpass' \
            sender="admin@example.com' \
            server='smtp.domain.com'
    '''
    if profile:
        creds = __salt__['config.option'](profile)
        server = creds.get('smtp.server')
        sender = creds.get('smtp.sender')
        # TODO Why are these credentials not used later?
        # use_ssl = creds.get('smtp.tls')
        # username = creds.get('smtp.username')
        # password = creds.get('smtp.password')

    msg = MIMEMultipart('alternative')
    message = email_from_tpl(source=template, context=context)

    html = MIMEText(message, 'html')

    recipient = _sanitize_recipient(recipient)
    recipients = _sanitize_recipient(recipient)

    msg.attach(html)
    msg['Subject'] = '{}'.format(subject)
    msg['From'] = sender
    msg['To'] = recipient

#    if 'email_admin' in context.keys():
#        log.info("Context[email_admin]: %s", str(context['email_admin']))
#        cc_recipient = _sanitize_recipient(context['email_admin'])
#        msg['Cc'] = context['email_admin']
#        recipient = recipient +','+ cc_recipient
#        recipient = recipient.split(",")
#        recipient = ["recipient","cc_recipient"]
#        recipients = [r.strip() for r in recipient.split(',’)]

    smtpconn = smtplib.SMTP(server)
    log.info("recipient: %s", recipient)

    log.warning("recipient: %s", recipient)
    log.warning("subject: %s", msg['Subject'])
    log.warning("mac: %s", context.get('mac', ' no mac address given'))
    log.info("Context: %s", str(context))

    try:
        smtpconn.sendmail(sender, recipient, msg.as_string())
    except smtplib.SMTPRecipientsRefused:
        log.debug("All recipients were refused.")
        return False
    except smtplib.SMTPHeloError:
        log.debug("The server didn’t reply properly to the HELO greeting.")
        return False
    except smtplib.SMTPSenderRefused:
        log.debug("The server didn’t accept the {0}.".format(sender))
        return False
    except smtplib.SMTPDataError:
        log.debug("The server replied with an unexpected error code.")
        return False

    smtpconn.quit()
    return True
