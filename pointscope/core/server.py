import grpc
from concurrent import futures
from pointscope.protos import pointscope_pb2_grpc
from .pointscope_service import PointScopeServicer
import logging
from .pointscope_o3d import PointScopeO3D


class PointScopeServer:

    def __init__(self, ip="0.0.0.0", port="50051"):
        self.ip = ip
        self.port = port

    def run(self, vis_delegate=PointScopeO3D):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        pointscope_pb2_grpc.add_PointScopeServicer_to_server(
            PointScopeServicer(vis_delegate), server)

        server.add_insecure_port(f'{self.ip}:{self.port}')
        server.start()
        logging.info(f"Start PointScope gRPC service at {self.ip}:{self.port}")
        server.wait_for_termination()
