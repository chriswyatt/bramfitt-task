import sys
from functools import partial

from protobuf import prediction_pb2


OPERATION_TYPE_MAPPING = {
    1: prediction_pb2.Prediction.OperationType.NEW_OR_UPDATED,
    2: prediction_pb2.Prediction.OperationType.INVALIDATED,
}

DIRECTION_MAPPING = {
    'inbound': prediction_pb2.Prediction.Direction.INBOUND,
    'outbound': prediction_pb2.Prediction.Direction.OUTBOUND,
}

pack_native_uint32 = partial(
    int.to_bytes,
    4,
    byteorder=sys.byteorder,
    signed=False,
)

unpack_native_uint = partial(
    int.from_bytes,
    byteorder=sys.byteorder,
    signed=False,
)


def create_prediction_pb(prediction_dict):
    prediction = prediction_pb2.Prediction()

    if 'id' in prediction_dict:
        prediction.prediction_id = prediction_dict['id']

    if 'operationType' in prediction_dict:
        prediction.operation_type = OPERATION_TYPE_MAPPING[prediction_dict['operationType']]

    if 'vehicleId' in prediction_dict:
        prediction.vehicle_id = prediction_dict['vehicleId']

    if 'naptanId' in prediction_dict:
        prediction.naptan_id = prediction_dict['naptanId']

    if 'stationName' in prediction_dict:
        prediction.station_name = prediction_dict['stationName']

    if 'lineId' in prediction_dict:
        prediction.line_id = prediction_dict['lineId']

    if 'lineName' in prediction_dict:
        prediction.line_name = prediction_dict['lineName']

    if 'platformName' in prediction_dict:
        prediction.platform_name = prediction_dict['platformName']

    if 'direction' in prediction_dict:
        prediction.direction = DIRECTION_MAPPING[prediction_dict['direction']]

    if 'bearing' in prediction_dict:
        prediction.bearing = int(prediction_dict['bearing'])

    if 'destinationNaptanId' in prediction_dict:
        prediction.destination_naptan_id = prediction_dict['destinationNaptanId']

    if 'destinationName' in prediction_dict:
        prediction.destination_name = prediction_dict['destinationName']

    if 'timestamp' in prediction_dict:
        prediction.prediction_sent_at.FromJsonString(prediction_dict['timestamp'])

    if 'timeToStation' in prediction_dict:
        prediction.seconds_to_station = prediction_dict['timeToStation']

    if 'currentLocation' in prediction_dict:
        prediction.current_location = prediction_dict['currentLocation']

    if 'towards' in prediction_dict:
        prediction.towards = prediction_dict['towards']

    if 'expectedArrival' in prediction_dict:
        prediction.expected_arrival_at.FromJsonString(prediction_dict['expectedArrival'])

    if 'timeToLive' in prediction_dict:
        prediction.invalidated_at.FromJsonString(prediction_dict['timeToLive'])

    if 'modeName' in prediction_dict:
        prediction.mode_name = prediction_dict['modeName']

    if 'timing' in prediction_dict:
        timing_dict = prediction_dict['timing']
        timing = prediction.timing

        if 'source' in timing_dict:
            timing.source_timestamp.FromJsonString(timing_dict['source'])

        if 'insert' in timing_dict:
            timing.inserted_at.FromJsonString(timing_dict['insert'])

        if 'read' in timing_dict:
            timing.read_at.FromJsonString(timing_dict['read'])

        if 'sent' in timing_dict:
            timing.sent_at.FromJsonString(timing_dict['sent'])

        if 'received' in timing_dict:
            timing.received_at.FromJsonString(timing_dict['received'])

    return prediction


def create_arrival_predictions_request_log_pb(naptan_id, predictions):
    log_pb = prediction_pb2.ArrivalPredictionsRequestLog()

    log_pb.naptan_id = naptan_id
    log_pb.requested_at.GetCurrentTime()

    log_pb.predictions.extend(predictions)

    return log_pb
