#!/usr/bin/env python
"""
This is an mbox filter. It scans through an entire mbox style mailbox
and shows email addresses that return with some error.
"""

import mailbox, sys

def main ():
    mailboxname_in = sys.argv[1]
    process_mailbox (mailboxname_in, passthrough_filter)

def passthrough_filter (msg, document):
    """This prints the 'from' address of the message and
    returns the document unchanged.
    """
    linha = 0
    email = ''
    error_code = ''
    from_addr = msg.getaddr('From')[1]
    for line in document.split('\n'):

     #Where the description of error begin
     if line == '   ----- The following addresses had permanent fatal errors -----':
      linha = 1

     #Address that contains some error
     elif linha == 1:
      email = line.strip('<>')
      linha = 2

     #Error
     elif linha == 2:
      if len(line.split()) > 0:
       error_code = line.split()[1]
      else:
       error_code = 'servidor invalido'
      linha = 0

    if email != '':
     print error_code + '\t' + email

    return document

def process_mailbox (mailboxname_in, filter_function):
    """This processes a each message in the 'in' mailbox and optionally
    writes the message to the 'out' mailbox. Each message is passed to
    the  filter_function. The filter function may return None to ignore
    the message or may return the document to be saved in the 'out' mailbox.
    See passthrough_filter().
    """

    # Open the mailbox.
    mb = mailbox.UnixMailbox (file(mailboxname_in,'r'))

    msg = mb.next()
    while msg is not None:
        # Properties of msg cannot be modified, so we pull out the
        # document to handle is separately. We keep msg around to
        # keep track of headers and stuff.
        document = msg.fp.read()
        document = filter_function (msg, document)

        msg = mb.next()

if __name__ == '__main__':
    main ()
