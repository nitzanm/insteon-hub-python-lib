class ServerSentEvent(object):
    def __init__(self, event_type, event_id, data):
        self.event_type = event_type
        self.event_id = event_id
        self.data = data

def iterate_server_sent_events(line_iterator):
    data = ''
    event_type = None
    event_id = None

    for line in line_iterator:
        # print "LINE: %s" % line
        if not line:
            # Dispatch event
            data = data.rstrip('\n')
            if data:
                yield ServerSentEvent(event_type, event_id, data)
            event_type = None
            data = ''
        if line.startswith(':'):
            continue
        if ':' in line:
            field, value = line.split(':', 1)
        else:
            field = line

        if field == 'event':
            event_type = value.lstrip(' ')
        elif field == 'data':
            data += value.lstrip(' ') + '\n'
        elif field == 'id':
            event_id = value
        else:
            # Ignore unknown fields
            pass
