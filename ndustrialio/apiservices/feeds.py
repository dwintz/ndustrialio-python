from datetime import datetime

from ndustrialio.apiservices import *

class FeedsService(Service):


    def __init__(self, client_id, client_secret=None):
        super(FeedsService, self).__init__(client_id, client_secret)


    def baseURL(self):
        return 'https://feeds.api.ndustrial.io'

    def audience(self):

        return 'iznTb30Sfp2Jpaf398I5DN6MyPuDCftA'


    def getFeeds(self, id=None, execute=True):

        if id is None:
            uri='feeds'
        else:
            assert isinstance(id, int)
            uri='feeds/'+str(id)


        return self.execute(GET(uri=uri), execute=execute)

    def getRecordByKey(self, key, execute=True):

        params = {"key": key}

        feed = self.execute(GET(uri='feeds').params(params), execute=execute)

        if feed.records:
            return feed.records[0]

        return None

    def getFieldDescriptors(self, feed_id, limit=100, offset=0, execute=True):

        assert isinstance(feed_id, int)
        assert isinstance(limit, int)
        assert isinstance(offset, int)

        params = {'limit': limit,
                  'offset': offset}

        return self.execute(GET('feeds/{}/fields'.format(feed_id)).params(params), execute=execute)

    def getUnprovisionedFieldDescriptors(self, feed_id, limit=100, offset=0, execute=True):

        assert isinstance(feed_id, int)
        assert isinstance(limit, int)
        assert isinstance(offset, int)

        params = {'limit': limit,
                  'offset': offset}

        return self.execute(GET('feeds/{}/fields/unprovisioned'
                                .format(feed_id)).params(params), execute=execute)


    def getFeedOutputs(self, feed_id, limit=100, offset=0, execute=True):
        assert isinstance(feed_id, int)
        assert isinstance(limit, int)
        assert isinstance(offset, int)

        params = {'limit': limit,
                  'offset': offset}

        return self.execute((GET('feeds/{}/outputs'.format(feed_id)).params(params)), execute=execute)

    def getUnprovisionedData(self, feed_id, field_descriptor, time_start, time_end=None, execute=True):
        assert isinstance(feed_id, int)
        assert isinstance(field_descriptor, str)

        params = {'time_start':time_start.strftime('%s')}

        if time_end:
            assert isinstance(time_end, datetime)
            params['time_end'] = time_end.strftime('%s')

        return self.execute(GET('feeds/{}/fields/{}/data'
                                .format(feed_id, field_descriptor))
                                .params(params), execute=execute)

    def getData(self, output_id, field_human_name, window, time_start, time_end=None, limit=100, execute=True):
        assert isinstance(output_id, int)
        assert isinstance(field_human_name, basestring)
        assert isinstance(time_start, datetime)
        assert window in [0, 60, 900, 3600]

        params = {'timeStart': time_start.strftime('%s'),
                    'window': str(window),
                    'limit': limit}

        if time_end:
            assert isinstance(time_end, datetime)
            params['timeEnd'] = time_end.strftime('%s')


        return self.execute(GET('outputs/{}/fields/{}/data'
                                .format(output_id, field_human_name))
                                .params(params), execute=execute)

    def getOutputsForFacility(self, facility_id=None, limit=100, offset=0, execute=True):
        assert isinstance(facility_id, int)

        params = {'facility_id': facility_id,
                    'limit': limit,
                  'offset': offset}

        return self.execute(GET(uri='outputs').params(params), execute=execute)

    def getOutputs(self, id=None, limit=100, offset=0, execute=True):

        if id is None:
            uri='outputs'
        else:
            assert isinstance(id, int)
            uri='outputs/'+str(id)

        params = {'limit': limit,
                  'offset': offset}

        return self.execute(GET(uri=uri).params(params), execute=execute)


    def getFields(self, output_id, execute=True):

        assert isinstance(output_id, int)

        return self.execute(GET('outputs/' + str(output_id) + '/fields'), execute=execute)

    def getTypes(self, execute=True):

        return self.execute(GET('feeds/types'), execute=execute)

    def updateStatus(self, feed_id, status, execute=True):
        assert isinstance(feed_id, int)
        # Check type of status

        params = {'status': str(status)}

        return self.execute(POST('feeds/{}/status'
                            .format(feed_id))
                            .params(params), execute=execute)

    def getLatestStatus(self, execute=True):

        return self.execute(GET('feeds/status/latest'), execute=execute)