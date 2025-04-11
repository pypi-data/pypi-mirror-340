import copy
from venv import logger
import requests
from rayspatial.serve.config.config import engine_config, config
import ray
import threading
import rayspatial.serve.exe
from rayspatial.serve.serveApiUtils import _calcate_paralle_num, _split_bbox
from datetime import datetime


class ServeApi:
    @staticmethod
    def execute_serve_api(params, header):
        s1 = datetime.now()
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
        logger.info(f"execute_serve_api use time: {datetime.now()-s1}")
        return serve_exe_result

    @staticmethod
    def execute_serve_api_paraller(params, header, paralle_num=1):
        s1 = datetime.now()
        bbox = header.get("bbox")
        scale = header.get("scale")
        paralle_num = _calcate_paralle_num(bbox, scale)
        print(f"paralle_num: {paralle_num}")
        sub_bboxes = _split_bbox(bbox, scale, paralle_num)
        results = []
        threads = []
        total_tasks = len(sub_bboxes)
        completed_tasks = 0
        lock = threading.Lock()

        def worker(sub_bbox, results, index):
            nonlocal completed_tasks
            tempHeader = copy.deepcopy(header)
            tempHeader["bbox"] = sub_bbox
            result = ServeApi.execute_serve_api(params, tempHeader)
            results[index] = result
            with lock:
                nonlocal completed_tasks
                completed_tasks += 1
                progress = (completed_tasks / total_tasks) * 100
                print(f"进度: {progress:.2f}% ({completed_tasks}/{total_tasks}) {datetime.now()}")

        results = [None] * len(sub_bboxes)
        for i, sub_bbox in enumerate(sub_bboxes):
            thread = threading.Thread(target=worker, args=(sub_bbox, results, i))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        print(f"execute_serve_api_paraller use time: {datetime.now()-s1}")
        return results



