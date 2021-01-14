import sys
from pathlib import Path

import lmdb
from flask import Flask, Response
from protobuf import prediction_pb2

from serializers import pack_native_uint32, unpack_native_uint, create_arrival_predictions_request_log_pb
from tfl_api import get_arrival_predictions as tfl_get_arrival_predictions

PROJECT_PATH = Path(__name__).parent.resolve()

app = Flask(__name__)

env = lmdb.open(bytes(PROJECT_PATH / 'bramfitt_db'), max_dbs=2)
request_db = env.open_db(b'arrival_predictions_request', integerkey=True)


def log_arrival_predictions_request(log_pb):
    with env.begin(db=request_db, write=True) as txn:
        with txn.cursor() as cur:
            if cur.last():
                last_request_id = unpack_native_uint(cur.key())
                request_id = last_request_id + 1
            else:
                request_id = 1

            log_pb.request_id = request_id

            txn.put(
                pack_native_uint32(request_id),
                log_pb.SerializeToString(),
            )


@app.route('/arrivals/<naptan_id>', methods=('GET', ))
def get_arrival_predictions(naptan_id):
    predictions = tuple(tfl_get_arrival_predictions(naptan_id))

    log_pb = create_arrival_predictions_request_log_pb(
        naptan_id,
        predictions,
    )

    log_arrival_predictions_request(log_pb)

    response_pb = prediction_pb2.ArrivalPredictionsResponse()
    response_pb.predictions.extend(predictions)

    return Response(
        response=response_pb.SerializeToString(),
        status=200,
        mimetype='application/protobuf',
    )


def print_requests():
    with env.begin(db=request_db, write=True) as txn:
        with txn.cursor() as cur:
            for key, value in cur:
                print(int.from_bytes(key, byteorder=sys.byteorder, signed=False))
                log = prediction_pb2.ArrivalPredictionsRequestLog()
                log.ParseFromString(value)
                print(log)
