import rasterio
import numpy as np
from rasterio.warp import calculate_default_transform
from rasterio import Affine
from rayspatial.serve.common import constants
from rayspatial.serve.core.utils.imageUtils import ImageUtils
from shapely import box
from shapely.geometry import shape
from rasterio import merge
from rasterio.warp import (
    calculate_default_transform,
    transform_bounds,
    reproject,
    Resampling,
)
from rasterio.crs import CRS


class ImageReadUtils:
    @staticmethod
    def calculate_intersection(src, bbox2):
        crs = constants.EPSG_4326
        orgBbox = src.bounds
        bbox2 = transform_bounds(
            crs,
            src.crs,
            float(bbox2[0]),
            float(bbox2[1]),
            float(bbox2[2]),
            float(bbox2[3]),
        )
        if bbox2:
            left, bottom, right, top = orgBbox
            min_lon, min_lat, max_lon, max_lat = bbox2
            min_lon = max(left, min_lon)
            min_lat = max(bottom, min_lat)
            max_lon = min(right, max_lon)
            max_lat = min(top, max_lat)
            return [min_lon, min_lat, max_lon, max_lat]
        else:
            return list(orgBbox)

    @staticmethod
    def read_image(path: str, header=None):
        src = rasterio.open(path)
        meta_session = src.meta.copy()
        win, outHeight, outWidth, win_transform = ImageReadUtils._window_by_scale(
            src, header
        )
        data = src.read(
            masked=True, out_shape=(src.count, outHeight, outWidth), window=win
        )
        meta_session.update(height=outHeight, width=outWidth, transform=win_transform)
        data, meta_data = ImageReadUtils._cover_data_to_bounds(
            data, meta_session, header.bbox, header=header
        )
        geometry = f"{shape(box(*ImageUtils.transform_bbox_to_crs(header.bbox, src.crs, constants.EPSG_4326)))}"
        return data, meta_data, geometry

    @staticmethod
    def _window_by_scale(src, header):
        x_resolution_org = abs((src.bounds[2] - src.bounds[0]) / src.width)
        y_resolution_org = abs((src.bounds[3] - src.bounds[1]) / src.height)
        meta_session = src.meta
        if "UTM" not in meta_session["crs"].to_wkt() or (
            "Sinusoidal" in meta_session["crs"].to_wkt()
        ):
            orgBbox = list(
                transform_bounds(src.crs, CRS.from_epsg("3857"), *src.bounds)
            )
            _, transWidth, transHeight = calculate_default_transform(
                src.crs, CRS.from_epsg("3857"), src.width, src.height, *src.bounds
            )
            x_resolution = abs((orgBbox[2] - orgBbox[0]) / transWidth)
            y_resolution = abs((orgBbox[3] - orgBbox[1]) / transHeight)
            if header.scale is None:
                header.scale = x_resolution
            h_factor = y_resolution / header.scale
            w_factor = x_resolution / header.scale
        else:
            if header.scale is None:
                header.scale = x_resolution_org
            h_factor = y_resolution_org / header.scale
            w_factor = x_resolution_org / header.scale
        src_bbox = list(src.bounds)
        bbox2 = ImageReadUtils.calculate_intersection(src, header.bbox)
        widthStart = (bbox2[0] - src_bbox[0]) / x_resolution_org
        if widthStart < 0:
            widthStart = 0
        widthEnd = (bbox2[2] - src_bbox[0]) / x_resolution_org
        if src.transform.b != 0 and src.transform.d != 0:
            heightStart = (bbox2[1] - src_bbox[1]) / y_resolution_org
            if heightStart < 0:
                heightStart = 0
            heightEnd = (bbox2[3] - src_bbox[1]) / y_resolution_org
        else:
            heightStart = (src_bbox[3] - bbox2[3]) / y_resolution_org
            if heightStart < 0:
                heightStart = 0
            heightEnd = (src_bbox[3] - bbox2[1]) / y_resolution_org
        outHeight = int((heightEnd * h_factor - heightStart * h_factor))
        outWidth = int((widthEnd * w_factor - widthStart * w_factor))
        win = ((int(heightStart), int(heightEnd)), (int(widthStart), int(widthEnd)))
        win_transform = src.window_transform(win)
        win_transform = Affine(
            win_transform.a / w_factor,
            win_transform.b / w_factor,
            win_transform.c,
            win_transform.d / h_factor,
            win_transform.e / h_factor,
            win_transform.f,
        )
        return win, outHeight, outWidth, win_transform

    @staticmethod
    def _cover_data_to_dataSet(
        data: np.ma.MaskedArray, meta: dict, header=None
    ) -> rasterio.io.DatasetReader:
        memfile = rasterio.MemoryFile()
        if meta.get("scale"):
            del meta["scale"]
        dst = memfile.open(**meta)
        dst.write(data)
        src = memfile.open()
        return src

    @staticmethod
    def _create_empty_image_by_bounds(bounds, header, mask_value, dtype, count):
        resolution = header.scale
        x_res = resolution
        y_res = -abs(resolution)
        left, bottom, right, top = bounds
        cols = int(round((right - left) / abs(x_res)))
        rows = int(round((top - bottom) / abs(y_res)))
        data = np.full((count, rows, cols), fill_value=mask_value, dtype=dtype)
        masked_array = np.ma.masked_array(
            data=data,
            mask=(data == mask_value),
            fill_value=mask_value,
        )
        transform = Affine.translation(left, top) * Affine.scale(x_res, y_res)
        meta = {
            "driver": "GTiff",
            "dtype": dtype,
            "nodata": mask_value,
            "width": cols,
            "height": rows,
            "count": count,
            "crs": constants.EPSG_3857,
            "transform": transform,
        }
        dataset = ImageReadUtils._cover_data_to_dataSet(masked_array, meta)
        return dataset

    @staticmethod
    def _cover_data_to_bounds(
        data: np.ma.MaskedArray,
        meta: dict,
        to_bounds: list,
        to_bounds_crs=constants.EPSG_4326,
        header=None,
    ) -> (np.ma.MaskedArray, dict):
        to_bounds = ImageUtils.transform_bbox_to_crs(
            to_bounds, from_crs=to_bounds_crs, to_crs=constants.EPSG_3857
        )
        merge_ds = []
        nodata = meta.get("nodata")
        empty_dataset = ImageReadUtils._create_empty_image_by_bounds(
            to_bounds, header, nodata, data.dtype, meta["count"]
        )
        merge_ds.append(empty_dataset)
        if not data.size == 0:
            data, meta = ImageReadUtils._cover_crs_to_3857(data, meta)
            dataset = ImageReadUtils._cover_data_to_dataSet(data, meta)
            merge_ds.append(dataset)
        
        dest, transform = merge.merge(
            merge_ds,
            target_aligned_pixels=True,
            res=header.scale,
            bounds=empty_dataset.bounds,
            nodata=nodata,
        )
        masked_dest = np.ma.masked_equal(dest, nodata)
        meta.update(
            {
                "transform": transform,
                "height": masked_dest.shape[1],
                "width": masked_dest.shape[2],
                "bounds": to_bounds,
            }
        )
        return masked_dest, meta

    @staticmethod
    def _cover_crs_to_3857(data, meta):
        resampling = Resampling.bilinear
        src_crs = meta["crs"]
        src_transform = meta["transform"]
        src_nodata = meta.get("nodata", None)
        src_count, src_height, src_width = data.shape
        left = src_transform[2]
        top = src_transform[5]
        right = left + src_transform[0] * src_width
        bottom = top + src_transform[4] * src_height
        src_bounds = (left, bottom, right, top)
        dst_crs = "EPSG:3857"
        dst_transform, dst_width, dst_height = calculate_default_transform(
            src_crs, dst_crs, src_width, src_height, *src_bounds
        )
        dst_meta = meta.copy()
        dst_meta.update(
            {
                "crs": dst_crs,
                "transform": dst_transform,
                "width": dst_width,
                "height": dst_height,
                "nodata": src_nodata,
            }
        )
        dst_data = np.ma.masked_array(
            np.zeros((src_count, dst_height, dst_width), dtype=data.dtype),
            mask=True,
            fill_value=src_nodata,
        )

        for band in range(src_count):
            reproject(
                source=data[band],
                destination=dst_data.data[band],
                src_transform=src_transform,
                src_crs=src_crs,
                dst_transform=dst_transform,
                dst_crs=dst_crs,
                src_nodata=src_nodata,
                dst_nodata=src_nodata,
                resampling=resampling,
            )

        if src_nodata is not None:
            dst_data.mask = dst_data.data == src_nodata
        else:
            dst_data.mask = np.zeros_like(dst_data.data, dtype=bool)
        return dst_data, dst_meta
