# -*- coding: iso-8859-1 -*-
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email.Header import Header
from email import Encoders
import StringIO


# Newer function with keyword parameters and multiple files
def send_mail(
        self,
        subject=None,
        efrom=None,
        eto=None,
        body_html=None,
        body_plain=None,
        files=None,
        reply_to=None,
        encoding_txt='iso-8859-1',
        encoding_html='iso-8859-1'):
    """Parameters:
    eto: must be a list of dictionaries (name and email)
    files: must be a list of dictionaries (name and file)
    body_html: may be None, to send text only

    """

    # Validations - Subject, efrom, body_plain and eto can not be none
    assert subject, 'subject can not be none'
    assert efrom, 'efrom can not be none'
    assert body_plain, 'body_plain can not be none'
    assert type(eto) == list, 'eto must be list'

    e_subject = subject
    e_from = efrom
    e_to = ''

    body_html = body_html
    body_plain = body_plain

    mime_msg = MIMEMultipart('related')
    mime_msg['Subject'] = Header(e_subject, encoding_txt)

    for to_item in eto:
        assert type(to_item) == dict, 'to_item must be a dictionary'
        e_to = e_to + \
            '%s <%s>, ' % (
                Header(to_item['name'], encoding_txt), to_item['email'])

    mime_msg['To'] = e_to

    # We should separate name and email address before encoding
    # this handling was necessary because this field already come formatted
    mime_msg['From'] = '%s <%s' % (
        Header(e_from.split('<')[0], encoding_txt), e_from.split('<')[1])

    # Optional parameter: make the reply-to address allow an alternative
    # address
    if reply_to:
        mime_msg['Reply-to'] = reply_to

    mime_msg.preamble = 'This is a multi-part message in MIME format.'

    # Encapsulate the plain and HTML versions of the message body
    # in an 'alternative' part, so message agents can decide
    # which they want to display.
    msgalternative = MIMEMultipart('alternative')
    mime_msg.attach(msgalternative)

    # plain part
    msg_txt = MIMEText(body_plain, _charset=encoding_txt)
    msgalternative.attach(msg_txt)

    if body_html:
        # html part
        msg_txt = MIMEText(body_html, _subtype='html', _charset=encoding_html)
        msgalternative.attach(msg_txt)

    # Attaching Files
    if files:
        assert type(files) == list, 'files must be list'
        for file in files:
            assert type(file) == dict, 'file must be a dictionary'
            part = MIMEBase('application', "octet-stream")
            filehandle = StringIO.StringIO(file["file"])
            part.set_payload(filehandle.read())
            filehandle.close()
            Encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition', 'attachment; filename=' + file["name"])
            mime_msg.attach(part)

    self.MailHost.send(mime_msg.as_string())
