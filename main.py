from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import List, Tuple
import os
from subprocess import run

app = FastAPI()

@app.post("/process")
async def process_files(files: List[UploadFile]):
    pass

@app.post("/convert")
async def convert_files(files: List[UploadFile]):
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)

    try:
        for file in files:
            file_path = os.path.join(temp_dir, file.filename)
            with open(file_path, "wb") as temp_file:
                temp_file.write(file.file.read())

            gdal_command = ["gdal_polygonize.py", file_path, "-f", "GeoJSON", "output.json"]
            run(gdal_command, check=True)

        with open("output.json", "rb") as result_file:
            result = result_file.read()

    finally:
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)

    return {"message": "Conversion complete", "result": result}

@app.post("/reproject")
async def reproject_files(files: List[UploadFile], src_crs: str, dst_crs: str):
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)

    try:
        for file in files:
            file_path = os.path.join(temp_dir, file.filename)
            with open(file_path, "wb") as temp_file:
                temp_file.write(file.file.read())

            gdal_command = ["gdalwarp", "-s_srs", src_crs, "-t_srs", dst_crs, file_path, "output.tif"]
            run(gdal_command, check=True)

        with open("output.tif", "rb") as result_file:
            result = result_file.read()

    finally:
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)

    return {"message": "Reprojection complete", "result": result}


@app.post("/rastercalc")
async def raster_calculation(expression: str, output_file: str, input_files: List[UploadFile]):
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)

    try:
        # Save the uploaded files to the temporary directory
        file_paths = []
        for file in input_files:
            file_path = os.path.join(temp_dir, file.filename)
            with open(file_path, "wb") as temp_file:
                temp_file.write(file.file.read())
            file_paths.append(file_path)

        # Prepare the gdal_calc.py command
        gdal_command = ["gdal_calc.py", "-A", file_paths[0], "--outfile", output_file, "--calc", expression]

        # If there are more than one input files, add them to the command
        for i, file_path in enumerate(file_paths[1:], start=2):
            gdal_command.extend([f"-{chr(64+i)}", file_path])

        # Run the command
        run(gdal_command, check=True)

        # Read the result file
        with open(output_file, "rb") as result_file:
            result = result_file.read()

    finally:
        # Clean up the temporary directory
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)

    return {"message": "Raster calculation complete", "result": result}


@app.post("/extractvalues")
async def extract_values(points: List[Tuple[float, float]], raster_file: UploadFile):
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)

    try:
        # Save the uploaded file to the temporary directory
        file_path = os.path.join(temp_dir, raster_file.filename)
        with open(file_path, "wb") as temp_file:
            temp_file.write(raster_file.file.read())

        # Prepare the gdallocationinfo command and run it for each point
        results = []
        for point in points:
            gdal_command = ["gdallocationinfo", "-valonly", "-geoloc", file_path, str(point[0]), str(point[1])]
            result = run(gdal_command, check=True, stdout=PIPE, encoding='utf-8')
            results.append(float(result.stdout.strip()))

    finally:
        # Clean up the temporary directory
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)

    return {"message": "Value extraction complete", "results": results}


@app.post("/resample")
async def resample_raster(x_res: float, y_res: float, raster_file: UploadFile):
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)

    try:
        # Save the uploaded file to the temporary directory
        file_path = os.path.join(temp_dir, raster_file.filename)
        with open(file_path, "wb") as temp_file:
            temp_file.write(raster_file.file.read())

        # Prepare the gdalwarp command
        output_file = "output_resampled.tif"
        gdal_command = ["gdalwarp", "-tr", str(x_res), str(y_res), file_path, output_file]
        
        # Run the command
        run(gdal_command, check=True)

        # Read the result file
        with open(output_file, "rb") as result_file:
            result = result_file.read()

    finally:
        # Clean up the temporary directory
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)

    return {"message": "Resampling complete", "result": result}