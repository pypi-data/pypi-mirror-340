"""Geometry operations module.

This module provides classes and functions for performing geometric operations
on geospatial data, such as buffering, reprojection, and clipping.
"""

from typing import Optional, Union

import geopandas as gpd
from loguru import logger

# Configure logging


class GeometryOperationError(Exception):
    """Custom exception for geometry operation errors."""

    pass


class GeometryProcessor:
    """Handle geometry operations with validation and error handling.

    This class provides methods for common
    geometric operations on GeoDataFrames,
    including buffering, reprojection, and clipping. All operations include
    input validation and proper error handling.
    """

    def __init__(self, input_gdf: Optional[gpd.GeoDataFrame] = None):
        """Initialize the processor with an optional GeoDataFrame."""
        self.gdf = input_gdf
        self._validate_gdf()

    def _validate_gdf(self) -> None:
        """Validate the GeoDataFrame."""
        if self.gdf is not None:
            if not isinstance(self.gdf, gpd.GeoDataFrame):
                raise GeometryOperationError("Input must be a GeoDataFrame")
            if not self.gdf.geometry.is_valid.all():
                logger.warning(
                    "Some geometries in the GeoDataFrame are invalid"
                )

    def set_data(self, gdf: gpd.GeoDataFrame) -> None:
        """Set the GeoDataFrame to process."""
        self.gdf = gdf
        self._validate_gdf()

    def apply_buffer(self, buffer_size: float) -> gpd.GeoDataFrame:
        """Apply a buffer operation to the geometry.

        Args:
            buffer_size: Buffer size to apply

        Returns:
            GeoDataFrame with buffered geometries

        Raises:
            GeometryOperationError: If operation fails
        """
        if self.gdf is None:
            raise GeometryOperationError("No GeoDataFrame set")

        try:
            logger.info(f"Applying buffer of size {buffer_size}")
            og_crs = self.gdf.crs
            self.gdf.geometry = (
                self.gdf.geometry.to_crs(epsg=3857)
                .buffer(buffer_size)
                .to_crs(og_crs)
            )
            return self.gdf
        except Exception as e:
            raise GeometryOperationError(
                f"Buffer operation failed: {str(e)}"
            ) from e

    def reproject(self, output_crs: Union[int, str]) -> gpd.GeoDataFrame:
        """Reproject the GeoDataFrame to a new CRS.

        Args:
            output_crs: Target coordinate reference system

        Returns:
            Reprojected GeoDataFrame

        Raises:
            GeometryOperationError: If reprojection fails
        """
        if self.gdf is None:
            raise GeometryOperationError("No GeoDataFrame set")

        try:
            logger.info(f"Reprojecting to CRS: {output_crs}")
            self.gdf = self.gdf.to_crs(crs=output_crs)
            return self.gdf
        except Exception as e:
            raise GeometryOperationError(
                f"Reprojection failed: {str(e)}"
            ) from e

    def clip(self, mask_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        """Clip the GeoDataFrame with a mask.

        Args:
            mask_gdf: GeoDataFrame to use as clip mask

        Returns:
            Clipped GeoDataFrame

        Raises:
            GeometryOperationError: If clipping fails
        """
        if self.gdf is None:
            raise GeometryOperationError("No GeoDataFrame set")

        try:
            logger.info("Applying clip operation")
            if self.gdf.crs != mask_gdf.crs:
                logger.info("Converting mask to match input CRS")
                mask_gdf = mask_gdf.to_crs(self.gdf.crs)

            self.gdf = gpd.clip(self.gdf, mask_gdf)
            return self.gdf
        except Exception as e:
            raise GeometryOperationError(
                f"Clipping operation failed: {str(e)}"
            ) from e


# For backward compatibility
def apply_buffer(
    gdf: gpd.GeoDataFrame, buffer_size: float
) -> gpd.GeoDataFrame:
    """Legacy function for backward compatibility."""
    processor = GeometryProcessor(gdf)
    return processor.apply_buffer(buffer_size)


def reproject_gdf(
    gdf: gpd.GeoDataFrame, output_crs: Union[int, str]
) -> gpd.GeoDataFrame:
    """Legacy function for backward compatibility.

    Args:
        gdf: GeoDataFrame to reproject
        output_crs: Target CRS to reproject to

    Returns:
        Reprojected GeoDataFrame
    """
    return gdf.to_crs(crs=output_crs)
