# FastAPI GDAL Web API

Welcome to the FastAPI GDAL Web API! This API provides a suite of endpoints to process geospatial data using the powerful GDAL library, all within a Docker container for ease of deployment and isolation.

## Endpoints Overview

The API provides the following endpoints:

- `/process`: A placeholder endpoint for future processing capabilities.
- `/convert`: Converts raster files to GeoJSON format.
- `/reproject`: Reprojects raster files from one coordinate reference system (CRS) to another.
- `/rastercalc`: Performs raster calculations on input files using a given mathematical expression.
- `/extractvalues`: Extracts values from a raster file at given geolocated points.
- `/resample`: Resamples a raster file to a new resolution.

Each endpoint is designed to handle file uploads and perform specific operations using GDAL commands. The results are returned in the response, making it easy to integrate this API into your geospatial data workflows.

## Lessons for GDAL to iOS Middleware

This web API serves as an exploratory project that will inform the development of a GDAL to iOS middleware. Through this API, we can learn about the intricacies of handling geospatial data in a server environment and how to effectively expose GDAL's functionality over HTTP. These lessons will be invaluable in creating a robust middleware that brings the power of GDAL to iOS applications.



