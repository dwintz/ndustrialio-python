import time
from ndustrialio.apiservices import *
from ndustrialio.apiservices.helpers.data_helper import DataHelper


class FeedsService(Service):


    def __init__(self, client_id, client_secret=None):
        super(FeedsService, self).__init__(client_id, client_secret)
        self.data_helper = DataHelper()


    def baseURL(self):
        return 'https://feeds.api.ndustrial.io'

    def audience(self):

        return 'iznTb30Sfp2Jpaf398I5DN6MyPuDCftA'

    def getFeeds(self, id=None, execute=True):

        if id is None:
            uri='feeds'
        else:
            # assert isinstance(id, int)
            uri='feeds/'+str(id)

        return self.execute(GET(uri=uri), execute=execute)

    def getFeedByKey(self, key, execute=True):

        params = {"key": key}

        if execute:
            return PagedResponse(self.execute(GET(uri='feeds').params(params), execute=True))

        else:
            return self.execute(GET(uri='feeds').params(params), execute=False)

    def createFeed(self, key, timezone, type, facility_id, execute=True):

        feed_data = {'key': key,
                     'timezone': timezone,
                     'feed_type': type,
                     'facility_id': facility_id,
                     'routing_keys': '["development.'+type+'.'+key+'"]'}

        return self.execute(POST(uri='feeds').body(feed_data)
                            .content_type(ApiRequest.URLENCODED_CONTENT_TYPE), execute = execute)

    def createOutput(self, feed_id, facility_id, label, type, key=None, execute=True):

        output_data = {'feed_id': feed_id,
                       'facility_id': facility_id,
                       'label': label,
                       'output_type': type}
        if key:
            output_data['key']=key

        return self.execute(POST(uri='outputs').body(output_data)
                            .content_type(ApiRequest.URLENCODED_CONTENT_TYPE), execute = execute)

    def createField(self, feed_key, output_id, human_name, field_descriptor, label=None, type=None, execute=True):

        field_data = {'feed_key': feed_key,
                'output_id': output_id,
                'field_human_name': human_name,
                'field_descriptor': field_descriptor}

        if type:
            field_data['value_type'] = type
        if label:
            field_data['label'] = label

        return self.execute(POST(uri='outputs/{}/fields'.format(output_id)).body(field_data)
                            .content_type(ApiRequest.URLENCODED_CONTENT_TYPE), execute = execute)

    def getFieldDescriptors(self, feed_id, limit=100, offset=0, execute=True):

        # assert isinstance(feed_id, int)
        # assert isinstance(limit, int)
        # assert isinstance(offset, int)

        params = {'limit': limit,
                  'offset': offset}

        return self.execute(GET('feeds/{}/fields'.format(feed_id)).params(params), execute=execute)

    def getUnprovisionedFieldDescriptors(self, feed_id, limit=100, offset=0, execute=True):

        # assert isinstance(feed_id, int)
        # assert isinstance(limit, int)
        # assert isinstance(offset, int)

        params = {'limit': limit,
                  'offset': offset}

        return self.execute(GET('feeds/{}/fields/unprovisioned'
                                .format(feed_id)).params(params), execute=execute)

    def getFeedOutputs(self, feed_id, limit=100, offset=0, execute=True):

        # assert isinstance(feed_id, int)
        # assert isinstance(limit, int)
        # assert isinstance(offset, int)

        params = {'limit': limit,
                  'offset': offset}

        return self.execute((GET('feeds/{}/outputs'.format(feed_id)).params(params)), execute=execute)

    def getUnprovisionedData(self, feed_id, field_descriptor, time_start, time_end=None, execute=True):

        # assert isinstance(feed_id, int)
        # assert isinstance(field_descriptor, str)

        params = {'time_start': str(get_epoch_time(time_start))}

        if time_end:
            assert isinstance(time_end, datetime)
            params['time_end'] = str(get_epoch_time(time_end))

        return self.execute(GET('feeds/{}/fields/{}/data'
                                .format(feed_id, field_descriptor))
                                .params(params), execute=execute)

    def getData(self, output_id, field_human_name, window, time_start, time_end=None, limit=100, execute=True):

        # assert isinstance(output_id, int)
        # assert isinstance(field_human_name, basestring)
        # assert isinstance(time_start, datetime)
        # assert window in [0, 60, 900, 3600]

        params = {'timeStart': str(get_epoch_time(time_start)),
                    'window': str(window),
                    'limit': limit}

        if time_end:
            params['timeEnd'] = str(get_epoch_time(time_end))

        # TODO: remove this.  The caller should wrap response objects
        if execute:
            return DataResponse(data=self.execute(GET('outputs/{}/fields/{}/data'
                                                      .format(output_id, field_human_name))
                                                  .params(params), execute=True),
                                client=self.client)
        else:
            return self.execute(GET('outputs/{}/fields/{}/data'
                                                      .format(output_id, field_human_name))
                                                  .params(params), execute=False)

    def getOutputsForFacility(self, facility_id=None, limit=100, offset=0, execute=True):

        # assert isinstance(facility_id, int)

        params = {'facility_id': facility_id,
                    'limit': limit,
                  'offset': offset}


        if execute:
            return PagedResponse(self.execute(GET(uri='outputs').params(params), execute=True))

        else:
            return self.execute(GET(uri='outputs').params(params), execute=False)

    def getOutputs(self, id=None, limit=100, offset=0, execute=True):

        if id is None:
            uri='outputs'
        else:
            # assert isinstance(id, int)
            uri='outputs/'+str(id)

        params = {'limit': limit,
                  'offset': offset}

        return self.execute(GET(uri=uri).params(params), execute=execute)

    def getFields(self, output_id, execute=True):

        # assert isinstance(output_id, int)

        return self.execute(GET('outputs/' + str(output_id) + '/fields'), execute=execute)

    def getTypes(self, execute=True):

        return self.execute(GET('feeds/types'), execute=execute)

    def updateStatus(self, feed_id, status, execute=True):

        # assert isinstance(feed_id, int)
        # Check type of status

        params = {'status': str(status)}

        return self.execute(POST('feeds/{}/status'
                            .format(feed_id))
                            .params(params), execute=execute)

    def getLatestStatus(self, execute=True):
        return self.execute(GET('feeds/status/latest'), execute=execute)


    # def batch(self, api_requests):
    #
    #     batch_body = {}
    #
    #     i = 0
    #
    #     for api_request in api_requests:
    #         batch_body['request_'+str(i)] = {'method': api_request.method(),
    #                                          'uri': str(api_request)}
    #         i+=1
    #
    #     return self.execute(POST(uri='batch').body(batch_body), execute=True)

    def getFieldDataMetrics(self, output_id_list, field_label, stale_seconds=None, start_time=None):

        assert isinstance(output_id_list, list)
        assert isinstance(field_label, str)
        test = [True if isinstance(id, int) else False for id in output_id_list]
        if False in test:
            raise Exception('All elements in the output_id_list must be integers (FeedsService.getFieldDataMetrics)')

        body = {
                "output_id_list": output_id_list,
                "labels": [field_label]
                }

        params = {}

        if stale_seconds:
            assert isinstance(stale_seconds, int)
            params["stale_seconds"] = stale_seconds

        if start_time:
            assert isinstance(start_time, datetime)
            params["timeStart"] = get_epoch_time(start_time)

        return self.execute(POST(uri='metrics/fieldDataMetrics')
                            .body(body)
                            .params(params))

    def getBatchFieldDataMetrics(self, start_time_datetime, end_time_datetime, minute_interval, field_identification_list):

        time_array = []
        value_array = []
        aggregate_batch_data = []
        data_request_map = {}
        request_count = 0
        MAX_BATCH_REQUESTS = 20

        num_bins, end_time_datetime = self.data_helper.calculateNumberOfBinsAndEndTime(start_time_datetime, end_time_datetime, minute_interval)
        start_time_utc = time.mktime(start_time_datetime.timetuple())
        end_time_utc = time.mktime(end_time_datetime.timetuple())

        for field_identification in field_identification_list:

            output_id = field_identification['output_id']
            field_human_name = field_identification['field_human_name']

            key = "{}.{}".format(output_id, field_human_name)

            data_request = self.getData(output_id=output_id,
                                field_human_name=field_human_name,
                                time_end=end_time_datetime,
                                time_start=start_time_datetime,
                                window=60,
                                execute=False)

            data_request_map[key] = {'method': data_request.method(),
                                     'uri': str(data_request)}

            request_count += 1

            if request_count == MAX_BATCH_REQUESTS:
                batch_data = self.execute(POST(uri='batch').body(data_request_map), execute=True)
                for key, value in batch_data.items():
                    aggregate_batch_data += value['body']['records']
                request_count = 0
                data_request_map = {}

        batch_data = self.execute(POST(uri='batch').body(data_request_map), execute=True)
        for key, value in batch_data.items():
            aggregate_batch_data += value['body']['records']

        for record in aggregate_batch_data:

            timestamp_datetime = datetime.strptime(record['event_time'], "%Y-%m-%dT%H:%M:%S.%fZ")
            timestamp_utc = time.mktime(timestamp_datetime.timetuple())
            try:
                value_array.append(float(record['value']))
                time_array.append(timestamp_utc)
            except:
                print ('Bad value: {}'.format(record['value']))

        metrics_map = self.data_helper.calculateMetrics(time_array, value_array, start_time_utc, end_time_utc, num_bins)

        return metrics_map
