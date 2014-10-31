from openerp_proxy.orm.record import RecordList


class HTMLTable(object):
    """ HTML Table representation object for RecordList

        :param recordlist: record list to create represetation for
        :type recordlist: RecordList instance
        :param fields: list of fields to display. each field should be string
                       with dot splitted names of related object, or callable
                       of one argument (record instance)
        :type fields: list(string | callable)
        :param highlight_row: function to check if row to be highlighted
        :type highlight_row: callable(record) -> bool
    """
    def __init__(self, recordlist, fields, highlight_row=None):
        self._recordlist = recordlist
        self._fields = fields
        self._highlight_row = highlight_row

    def _get_field(self, record, field):
        if callable(field):
            return field(record)

        fields = field.split('.')
        r = record
        while fields:
            field = fields.pop(0)
            try:
                r = r[field]
            except KeyError:
                try:
                    r = r[int(field)]
                except (KeyError, ValueError):
                    try:
                        r = getattr(r, field)
                        if callable(r):
                            r = r()
                    except AttributeError:
                        raise
        return r

    def _repr_html_(self):
        table = "<table>%s</table>"
        trow = "<tr>%s</tr>"
        throw = '<tr style="background: #ffff99">%s</tr>'
        tcaption = "<caption>%s</caption>" % self._recordlist
        theaders = "".join(("<th>%s</th>" % field for field in self._fields))
        data = ""
        data += tcaption
        data += trow % theaders
        for record in self._recordlist:
            tdata = "".join(("<td>%s</td>" % self._get_field(record, field) for field in self._fields))
            if self._highlight_row is not None and self._highlight_row(record):
                data += throw % tdata
            else:
                data += trow % tdata
        return table % data


class RecordListData(RecordList):
    """ Extend record list to add aditional methods related to RecordList representation
    """

    def as_table(self, fields=None):
        """ Table representation of record list

            At this moment hust (ID | Name) table
        """
        if fields is None:
            res = "     ID | Name\n"
            res += "\n".join(("%7s | %s" % (r.id, r._name) for r in self))
            return res
        raise NotImplementedError()

    def as_html_table(self, *fields, **kwargs):
        """ HTML Table representation object for RecordList

            :param fields: list of fields to display. each field should be string
                           with dot splitted names of related object, or callable
                           of one argument (record instance)
            :type fields: list(string | callable)
            :param highlight_row: function to check if row to be highlighted
            :type highlight_row: callable(record) -> bool
        """
        return HTMLTable(self, fields, **kwargs)


