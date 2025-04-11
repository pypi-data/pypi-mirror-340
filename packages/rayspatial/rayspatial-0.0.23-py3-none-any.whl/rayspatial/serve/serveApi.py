import copy
from math import log
import requests
from rayspatial.serve.config.config import engine_config, config
import ray
import threading
from queue import Queue
import rayspatial.serve.exe
from rayspatial.serve.serveApiUtils import _calcate_paralle_num, _split_bbox


class ServeApi:
    @staticmethod
    def execute_serve_api(params, header):
        p = {"params": params, "header": header}
        if ray.is_initialized():
            if engine_config.ray_address_ip is None:
                serve_exe_result = requests.post(
                    f"http://0.0.0.0:{config.config_ray['serve_port']}/rs", json=p
                )
            else:
                serve_exe_result = requests.post(
                    f"http://{engine_config.ray_address_ip}:{config.config_ray['serve_port']}/rs",
                    json=p,
                )
            serve_exe_result = serve_exe_result.json()
        else:
            # model local
            serve_exe_result = rayspatial.serve.exe.ServeExecute.execute_serve(
                params, header
            )
        return serve_exe_result

    @staticmethod
    def execute_serve_api_paraller(params, header, paralle_num=1):
        bbox = header.get("bbox")
        scale = header.get("scale")
        paralle_num = _calcate_paralle_num(bbox, scale)
        print(f"paralle_num: {paralle_num}")
        sub_bboxes = _split_bbox(bbox, scale, paralle_num)
        results_queue = Queue()
        def worker(sub_bbox):
            tempHeader = copy.deepcopy(header)
            tempHeader["bbox"] = sub_bbox
            result = ServeApi.execute_serve_api(params, tempHeader)
            results_queue.put(result)
        threads = []
        for sub_bbox in sub_bboxes:
            thread = threading.Thread(target=worker, args=(sub_bbox,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        results = []
        while not results_queue.empty():
            results.append(results_queue.get())
        return results



